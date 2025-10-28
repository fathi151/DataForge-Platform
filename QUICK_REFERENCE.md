# Data Platform - Quick Reference Guide

## 🚀 Quick Start Commands

### Start All Services
```bash
docker-compose up -d
```

### Stop All Services
```bash
docker-compose down
```

### View Service Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f api
docker-compose logs -f postgres
```

## 🌐 Service URLs

| Service | URL | User | Password |
|---------|-----|------|----------|
| React Dashboard | http://localhost:3000 | - | - |
| API Backend | http://localhost:8000 | - | - |
| Airflow | http://localhost:8080 | admin | admin |
| Grafana | http://localhost:3001 | admin | admin |
| Jupyter | http://localhost:8888 | - | - |
| Adminer | http://localhost:8081 | datauser | datapass123 |
| MinIO Console | http://localhost:9001 | minioadmin | minioadmin123 |

## 🗄️ Database Access

### Via Adminer (Web UI)
- URL: http://localhost:8081
- Server: postgres
- User: datauser
- Password: datapass123
- Database: datawarehouse

### Via Command Line
```bash
docker-compose exec postgres psql -U datauser -d datawarehouse
```

### Common SQL Queries
```sql
-- List all tables
\dt

-- Show customers
SELECT * FROM raw_data.customers LIMIT 5;

-- Show orders
SELECT * FROM raw_data.orders LIMIT 5;

-- Show analytics
SELECT * FROM analytics.customer_metrics;
```

## 📊 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Dashboard Stats
```bash
curl http://localhost:8000/api/dashboard/stats
```

### Data Quality
```bash
curl http://localhost:8000/api/data-quality/metrics
```

### Pipeline Status
```bash
curl http://localhost:8000/api/pipelines/status
```

### Services Status
```bash
curl http://localhost:8000/api/services/status
```

### System Stats
```bash
curl http://localhost:8000/api/services/system-stats
```

### Revenue Analytics
```bash
curl http://localhost:8000/api/analytics/revenue
```

### Customer Analytics
```bash
curl http://localhost:8000/api/analytics/customers
```

## 🔧 Service Management

### Restart a Service
```bash
docker-compose restart [service_name]
```

### Rebuild a Service
```bash
docker-compose build --no-cache [service_name]
docker-compose up -d [service_name]
```

### View Resource Usage
```bash
docker stats
```

### Clean Up
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup (careful!)
docker system prune -a
```

## 📁 Important Directories

| Directory | Purpose |
|-----------|---------|
| `frontend/` | React dashboard source code |
| `api/` | Flask API backend source code |
| `dags/` | Airflow DAG definitions |
| `notebooks/` | Jupyter notebooks |
| `scripts/` | Utility scripts |
| `init-scripts/` | Database initialization SQL |
| `grafana/` | Grafana configuration |
| `data/` | Data files |
| `logs/` | Application logs |

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### Database Connection Error
```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready -U datauser

# Restart PostgreSQL
docker-compose restart postgres
```

### Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### API Connection Issues
```bash
# Check API logs
docker-compose logs api

# Test API health
curl http://localhost:8000/health

# Rebuild API
docker-compose build --no-cache api
docker-compose up -d api
```

### Memory Issues
```bash
# Check memory usage
docker stats

# Increase Docker resources:
# Docker Desktop → Preferences → Resources
# Set CPU: 4+, Memory: 8GB+
```

## 📝 Configuration Files

### Environment Variables (.env)
```env
POSTGRES_USER=datauser
POSTGRES_PASSWORD=datapass123
POSTGRES_DB=datawarehouse
GF_SECURITY_ADMIN_PASSWORD=admin
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
```

### Docker Compose (docker-compose.yml)
- Service definitions
- Port mappings
- Volume configuration
- Network setup
- Environment variables

## 🔄 Common Workflows

### Load Sample Data
```bash
docker-compose exec postgres python /scripts/load_sample_data.py
```

### Backup Database
```bash
docker-compose exec postgres pg_dump -U datauser datawarehouse > backup.sql
```

### Restore Database
```bash
docker-compose exec postgres psql -U datauser datawarehouse < backup.sql
```

### View Airflow Logs
```bash
docker-compose logs -f airflow-webserver
```

### Access Jupyter
1. Open http://localhost:8888
2. Navigate to `work/` directory
3. Open `data_analysis.ipynb`

### Monitor Grafana
1. Open http://localhost:3001
2. Login with admin/admin
3. View pre-configured dashboards

## 📊 Dashboard Navigation

### React Dashboard (http://localhost:3000)

**Dashboard Page**
- Real-time KPIs
- Daily sales chart
- Customer metrics
- Data quality overview
- Recent activities

**Data Quality Page**
- Quality score trend
- Table quality scores
- Data quality issues
- Issue severity levels

**Pipelines Page**
- Pipeline status
- Progress tracking
- Task details
- Pipeline controls

**Services Page**
- System resource monitoring
- Service status indicators
- Service details table
- Quick links to services

**Analytics Page**
- Revenue trends
- Customer segmentation
- Product performance
- Hourly activity patterns

## 🔐 Security Notes

### Default Credentials (Change in Production!)
- PostgreSQL: datauser / datapass123
- Grafana: admin / admin
- MinIO: minioadmin / minioadmin123
- Airflow: admin / admin

### Security Recommendations
1. Change all default passwords
2. Enable SSL/TLS
3. Configure firewall rules
4. Use strong authentication
5. Enable audit logging
6. Regular backups
7. Monitor access logs

## 📚 Documentation Links

- [Main README](README.md)
- [Architecture](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- [Frontend README](frontend/README.md)
- [API README](api/README.md)
- [Usage Guide](GUIDE_UTILISATION.md)

## 🆘 Getting Help

### Check Logs
```bash
docker-compose logs [service_name]
```

### Check Service Status
```bash
docker-compose ps
```

### Test Connectivity
```bash
# Test API
curl http://localhost:8000/health

# Test Database
docker-compose exec postgres pg_isready -U datauser

# Test Frontend
curl http://localhost:3000
```

### Review Documentation
- Check DEPLOYMENT_GUIDE.md for detailed setup
- Check IMPLEMENTATION_SUMMARY.md for architecture
- Check service-specific README files

## 💡 Tips & Tricks

### Speed Up Builds
```bash
# Use --no-cache to rebuild from scratch
docker-compose build --no-cache

# Use cache for faster builds
docker-compose build
```

### Monitor in Real-time
```bash
# Watch service status
watch docker-compose ps

# Monitor resource usage
docker stats --no-stream=false
```

### Development Workflow
```bash
# Start services
docker-compose up -d

# Make changes to code
# (edit files in frontend/ or api/)

# Rebuild affected service
docker-compose build [service]

# Restart service
docker-compose up -d [service]

# Check logs
docker-compose logs -f [service]
```

### Production Checklist
- [ ] Change all default passwords
- [ ] Enable SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerts
- [ ] Configure backups
- [ ] Test disaster recovery
- [ ] Enable audit logging
- [ ] Configure log aggregation
- [ ] Set up health checks
- [ ] Document custom configurations

---

**Last Updated:** 2024-01-06
**Version:** 1.0.0
