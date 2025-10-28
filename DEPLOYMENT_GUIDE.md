# Data Platform - Deployment Guide

Complete guide for deploying the Data Platform with React Dashboard.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Service Configuration](#service-configuration)
5. [Accessing Services](#accessing-services)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

## 🚀 Quick Start

### Windows

```bash
cd c:\Users\TUF\Desktop\docker
start.bat
```

### Linux/Mac

```bash
cd ~/docker
chmod +x start.sh
./start.sh
```

### Docker Compose (All Platforms)

```bash
docker-compose up -d
```

## 💻 System Requirements

### Minimum Requirements

- **CPU**: 4 cores
- **RAM**: 8 GB
- **Disk**: 20 GB free space
- **Docker**: 20.10+
- **Docker Compose**: 1.29+

### Recommended Requirements

- **CPU**: 8 cores
- **RAM**: 16 GB
- **Disk**: 50 GB free space
- **Docker**: Latest version
- **Docker Compose**: Latest version

### Network Requirements

- Ports 3000-3001 (Frontend, Grafana)
- Port 5432 (PostgreSQL)
- Port 6379 (Redis)
- Port 8000 (API)
- Port 8080 (Airflow)
- Port 8081 (Adminer)
- Port 8888 (Jupyter)
- Port 9000-9001 (MinIO)

## 📦 Installation Steps

### 1. Prerequisites Installation

#### Windows

Download and install:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/download/win)

#### Linux (Ubuntu/Debian)

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### macOS

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Docker Desktop
brew install --cask docker

# Start Docker
open /Applications/Docker.app
```

### 2. Clone/Download Project

```bash
# Clone from repository
git clone <repository-url> data-platform
cd data-platform

# Or download and extract ZIP file
cd data-platform
```

### 3. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# PostgreSQL
POSTGRES_USER=datauser
POSTGRES_PASSWORD=datapass123
POSTGRES_DB=datawarehouse

# Grafana
GF_SECURITY_ADMIN_PASSWORD=admin

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

# API
DB_HOST=postgres
DB_USER=datauser
DB_PASSWORD=datapass123

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### 4. Build and Start Services

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Initialize Database

```bash
# Load sample data
docker-compose exec postgres python /scripts/load_sample_data.py

# Or manually run SQL
docker-compose exec postgres psql -U datauser -d datawarehouse -f /init-scripts/postgres-init.sql
```

## ⚙️ Service Configuration

### PostgreSQL

**Connection Details:**
- Host: `localhost` or `postgres` (from Docker)
- Port: `5432`
- User: `datauser`
- Password: `datapass123`
- Database: `datawarehouse`

**Volumes:**
- `postgres_data:/var/lib/postgresql/data`

### Apache Airflow

**Configuration:**
- Executor: LocalExecutor
- DAGs folder: `/opt/airflow/dags`
- Logs folder: `/opt/airflow/logs`

**Environment Variables:**
```env
AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
AIRFLOW__CORE__LOAD_EXAMPLES=false
AIRFLOW__CORE__EXECUTOR=LocalExecutor
```

### React Frontend

**Configuration:**
- Port: `3000`
- API URL: `http://localhost:8000`

**Build Configuration:**
- Node.js: 18-alpine
- Build tool: Create React App
- CSS Framework: Tailwind CSS

### Flask API

**Configuration:**
- Port: `8000`
- Workers: 4 (Gunicorn)
- Timeout: 120 seconds

**Database Connection:**
- Connects to PostgreSQL
- Connection pooling enabled
- CORS enabled for frontend

### Grafana

**Configuration:**
- Port: `3001` (changed from 3000 to avoid conflict)
- Admin User: `admin`
- Admin Password: `admin`

**Data Sources:**
- PostgreSQL (configured)

### MinIO

**Configuration:**
- API Port: `9000`
- Console Port: `9001`
- Root User: `minioadmin`
- Root Password: `minioadmin123`

### Redis

**Configuration:**
- Port: `6379`
- No authentication (default)

### Jupyter

**Configuration:**
- Port: `8888`
- No token/password required
- Lab interface enabled

### Adminer

**Configuration:**
- Port: `8081`
- Database: PostgreSQL

## 🌐 Accessing Services

### Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| **React Dashboard** | http://localhost:3000 | - |
| **API Backend** | http://localhost:8000 | - |
| **Airflow** | http://localhost:8080 | admin / admin |
| **Grafana** | http://localhost:3001 | admin / admin |
| **Jupyter** | http://localhost:8888 | - |
| **Adminer** | http://localhost:8081 | datauser / datapass123 |
| **MinIO Console** | http://localhost:9001 | minioadmin / minioadmin123 |
| **PostgreSQL** | localhost:5432 | datauser / datapass123 |
| **Redis** | localhost:6379 | - |

### First Time Setup

1. **Access React Dashboard**
   - Open http://localhost:3000
   - Dashboard loads with mock data
   - Navigate through different sections

2. **Configure Grafana**
   - Open http://localhost:3001
   - Login with admin/admin
   - Add PostgreSQL data source
   - Import dashboards

3. **Setup Airflow**
   - Open http://localhost:8080
   - Login with admin/admin
   - Enable DAGs
   - Trigger pipelines

4. **Load Sample Data**
   - Run: `docker-compose exec postgres python /scripts/load_sample_data.py`
   - Or use Adminer to import data

## 🔧 Troubleshooting

### Services Won't Start

```bash
# Check Docker status
docker ps -a

# View logs
docker-compose logs

# Restart services
docker-compose restart

# Full reset
docker-compose down -v
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

### Database Connection Error

```bash
# Check PostgreSQL
docker-compose exec postgres pg_isready -U datauser

# Check logs
docker-compose logs postgres

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
# Check resource usage
docker stats

# Increase Docker resources
# Docker Desktop → Preferences → Resources
# Set CPU: 4+, Memory: 8GB+
```

## 🚀 Production Deployment

### Pre-Production Checklist

- [ ] Change all default passwords
- [ ] Enable SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Configure monitoring and alerts
- [ ] Set up log aggregation
- [ ] Configure database replication
- [ ] Test disaster recovery

### Security Hardening

1. **Change Default Passwords**
   ```env
   POSTGRES_PASSWORD=<strong-password>
   GF_SECURITY_ADMIN_PASSWORD=<strong-password>
   MINIO_ROOT_PASSWORD=<strong-password>
   ```

2. **Enable SSL/TLS**
   - Configure reverse proxy (Nginx/Apache)
   - Install SSL certificates
   - Update service URLs

3. **Network Security**
   - Use private networks
   - Configure firewall rules
   - Implement VPN access

4. **Database Security**
   - Enable authentication
   - Configure user roles
   - Enable encryption at rest

### Scaling Considerations

1. **Horizontal Scaling**
   - Use Kubernetes instead of Docker Compose
   - Deploy multiple API instances
   - Use load balancer

2. **Database Scaling**
   - Implement read replicas
   - Configure connection pooling
   - Optimize queries

3. **Caching**
   - Use Redis cluster
   - Implement cache invalidation
   - Monitor cache hit rates

### Monitoring and Logging

1. **Set Up Monitoring**
   - Configure Prometheus
   - Set up Grafana dashboards
   - Configure alerts

2. **Centralized Logging**
   - Use ELK stack or similar
   - Aggregate logs from all services
   - Set up log retention policies

3. **Performance Monitoring**
   - Monitor database performance
   - Track API response times
   - Monitor resource usage

### Backup and Recovery

1. **Database Backups**
   ```bash
   docker-compose exec postgres pg_dump -U datauser datawarehouse > backup.sql
   ```

2. **Volume Backups**
   ```bash
   docker run --rm -v postgres_data:/data -v $(pwd):/backup \
     alpine tar czf /backup/postgres_backup.tar.gz /data
   ```

3. **Automated Backups**
   - Configure cron jobs
   - Use backup services
   - Test recovery procedures

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📞 Support

For issues or questions:

1. Check logs: `docker-compose logs`
2. Review troubleshooting section
3. Check service health: `docker-compose ps`
4. Consult documentation

---

**Last Updated**: 2024
**Version**: 1.0.0
