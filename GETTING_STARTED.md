# Data Platform - Getting Started Guide

Welcome to the Data Platform! This guide will help you get up and running quickly.

## ⚡ 5-Minute Quick Start

### 1. Prerequisites Check

Ensure you have:
- Docker Desktop installed and running
- At least 8GB RAM available
- 20GB free disk space

### 2. Start the Platform

```bash
cd c:\Users\TUF\Desktop\docker
docker-compose up -d
```

### 3. Wait for Services to Start

```bash
# Check status (wait until all are "healthy")
docker-compose ps
```

### 4. Access the Dashboard

Open your browser and go to:
- **React Dashboard**: http://localhost:3000

That's it! You now have a fully functional data platform running.

## 🎯 What You Can Do Now

### View Real-time Metrics
- Open http://localhost:3000
- See KPIs, charts, and analytics
- Monitor data quality
- Track pipelines

### Access Other Services

| Service | URL | Purpose |
|---------|-----|---------|
| Airflow | http://localhost:8080 | Schedule & monitor ETL |
| Grafana | http://localhost:3001 | Create dashboards |
| Jupyter | http://localhost:8888 | Data analysis |
| Adminer | http://localhost:8081 | Database management |
| MinIO | http://localhost:9001 | Object storage |

### Load Sample Data

```bash
docker-compose exec postgres python /scripts/load_sample_data.py
```

Then refresh the dashboard to see data!

## 📊 Dashboard Tour

### Dashboard Page (Home)
- **KPI Cards**: Total records, active users, pipeline success, response time
- **Daily Sales Chart**: Revenue and order trends
- **Customer Metrics**: Distribution of customer types
- **Data Quality**: Overall quality score
- **Recent Activities**: Latest platform events

### Data Quality Page
- **Quality Score Trend**: Historical quality metrics
- **Table Quality**: Quality by table
- **Issues List**: Data quality problems with severity

### Pipelines Page
- **Pipeline Status**: Running, completed, or failed
- **Progress Tracking**: Task-by-task progress
- **Pipeline Controls**: Play, pause, restart buttons

### Services Page
- **System Resources**: CPU, memory, disk, network usage
- **Service Status**: Health of all services
- **Quick Links**: Direct access to all services

### Analytics Page
- **Revenue Trends**: Sales over time
- **Customer Segmentation**: Customer distribution
- **Product Performance**: Top products
- **Activity Patterns**: Hourly user activity

## 🔧 Common Tasks

### Check Service Status

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

### Access Database

**Via Web UI (Adminer):**
1. Go to http://localhost:8081
2. Enter credentials:
   - Server: postgres
   - User: datauser
   - Password: datapass123
   - Database: datawarehouse

**Via Command Line:**
```bash
docker-compose exec postgres psql -U datauser -d datawarehouse
```

### Query Data

```bash
# Show customers
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM raw_data.customers LIMIT 5;"

# Show orders
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM raw_data.orders LIMIT 5;"

# Show analytics
docker-compose exec postgres psql -U datauser -d datawarehouse -c "SELECT * FROM analytics.customer_metrics;"
```

### Restart a Service

```bash
docker-compose restart [service_name]

# Examples:
docker-compose restart frontend
docker-compose restart api
docker-compose restart postgres
```

### Stop Everything

```bash
docker-compose down
```

### Reset Everything (Delete All Data)

```bash
docker-compose down -v
```

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Restart Docker
# Docker Desktop → Restart

# Try again
docker-compose up -d
```

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :3000
kill -9 <PID>
```

### Dashboard Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### API Connection Error

```bash
# Check API logs
docker-compose logs api

# Test API
curl http://localhost:8000/health

# Rebuild API
docker-compose build --no-cache api
docker-compose up -d api
```

### Database Connection Error

```bash
# Check PostgreSQL
docker-compose logs postgres

# Test connection
docker-compose exec postgres pg_isready -U datauser

# Restart PostgreSQL
docker-compose restart postgres
```

### Out of Memory

```bash
# Check resource usage
docker stats

# Increase Docker resources:
# Docker Desktop → Preferences → Resources
# Set CPU: 4+, Memory: 8GB+
```

## 📚 Next Steps

### 1. Explore the Dashboard
- Navigate through all pages
- Understand the data structure
- Familiarize yourself with the UI

### 2. Load Sample Data
```bash
docker-compose exec postgres python /scripts/load_sample_data.py
```

### 3. Create Grafana Dashboards
- Go to http://localhost:3001
- Login with admin/admin
- Add PostgreSQL data source
- Create custom dashboards

### 4. Run Airflow Pipelines
- Go to http://localhost:8080
- Login with admin/admin
- Enable DAGs
- Trigger pipelines

### 5. Analyze Data with Jupyter
- Go to http://localhost:8888
- Open `work/data_analysis.ipynb`
- Run analysis notebooks

### 6. Manage Data with Adminer
- Go to http://localhost:8081
- Login with datauser/datapass123
- Browse and manage data

## 🎓 Learning Resources

### Understanding the Architecture
- Read [ARCHITECTURE.md](ARCHITECTURE.md)
- Review [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md)

### Deployment & Configuration
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### Component Documentation
- Frontend: [frontend/README.md](frontend/README.md)
- API: [api/README.md](api/README.md)

### Implementation Details
- Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

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

## 💡 Tips & Tricks

### Monitor Services in Real-time
```bash
watch docker-compose ps
```

### View All Logs at Once
```bash
docker-compose logs -f --tail=50
```

### Access Container Shell
```bash
docker-compose exec [service] /bin/bash
```

### Copy Files from Container
```bash
docker-compose cp [service]:/path/to/file ./local/path
```

### Copy Files to Container
```bash
docker-compose cp ./local/file [service]:/path/to/file
```

## 🚀 Performance Tips

### Optimize Docker Resources
- Allocate sufficient CPU and memory
- Use SSD for better performance
- Close unnecessary applications

### Database Performance
- Ensure PostgreSQL is healthy
- Monitor query performance
- Use indexes appropriately

### Frontend Performance
- Clear browser cache
- Use modern browser
- Check network latency

## �� Getting Help

### Check Documentation
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick answers
2. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed setup
3. [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md) - System design

### Check Logs
```bash
docker-compose logs [service_name]
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

### Common Issues

**Q: Dashboard shows no data**
A: Load sample data with: `docker-compose exec postgres python /scripts/load_sample_data.py`

**Q: Services won't start**
A: Check logs with: `docker-compose logs` and ensure ports are available

**Q: API returns errors**
A: Check API logs with: `docker-compose logs api` and verify database connection

**Q: Out of memory**
A: Increase Docker resources in Docker Desktop preferences

## 🎯 Success Checklist

- [ ] Docker Desktop is running
- [ ] All services are healthy (`docker-compose ps`)
- [ ] React Dashboard loads at http://localhost:3000
- [ ] API responds at http://localhost:8000/health
- [ ] Database is accessible
- [ ] Sample data is loaded
- [ ] You can see data in the dashboard

## 🎉 You're Ready!

Congratulations! You now have a fully functional data platform running. 

### What's Next?

1. **Explore**: Navigate through the dashboard and understand the data
2. **Customize**: Modify dashboards and create new visualizations
3. **Integrate**: Connect your own data sources
4. **Scale**: Deploy to production with Kubernetes
5. **Monitor**: Set up alerts and monitoring

## 📖 Documentation Map

```
Getting Started (You are here)
    ↓
Quick Reference → Common tasks & commands
    ↓
Deployment Guide → Detailed setup & configuration
    ↓
Architecture → System design & components
    ↓
Implementation Summary → Technical details
    ↓
Component Documentation → Frontend & API details
```

## 🤝 Contributing

Found an issue or have a suggestion? 
1. Check existing documentation
2. Review logs for errors
3. Test with fresh installation
4. Document your findings

## 📝 Version Info

- **Platform Version**: 1.0.0
- **Last Updated**: 2024-01-06
- **Status**: Production Ready

---

**Happy exploring! 🚀**

For detailed information, refer to the other documentation files in the project.
