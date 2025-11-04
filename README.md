# 🚀 DataForge Platform

A comprehensive, enterprise-grade data platform built with modern technologies for ETL orchestration, real-time analytics, and data quality monitoring.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Components](#components)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

DataForge Platform is an integrated data management solution that combines:

- **ETL Orchestration**: Apache Airflow for workflow automation
- **Real-time Analytics**: React-based interactive dashboard
- **Data Quality Monitoring**: Automated quality checks and reporting
- **REST API**: Comprehensive backend API for data access
- **Visualization**: Grafana dashboards for metrics monitoring
- **Data Storage**: PostgreSQL for reliable data persistence

## ✨ Features

### Core Features

- ✅ **Automated ETL Pipelines**: Schedule and monitor data workflows
- ✅ **Real-time Dashboard**: Live KPIs and metrics visualization
- ✅ **Data Quality Monitoring**: Automated quality checks and alerts
- ✅ **Pipeline Management**: Track execution status and performance
- ✅ **Service Monitoring**: System health and resource tracking
- ✅ **Business Analytics**: Revenue, customer, and product insights
- ✅ **REST API**: Complete backend API for integrations
- ✅ **Grafana Integration**: Advanced metrics visualization
- ✅ **Docker Support**: Containerized deployment ready

### Advanced Features

- 🔄 Advanced analytics pipelines
- 📊 Data preparation and transformation
- 🔧 Maintenance and optimization tasks
- 📈 Performance monitoring and reporting
- 🔐 Secure data handling
- 🚀 Scalable architecture

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
│              Dashboard | Analytics | Monitoring              │
└────────────────��───────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    REST API (Flask)                          │
│         /api/dashboard | /api/pipelines | /api/analytics    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Data Layer (PostgreSQL)                     │
│    Raw Data | Analytics | Metadata | Monitoring             │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Orchestration (Apache Airflow)                  │
│    ETL | Analytics | Maintenance | Monitoring Pipelines     │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Python 3.11+**: Core language
- **Flask**: REST API framework
- **Apache Airflow 2.7**: Workflow orchestration
- **PostgreSQL**: Primary database
- **SQLAlchemy**: ORM and database toolkit
- **Gunicorn**: WSGI application server

### Frontend
- **React 18**: UI framework
- **React Router**: Client-side routing
- **Recharts**: Data visualization
- **Tailwind CSS**: Styling framework
- **Lucide React**: Icon library
- **Axios**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Grafana**: Metrics visualization
- **Redis**: Caching and message broker

### Data Processing
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning
- **Plotly**: Interactive visualizations

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 16+ (for frontend development)
- PostgreSQL 13+ (if running locally)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/fathi151/DataForge-Platform.git
cd DataForge-Platform
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Access the services**
- Frontend Dashboard: http://localhost:3000
- API: http://localhost:8000
- Airflow UI: http://localhost:8080
- Grafana: http://localhost:3001
- PostgreSQL: localhost:5432

### Option 2: Local Development

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=datawarehouse
export DB_USER=datauser
export DB_PASSWORD=datapass123

# Run API
cd api
python app.py
```

#### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

#### Airflow Setup

```bash
# Initialize Airflow database
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

# Start Airflow scheduler
airflow scheduler

# Start Airflow webserver (in another terminal)
airflow webserver
```

## 📁 Project Structure

```
DataForge-Platform/
├── api/                          # Flask REST API
│   ├── app.py                   # Main application
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # API container
│   └── README.md                # API documentation
│
├── frontend/                     # React Dashboard
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── App.js               # Main app component
│   │   └── index.js             # Entry point
│   ├── package.json             # Node dependencies
│   ├── Dockerfile               # Frontend container
│   └── README.md                # Frontend documentation
│
├── dags/                         # Airflow DAGs
│   ├── etl_pipeline.py          # Main ETL pipeline
│   ├── advanced_analytics_pipeline.py
│   ├── data_preparation_pipeline.py
│   ├── maintenance_pipeline.py
│   ├── monitoring_pipeline.py
│   └── README.md                # DAGs documentation
│
├── config/                       # Configuration files
│   ├── docker-compose.yml       # Docker Compose config
│   ├── docker-compose.override.yml
│   └── Makefile                 # Build automation
│
├── setup/                        # Database setup scripts
│   ├── postgres-init.sql        # PostgreSQL initialization
│   ├── setup-enterprise-schema.sql
│   └── create-airflow-db.sql
│
├── scripts/                      # Utility scripts
│   ├── generate_realistic_data.py
│   ├── ingest_new_data.py
│   ├── load_data.py
│   └── README.md
│
├── grafana/                      # Grafana configuration
│   └── provisioning/
│       ├── dashboards/          # Dashboard definitions
│       └── datasources/         # Data source configs
│
├── notebooks/                    # Jupyter notebooks
│   ├── data_analysis.ipynb
│   └── README.md
│
├── data/                         # Data directory
│   └── README.md
│
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Main Docker Compose
└── README.md                     # This file
```

## 🔧 Components

### 1. REST API (Flask)

**Location**: `api/`

Provides RESTful endpoints for:
- Dashboard statistics
- Data quality metrics
- Pipeline status
- Service monitoring
- Business analytics

**Key Endpoints**:
- `GET /health` - Health check
- `GET /api/dashboard/stats` - Dashboard metrics
- `GET /api/data-quality/metrics` - Quality scores
- `GET /api/pipelines/status` - Pipeline status
- `GET /api/services/status` - Service health
- `GET /api/analytics/revenue` - Revenue analytics

See [API Documentation](#api-documentation) for complete details.

### 2. React Dashboard

**Location**: `frontend/`

Interactive web interface with:
- Real-time KPI dashboard
- Data quality monitoring
- Pipeline management
- Service monitoring
- Business analytics

**Pages**:
- Dashboard - Overview and KPIs
- Data Quality - Quality metrics and issues
- Pipelines - Pipeline execution tracking
- Services - System monitoring
- Analytics - Business metrics

### 3. Apache Airflow

**Location**: `dags/`

Orchestrates data workflows:
- **ETL Pipeline** - Daily data extraction, transformation, loading
- **Advanced Analytics** - Complex analytical computations
- **Data Preparation** - Data cleaning and preparation
- **Maintenance** - Database optimization and cleanup
- **Monitoring** - System health and performance checks

**Access**: http://localhost:8080

### 4. PostgreSQL Database

**Schemas**:
- `raw_data` - Raw ingested data
- `analytics` - Processed analytical data
- `metadata` - System metadata
- `monitoring` - Monitoring and audit logs

### 5. Grafana Dashboards

**Location**: `grafana/`

Advanced metrics visualization:
- System performance
- Pipeline execution metrics
- Data quality trends
- Service health status

**Access**: http://localhost:3001

## 📦 Installation

### Full Installation with Docker

```bash
# Clone repository
git clone https://github.com/fathi151/DataForge-Platform.git
cd DataForge-Platform

# Build images
docker-compose build

# Start services
docker-compose up -d

# Initialize database
docker-compose exec postgres psql -U datauser -d datawarehouse -f /docker-entrypoint-initdb.d/postgres-init.sql

# Create Airflow admin user
docker-compose exec airflow-webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### Manual Installation

#### 1. Database Setup

```bash
# Create PostgreSQL database
createdb -U postgres datawarehouse

# Run initialization scripts
psql -U datauser -d datawarehouse -f setup/postgres-init.sql
psql -U datauser -d datawarehouse -f setup/setup-enterprise-schema.sql
```

#### 2. Backend Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd api
python app.py
```

#### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

#### 4. Airflow Setup

```bash
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow scheduler &
airflow webserver
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=datawarehouse
DB_USER=datauser
DB_PASSWORD=datapass123

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
API_PORT=8000

# Airflow
AIRFLOW_HOME=/opt/airflow
AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
AIRFLOW__CORE__LOAD_EXAMPLES=False

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=production

# Grafana
GF_SECURITY_ADMIN_PASSWORD=admin
GF_SECURITY_ADMIN_USER=admin
```

### Docker Compose Configuration

Edit `config/docker-compose.yml` to customize:
- Port mappings
- Resource limits
- Volume mounts
- Environment variables

## 🎯 Usage

### Running ETL Pipelines

#### Via Airflow UI

1. Navigate to http://localhost:8080
2. Login with admin credentials
3. Find your DAG in the list
4. Click the play button to trigger

#### Via CLI

```bash
# List all DAGs
airflow dags list

# Trigger a DAG
airflow dags trigger etl_pipeline

# Test a DAG
airflow dags test etl_pipeline 2024-01-01

# View DAG details
airflow dags show etl_pipeline
```

### Accessing the Dashboard

1. Open http://localhost:3000
2. View real-time metrics and KPIs
3. Monitor pipeline execution
4. Check data quality scores
5. Analyze business metrics

### Loading Data

```bash
# Generate sample data
python scripts/generate_realistic_data.py

# Ingest data
python scripts/ingest_new_data.py

# Load data into warehouse
python scripts/load_data.py
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Health Check
```
GET /health
```

### Dashboard Endpoints

#### Get Dashboard Statistics
```
GET /api/dashboard/stats
```

**Response**:
```json
{
  "totalRecords": 125430,
  "activeUsers": 1234,
  "pipelineSuccess": 98.5,
  "avgResponseTime": 245,
  "dailySales": [...]
}
```

### Data Quality Endpoints

#### Get Quality Metrics
```
GET /api/data-quality/metrics
```

**Response**:
```json
{
  "overallScore": 98.5,
  "validRecords": 125000,
  "invalidRecords": 430,
  "tableQuality": [...]
}
```

### Pipeline Endpoints

#### Get Pipeline Status
```
GET /api/pipelines/status
```

**Response**:
```json
[
  {
    "id": 1,
    "name": "ETL Pipeline",
    "status": "running",
    "progress": 65,
    "lastRun": "2024-01-06T02:00:00",
    "nextRun": "2024-01-07T02:00:00"
  }
]
```

### Service Endpoints

#### Get Services Status
```
GET /api/services/status
```

#### Get System Statistics
```
GET /api/services/system-stats
```

### Analytics Endpoints

#### Get Revenue Analytics
```
GET /api/analytics/revenue
```

#### Get Customer Analytics
```
GET /api/analytics/customers
```

For complete API documentation, see [api/README.md](api/README.md)

## 🚀 Deployment

### Docker Compose Deployment

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

#### 1. Environment Setup

```bash
# Set production environment variables
export FLASK_ENV=production
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export GF_SECURITY_ADMIN_PASSWORD=<secure-password>
```

#### 2. Database Backup

```bash
# Backup PostgreSQL
pg_dump -U datauser datawarehouse > backup.sql

# Restore from backup
psql -U datauser datawarehouse < backup.sql
```

#### 3. SSL/TLS Configuration

Configure HTTPS in your reverse proxy (Nginx/Apache):

```nginx
server {
    listen 443 ssl;
    server_name dataforge.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

#### 4. Monitoring Setup

- Configure Grafana dashboards
- Set up alerting rules
- Enable audit logging
- Configure backup schedules

## 📊 Monitoring

### Grafana Dashboards

Access Grafana at http://localhost:3001

**Available Dashboards**:
- Platform Overview
- Pipeline Performance
- Data Quality Trends
- System Resources
- Service Health

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs api
docker-compose logs frontend
docker-compose logs airflow-webserver

# Follow logs in real-time
docker-compose logs -f
```

### Metrics

Monitor key metrics:
- Pipeline success rate
- Data quality score
- API response time
- Database performance
- System resource usage

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### Database Connection Error

```bash
# Check PostgreSQL status
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

#### Airflow DAG Not Appearing

```bash
# Check DAG syntax
airflow dags list

# Validate DAG file
python -m py_compile dags/my_dag.py

# Restart Airflow scheduler
docker-compose restart airflow-scheduler
```

#### Frontend Not Loading

```bash
# Clear browser cache
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build --no-cache frontend
```

### Debug Mode

Enable debug logging:

```bash
# Flask API
export FLASK_DEBUG=True

# Airflow
export AIRFLOW__LOGGING__LOGGING_LEVEL=DEBUG

# Docker Compose
docker-compose up --verbose
```

## 📖 Documentation

- [API Documentation](api/README.md)
- [Frontend Documentation](frontend/README.md)
- [DAGs Documentation](dags/README.md)
- [Scripts Documentation](scripts/README.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React
- Write tests for new features
- Update documentation
- Keep commits atomic and descriptive

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions:

1. Check existing [Issues](https://github.com/fathi151/DataForge-Platform/issues)
2. Create a new issue with detailed description
3. Include error logs and environment details
4. Provide steps to reproduce

## 🎉 Acknowledgments

- Apache Airflow community
- React community
- PostgreSQL team
- Grafana team
- All contributors

---

**Last Updated**: 2024
**Version**: 1.0.0
**Maintainer**: DataForge Team

For more information, visit the [GitHub Repository](https://github.com/fathi151/DataForge-Platform)
