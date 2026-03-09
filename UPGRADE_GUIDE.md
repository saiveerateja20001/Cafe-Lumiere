# Upgrade Guide: v1.0 to v2.0

## Overview

Café Lumière v2.0 is a backward-compatible enhancement of v1.0 with improved performance, stability, and error handling.

## Key Changes in v2.0

### Performance Improvements
- Optimized database query performance
- Enhanced connection pooling
- Improved response times for order operations

### Stability Enhancements
- Better error handling and recovery
- Improved health checks
- More robust retry logic for service communication

### UI/UX Improvements
- Faster page load times
- Improved UI responsiveness
- Better status updates

## Migration Path

### Option 1: Side-by-Side (Recommended for Testing)

Both v1.0 and v2.0 can run simultaneously with different ports:

```bash
# v1.0 - Original (ports 5000, 5001, 5002)
cd cafe/
docker-compose up --build

# v2.0 - New version (in different terminal/instance)
cd cafe-v2.0/
docker-compose up --build
```

### Option 2: Direct Upgrade

1. Stop v1.0 services:
```bash
cd cafe/
docker-compose down
```

2. Start v2.0 services:
```bash
cd cafe-v2.0/
docker-compose up --build
```

**Note:** Database data is preserved as PostgreSQL volume persists data independently.

## Compatibility

- ✅ All existing APIs remain compatible
- ✅ Database schema unchanged
- ✅ No data migration required
- ✅ Same Docker and Python dependencies

## Testing v2.0

Access the application at: `http://localhost:5000`

### Verify Version
Check the version information:
- Look for "v2.0" in headers and documentation
- Services report version 2.0 in their configuration

## Rollback to v1.0

If needed, simply switch back:

```bash
cd cafe-v2.0/
docker-compose down

cd cafe/
docker-compose up
```

## Support

For issues or questions, refer to:
- [Architecture Documentation](cafe-v2.0/ARCHITECTURE.md)
- [Setup Guide](cafe-v2.0/SETUP.md)

---

**Version:** 2.0
**Release Date:** 2026-03-09
