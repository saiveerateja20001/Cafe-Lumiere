# ☕ Café Lumière v3.0

A microservices café management application built with Python, Flask, and PostgreSQL. **Modern Version 3.0** with contemporary design and refined aesthetics.

## What is This?

Café Lumière is a complete café ordering system with:
- **Customer Interface** - Browse menu, place orders, track status
- **Kitchen Dashboard** - View and manage orders in real-time
- **Display Board** - Show ready orders for pickup
- **Three Microservices** - Frontend, Order Service, Kitchen Service
- **PostgreSQL Database** - Persistent order storage

## Quick Start

### Using Docker Compose (Recommended)

```powershell
# Build and start all services
docker-compose up --build

# Open in browser
start http://localhost:5000
```

### Manual Setup

1. **Start PostgreSQL**
```powershell
docker run -d --name cafe-db -e POSTGRES_PASSWORD=cafe123 -p 5432:5432 postgres:15
```

2. **Install Dependencies** (in each service folder)
```powershell
pip install -r requirements.txt
```

3. **Run Services**
```powershell
# Terminal 1 - Order Service
cd order-service
python app.py

# Terminal 2 - Kitchen Service
cd kitchen-service
python app.py

# Terminal 3 - Frontend
cd frontend
python app.py
```

## Access Points

- **Customer Orders:** http://localhost:5000
- **Kitchen Dashboard:** http://localhost:5000/kitchen
- **Display Board:** http://localhost:5000/display
- **Order API:** http://localhost:5001
- **Kitchen API:** http://localhost:5002

## Technology Stack

- **Backend:** Python 3.11, Flask 3.0.2
- **Database:** PostgreSQL 15
- **Frontend:** HTML5, CSS3, JavaScript
- **Containers:** Docker, Docker Compose
- **Orchestration:** Kubernetes, Helm

## Order Flow

1. **Ordered** - Customer places order through UI
2. **Preparing** - Kitchen staff starts preparing
3. **Ready** - Order ready for pickup
4. **Served** - Order delivered to customer

## Project Structure

```
cafe-lumiere/
├── frontend/          # UI service (Port 5000)
├── order-service/     # Order API (Port 5001)
├── kitchen-service/   # Kitchen API (Port 5002)
├── database/          # DB init scripts
├── k8s/              # Kubernetes configs
├── helm/             # Helm charts
├── docker-compose.yml # Local deployment
├── ARCHITECTURE.md   # System design docs
└── README.md         # This file
```

## Docker Compose Commands

```powershell
# Build images
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Clean restart
docker-compose down -v
docker-compose up --build
```

## Kubernetes Deployment

```powershell
# Deploy database
helm install cafe-db ./helm/postgresql

# Deploy services
kubectl apply -f k8s/deployments.yaml

# Check status
kubectl get pods

# Port forward to access locally
kubectl port-forward svc/frontend 5000:5000
```

## Troubleshooting

### Services not connecting
```powershell
# Check all containers are running
docker-compose ps

# View service logs
docker-compose logs frontend
docker-compose logs order-service
docker-compose logs kitchen-service
```

### Database connection issues
```powershell
# Restart database
docker-compose restart postgres

# Check database is ready
docker-compose logs postgres
```

### Port already in use
```powershell
# Find process using port
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <pid> /F
```

## Development

### Adding New Menu Items
Edit menu in [frontend/app.py](frontend/app.py) - search for `menu_items` list.

### Database Schema
The orders table is auto-created on first run. See [database/init.sql](database/init.sql).

### API Documentation
- Order Service: http://localhost:5001/health
- Kitchen Service: http://localhost:5002/health

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design, data flows, and service interactions.

---
*Bienvenue à Café Lumière* ☕
