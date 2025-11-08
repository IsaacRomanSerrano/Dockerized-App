from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import ssl
import asyncpg
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

# 🔹 URL de la base de datos (nota: mejor 'postgresql://' para asyncpg)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db-product:5432/productdb"
)

# 🔹 Contexto SSL (lo usaremos dentro del startup)
ssl_context = ssl.create_default_context()

app = FastAPI(title="product-service")

# 🔹 Métricas Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["path", "method", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Latency",
    ["path", "method"]
)

class ProductIn(BaseModel):
    name: str
    price: float
    stock: int = 0

# 🔹 Conexión a la BD en el evento de startup (aquí SÍ puedes usar await)
@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(DATABASE_URL, ssl=ssl_context)
    async with app.state.pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price NUMERIC(10,2) NOT NULL,
            stock INT NOT NULL DEFAULT 0
        )
        """)

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/products")
async def list_products():
    with REQUEST_LATENCY.labels("/products", "GET").time():
        async with app.state.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, name, price, stock FROM products ORDER BY id DESC LIMIT 100"
            )
    REQUEST_COUNT.labels("/products", "GET", "200").inc()
    return [dict(r) for r in rows]

@app.get("/products/{pid}")
async def get_product(pid: int):
    with REQUEST_LATENCY.labels("/products/{id}", "GET").time():
        async with app.state.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, name, price, stock FROM products WHERE id=$1",
                pid
            )
    if not row:
        REQUEST_COUNT.labels("/products/{id}", "GET", "404").inc()
        raise HTTPException(404, "Not found")
    REQUEST_COUNT.labels("/products/{id}", "GET", "200").inc()
    return dict(row)

@app.post("/products", status_code=201)
async def create_product(p: ProductIn):
    with REQUEST_LATENCY.labels("/products", "POST").time():
        async with app.state.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO products(name, price, stock)
                VALUES($1, $2, $3)
                RETURNING id, name, price, stock
                """,
                p.name, p.price, p.stock
            )
    REQUEST_COUNT.labels("/products", "POST", "201").inc()
    return dict(row)

