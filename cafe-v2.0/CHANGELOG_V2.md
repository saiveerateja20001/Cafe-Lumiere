# Café Lumière v2.0 - Version 2.0 Summary

## What's Changed

### New Files
- **VERSION** - Version information file (2.0)
- **UPGRADE_GUIDE.md** - At root level, guides users on upgrading from v1.0 to v2.0

### Modified Files

#### Documentation
- **README.md** - Updated title and description for v2.0
- **SETUP.md** - Updated title to reflect v2.0
- **ARCHITECTURE.md** - Updated title and description to v2.0 Enhanced

#### Docker Configuration  
- **docker-compose.yml** - Added version comment header indicating v2.0

#### Services (Python Applications)
All service files now include version information:

1. **frontend/app.py**
   - Added `APP_VERSION = "2.0"`
   - Added `APP_NAME = "Café Lumière v2.0"`

2. **order-service/app.py**
   - Added `APP_VERSION = "2.0"`
   - Added `APP_NAME = "Café Lumière Order Service v2.0"`

3. **kitchen-service/app.py**
   - Added `APP_VERSION = "2.0"`
   - Added `APP_NAME = "Café Lumière Kitchen Service v2.0"`

### Root Level Changes
- **README.md** - Added section listing both v1.0 and v2.0 versions
- **UPGRADE_GUIDE.md** - New comprehensive upgrade documentation

## What Remained Unchanged

✅ All service architectures and port configurations
✅ Database schema and initialization scripts
✅ API endpoints and responses
✅ Docker Dockerfile configurations
✅ Requirements.txt dependencies
✅ Frontend templates and static files
✅ Kubernetes and Helm deployments

## Folder Structure

```
/workspaces/Cafe-Lumiere/
├── cafe/                 (v1.0 - Original)
├── cafe-v2.0/           (v2.0 - Enhanced - NEW)
├── README.md            (Updated)
├── UPGRADE_GUIDE.md     (NEW)
└── deploy-k8s.sh        (Original)
```

## Running v2.0

### Start v2.0 services:
```bash
cd cafe-v2.0/
docker-compose up --build
```

### Access the application:
- Frontend: http://localhost:5000
- Order Service: http://localhost:5001
- Kitchen Service: http://localhost:5002

## Version Detection

You can see v2.0 is running by:
1. Checking documentation headers (README.md, SETUP.md)
2. Looking at VERSION file
3. Service headers showing v2.0 in configuration
4. Docker container names prefixed with cafes

## Testing Both Versions

You can run both v1.0 and v2.0 simultaneously:

```bash
# Terminal 1: v1.0
cd cafe/
docker-compose up --build

# Terminal 2: v2.0  
cd cafe-v2.0/
docker-compose up --build
```

Both will use the same database volume, so orders are shared. To test in isolation, use separate database containers.

---

**Created:** 2026-03-09
**Version:** 2.0
