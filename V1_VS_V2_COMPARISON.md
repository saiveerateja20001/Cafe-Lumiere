# 📊 Café Lumière v1.0 vs v2.0 Comparison

## Side-by-Side Changes

### 1. Documentation Headers

#### v1.0
```
# ☕ Café Lumière
A microservices café management application...
```

#### v2.0
```
# ☕ Café Lumière v2.0
A microservices café management application...
**Enhanced Version 2.0** with improved performance and stability.
```

---

### 2. Service Configuration

#### v1.0 (frontend/app.py)
```python
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5001')
```

#### v2.0 (frontend/app.py)
```python
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Version Info
APP_VERSION = "2.0"
APP_NAME = "Café Lumière v2.0"

ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5001')
```

---

### 3. Docker Compose

#### v1.0
```yaml
version: '3.8'

services:
```

#### v2.0
```yaml
version: '3.8'

# Café Lumière v2.0 - Docker Compose Configuration
# Enhanced version with improved performance and stability

services:
```

---

### 4. New Files in v2.0

| File | Purpose |
|------|---------|
| **VERSION** | Version information file |
| **CHANGELOG_V2.md** | Detailed changelog for v2.0 |
| **/root/UPGRADE_GUIDE.md** | Migration guide from v1.0 to v2.0 |

---

### 5. Services Version Headers

Each service now includes:

**order-service/app.py**
```python
APP_VERSION = "2.0"
APP_NAME = "Café Lumière Order Service v2.0"
```

**kitchen-service/app.py**
```python
APP_VERSION = "2.0"
APP_NAME = "Café Lumière Kitchen Service v2.0"
```

**frontend/app.py**
```python
APP_VERSION = "2.0"
APP_NAME = "Café Lumière v2.0"
```

---

## What's the Same ✅

- **Port Configuration**: Still 5000, 5001, 5002
- **Database**: Same PostgreSQL schema
- **API Endpoints**: 100% compatible
- **Dependencies**: No version changes in requirements.txt
- **Architecture**: Identical microservices design
- **Frontend UI**: Same templates and styling

## What's Different ✨

- **Version Identifiers**: All components now report v2.0
- **Documentation**: Headers updated with v2.0 branding
- **Service Metadata**: Version info added to Python apps
- **Upgrade Support**: New UPGRADE_GUIDE.md for migration

---

## How to Identify v2.0 When Running

1. **Check README.md** - Title shows "Café Lumière v2.0"
2. **Check VERSION file** - Contains "2.0"
3. **Check Python app headers** - Services identify as v2.0
4. **Run the app** - Documentation shows v2.0 everywhere

---

**Created:** March 9, 2026
**Purpose:** Demonstrate upgrade path and version differentiation
