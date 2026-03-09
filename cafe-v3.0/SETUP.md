# ☕ Café Lumière v3.0 - Setup Guide

## Prerequisites

Install these first:
- Docker Desktop (https://www.docker.com/products/docker-desktop)
- Python 3.11+ (https://www.python.org/downloads/)
- Git (optional)

## Option 1: Docker Compose (Recommended)

### One-Command Setup
```powershell
docker-compose up --build
```

Access at: http://localhost:5000

### Individual Commands
```powershell
# Build all images
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Clean restart (removes data)
docker-compose down -v
docker-compose up --build
```

---

## Option 2: Manual Setup (Development)

### 1. Start PostgreSQL Database
```powershell
docker run -d `
  --name cafe-db `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=cafe123 `
  -e POSTGRES_DB=cafe_db `
  -p 5432:5432 `
  postgres:15
```

### 2. Setup Order Service
```powershell
cd order-service
pip install -r requirements.txt
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="cafe_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="cafe123"
python app.py
```

### 3. Setup Kitchen Service (New Terminal)
```powershell
cd kitchen-service
pip install -r requirements.txt
$env:ORDER_SERVICE_URL="http://localhost:5001"
python app.py
```

### 4. Setup Frontend (New Terminal)
```powershell
cd frontend
pip install -r requirements.txt
$env:ORDER_SERVICE_URL="http://localhost:5001"
$env:KITCHEN_SERVICE_URL="http://localhost:5002"
python app.py
```

---

## Option 3: Kubernetes Deployment

### 1. Deploy PostgreSQL with Helm
```powershell
# Install PostgreSQL
helm install cafe-db ./helm/postgresql

# Wait for database to be ready
kubectl wait --for=condition=ready pod -l app=postgresql --timeout=120s
```

### 2. Deploy Application Services
```powershell
# Deploy all services
kubectl apply -f k8s/deployments.yaml

# Check deployment status
kubectl get pods
kubectl get services
```

### 3. Access the Application
```powershell
# Port forward to access locally
kubectl port-forward svc/frontend 5000:5000
```

Access at: http://localhost:5000

### 4. Cleanup Kubernetes
```powershell
# Delete all services
kubectl delete -f k8s/deployments.yaml

# Delete database
helm uninstall cafe-db
```

---

## Verification Commands

### Check Docker Containers
```powershell
# List running containers
docker ps

# View specific service logs
docker logs cafe-frontend
docker logs cafe-order-service
docker logs cafe-kitchen-service
docker logs cafe-postgres
```

### Test API Endpoints
```powershell
# Order Service health check
curl http://localhost:5001/health

# Kitchen Service health check
curl http://localhost:5002/health

# Get all orders
curl http://localhost:5001/orders
```

### Database Connection Test
```powershell
# Connect to PostgreSQL
docker exec -it cafe-postgres psql -U postgres -d cafe_db

# Inside psql, run:
# \dt                    -- List tables
# SELECT * FROM orders;  -- View orders
# \q                     -- Exit
```

---

## Troubleshooting

### Port Already in Use
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual PID)
taskkill /PID <PID> /F
```

### Reset Everything
```powershell
# Stop all containers
docker-compose down -v

# Remove all cafe-related containers
docker ps -a | findstr cafe | ForEach-Object { docker rm -f $_.Split()[0] }

# Remove all cafe-related images
docker images | findstr cafe | ForEach-Object { docker rmi -f $_.Split()[2] }

# Fresh start
docker-compose up --build
```

### Database Connection Issues
```powershell
# Restart database
docker-compose restart postgres

# Check database logs
docker-compose logs postgres

# Recreate database
docker-compose down postgres
docker-compose up -d postgres
```

### Service Not Starting
```powershell
# View service logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>

# Rebuild and restart
docker-compose up --build <service-name>
```

---

## Quick Reference

| Service | Port | URL |
|---------|------|-----|
| Frontend | 5000 | http://localhost:5000 |
| Kitchen UI | 5000 | http://localhost:5000/kitchen |
| Display Board | 5000 | http://localhost:5000/display |
| Order API | 5001 | http://localhost:5001 |
| Kitchen API | 5002 | http://localhost:5002 |
| PostgreSQL | 5432 | localhost:5432 |

---

## Environment Variables

### Order Service
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cafe_db
DB_USER=postgres
DB_PASSWORD=cafe123
```

### Kitchen Service
```
ORDER_SERVICE_URL=http://localhost:5001
```

### Frontend
```
ORDER_SERVICE_URL=http://localhost:5001
KITCHEN_SERVICE_URL=http://localhost:5002
```

---

**That's it! Your café is ready to serve.** ☕
