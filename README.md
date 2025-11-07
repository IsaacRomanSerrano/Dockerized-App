# 🐳 DevOps Infrastructure for E-Commerce
![Docker](https://img.shields.io/badge/Docker-Compose%20%7C%20Containers-blue?logo=docker)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana%20%7C%20Loki-orange?logo=grafana)
![Proxy](https://img.shields.io/badge/Reverse%20Proxy-Traefik%20%7C%20Load%20Balancing-lightgrey?logo=traefik)

> Docker-based **microservices platform** for an e-commerce environment, featuring observability, logging, and reverse proxy management.  
> Designed as a **DevOps infrastructure project** to demonstrate container orchestration, service monitoring, and scalability.  
> ☁️ Ready for future deployment on **AWS ECS Fargate**.

---

## 📘 Overview
This project represents a **complete DevOps infrastructure** for an e-commerce microservices stack.  
It includes containerized services for application logic, database, reverse proxy, and full observability (metrics and logs).

The main goal is to **replicate a production-like environment** locally using Docker Compose, preparing for later deployment to AWS.

---

## 🧰 Technologies

### **Core Services**
| Service | Purpose |
|----------|----------|
| **Traefik** | Reverse proxy and load balancer for dynamic routing. |
| **FastAPI (Product Service)** | RESTful API simulating product management in an e-commerce app. |
| **PostgreSQL** | Database service for product data persistence. |

### **Observability Stack**
| Tool | Purpose |
|------|----------|
| **Prometheus** | Metrics collection from application and infrastructure. |
| **Grafana** | Visualization and dashboards for metrics and logs. |
| **Loki** | Centralized log storage. |
| **Promtail** | Log collector and shipper to Loki. |

---

## 🧱 Architecture

The architecture consists of several **Dockerized microservices** connected through an internal network.  
Each service is observable and monitored through Prometheus and Grafana.

```mermaid
graph TD
    A[User] -->|HTTP Requests| B[Traefik: Reverse Proxy]
    B --> C[Product Service (FastAPI)]
    C --> D[PostgreSQL Database]
    C --> E[Prometheus: Metrics /metrics]
    E --> F[Grafana Dashboard]
    C --> G[Promtail: Logs Collector]
    G --> H[Loki: Log Storage]
```
## ⚙️ Implementation Steps

1. **Project Initialization**
   - Define multi-service architecture (`product-service`, `db-product`, `prometheus`, `grafana`, `loki`, `promtail`, `traefik`).

2. **Containerization**
   - Create individual Dockerfiles for each microservice.
   - Build and orchestrate them with **Docker Compose**.

3. **Database Setup**
   - PostgreSQL container with healthchecks and environment variables.  
   - Application connects through `DATABASE_URL`.

4. **Reverse Proxy Configuration**
   - **Traefik** routes requests to internal services based on labels (`PathPrefix(`/products`)`).

5. **Monitoring and Logging**
   - **Prometheus** scrapes metrics from FastAPI service.  
   - **Grafana** visualizes both metrics and logs.  
   - **Loki + Promtail** handle log aggregation.

6. **Network and Dependencies**
   - All containers share a dedicated Docker network for internal communication.  
   - Healthchecks ensure correct startup order.

7. **Validation**
   - Access APIs and dashboards locally:
     - Product API → [http://localhost:8080/products](http://localhost:8080/products)
     - Prometheus → [http://localhost:9090/targets](http://localhost:9090/targets)
     - Grafana → [http://localhost:3000](http://localhost:3000)
     - Traefik Dashboard → [http://localhost:8081](http://localhost:8081)
     - Loki API → [http://localhost:3100](http://localhost:3100)

---

## 📊 Metrics and Observability

- **Prometheus** collects service metrics from `/metrics` endpoint.  
- **Grafana** visualizes CPU, memory, request rate, and API latency.  
- **Loki** centralizes logs for all containers, accessible via Grafana’s *Explore* tab.

---

## 🚀 Usage

```bash
git clone https://github.com/IsaacRomanSerrano/ecommerce-devops.git
cd ecommerce-devops/ops/docker-compose
docker compose up --build
```
en desarrollo .....
