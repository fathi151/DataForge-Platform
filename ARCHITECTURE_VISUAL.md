# Data Platform - Visual Architecture

## 🏗️ Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA PLATFORM ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────┐  │
│  │  React Dashboard     │  │  Grafana Dashboards  │  │  Jupyter Notebooks│ │
│  │  (Port 3000)         │  │  (Port 3001)         │  │  (Port 8888)      │ │
│  │                      │  │                      │  │                   │ │
│  │  • Dashboard         │  │  • Real-time charts  │  │  • Data analysis  │ │
│  │  • Data Quality      │  │  • Alerts            │  │  • Exploration    │ │
│  │  • Pipelines         │  │  • Monitoring        │  │  • Visualization  │ │
│  │  • Services          │  │  • Custom panels     │  │  • ML models      │ │
│  │  • Analytics         │  │                      │  │                   │ │
│  └──────────────────────┘  └──────────────────────┘  └───────────────��──┘  │
│                                                                               │
│  ┌──────────────────────┐  ┌──────────────────────┐                         │
│  │  Adminer             │  │  MinIO Console       │                         │
│  │  (Port 8081)         │  │  (Port 9001)         │                         │
│  │                      │  │                      │                         │
│  │  • DB Management     │  │  • Object Storage    │                         │
│  │  • Query Editor      │  │  • File Management   │                         │
│  │  • Data Import/Export│  │  • Bucket Management │                         │
│  └──────────────────────┘  └──────────────────────┘                         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↑
                                    │ HTTP/REST
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                           API LAYER                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Flask API Backend (Port 8000)                                       │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ Endpoints:                                                     │ │   │
│  │  │ • /api/dashboard/stats                                         │ │   │
│  │  │ • /api/data-quality/metrics                                    │ │   │
│  │  │ • /api/pipelines/status                                        │ │   │
│  │  │ • /api/services/status                                         │ │   │
│  │  │ • /api/analytics/revenue                                       │ │   │
│  │  │ • /api/analytics/customers                                     │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  │  Features:                                                           │   │
│  │  • CORS enabled                                                      │   │
│  │  • Health checks                                                     │   │
│  │  • Error handling                                                    │   │
│  │  • Database connection pooling                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↑
                                    │ SQL
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Apache Airflow (Port 8080)                                          │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ DAGs:                                                          │ │   │
│  │  │ • etl_pipeline.py (Daily at 2 AM)                             │ │   │
│  │  │ • maintenance_pipeline.py (Weekly Sunday 3 AM)                │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  │  Features:                                                           │   │
│  │  • Task scheduling                                                   │   │
│  │  • Dependency management                                             │   │
│  │  • Error handling & retries                                          │   │
│  │  • Monitoring & logging                                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↑
                                    │ SQL
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROCESSING LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PostgreSQL Data Warehouse (Port 5432)                               │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ RAW DATA LAYER                                                 │ │   │
│  │  │ • customers (5,000 records)                                    │ │   │
│  │  │ • orders (45,000 records)                                      │ │   │
│  │  │ • products (2,000 records)                                     │ │   │
���  │  │ • order_items (73,000 records)                                 │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  │  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ STAGING LAYER                                                  │ │   │
│  │  │ • customers_staging (cleaned & validated)                      │ │   │
│  │  │ • orders_staging (cleaned & validated)                         │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  ���  ┌────────────────────────────────────────────────────────────────┐ │   │
│  │  │ ANALYTICS LAYER                                                │ │   │
│  │  │ • customer_metrics (aggregated KPIs)                           │ │   │
│  │  │ • daily_sales (daily aggregates)                               │ │   │
│  │  └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↑
                                    │ Cache/Session
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CACHING LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────┐  ┌──────────────────────┐                         │
│  │  Redis Cache         │  │  MinIO Storage       │                         │
│  │  (Port 6379)         │  │  (Port 9000)         │                         │
│  │                      │  │                      │                         │
│  │  • Query cache       │  │  • Raw data files    │                         │
│  │  • Session storage   │  │  • Processed data    │                         │
│  │  • Temporary data    │  │  • Backups           │                         │
│  │  • Rate limiting     │  │  • Archives          │                         │
│  └──────────────────────┘  └──────────────────────┘                         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW                                          │
└─────────────────────────────────────────────────────────────────────────────┘

INGESTION
    │
    ├─→ External APIs
    ├─→ CSV/JSON Files
    ├─→ Databases
    └─→ Streaming Sources
         │
         ↓
    ┌─────────────────────┐
    │  MinIO Storage      │
    │  (Raw Data)         │
    └─────────────────────┘
         │
         ↓
    ┌─────────────────────┐
    │  Airflow DAG        │
    │  (Orchestration)    │
    └─────────────────────┘
         │
         ├─→ EXTRACT
         │   └─→ Read from MinIO
         │
         ├─→ TRANSFORM
         │   ├─→ Clean data
         │   ├─→ Validate
         │   └─→ Enrich
         │
         └─→ LOAD
             ├─→ raw_data schema
             ├─→ staging schema
             └─→ analytics schema
                  │
                  ↓
         ┌─────────────────────┐
         │  PostgreSQL         │
         │  (Data Warehouse)   │
         └─────────────────────┘
              │
              ├─→ Redis Cache
              │
              ├─→ Flask API
              │   └─→ React Dashboard
              │
              ├─→ Grafana
              │   └─→ Dashboards
              │
              └─→ Jupyter
                  └─→ Analysis
```

## 🌐 Network Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Docker Network: data-platform                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Frontend Container                                                   │   │
│  │ • Service: frontend                                                  │   │
│  │ • Port: 3000                                                         │   │
│  │ • Image: node:18-alpine                                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────���───────────────────────────┐   │
│  │ API Container                                                        │   │
│  │ • Service: api                                                       │   │
│  │ • Port: 8000                                                         │   │
│  │ • Image: python:3.11-slim                                            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ PostgreSQL Container                                                 │   │
│  │ • Service: postgres                                                  │   │
│  │ • Port: 5432                                                         │   │
│  │ • Image: postgres:15-alpine                                          │   │
│  │ • Volume: postgres_data                                              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Airflow Container                                                    │   │
│  │ • Service: airflow-webserver                                         │   │
│  │ • Port: 8080                                                         │   │
│  │ • Image: apache/airflow:2.7.0                                        │   │
│  │ • Volumes: dags, logs, plugins                                       │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Grafana Container                                                    │   │
│  │ • Service: grafana                                                   │   │
│  │ • Port: 3001                                                         │   │
│  │ • Image: grafana/grafana:10.0.0                                      │   │
│  │ • Volume: grafana_data                                               │   │
│  └───────────────────��──────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Jupyter Container                                                    │   │
│  │ • Service: jupyter                                                   │   │
│  │ • Port: 8888                                                         │   │
│  │ • Image: jupyter/datascience-notebook                                │   │
│  │ • Volumes: notebooks, data                                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌───────────────────────────────────────���──────────────────────────────┐   │
│  │ MinIO Container                                                      │   │
│  │ • Service: minio                                                     │   │
│  │ • Ports: 9000, 9001                                                  │   │
│  │ • Image: minio/minio                                                 │   │
│  │ • Volume: minio_data                                                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌────────────────────────────────────────────────────────────────��─────┐   │
│  │ Redis Container                                                      │   │
│  │ • Service: redis                                                     │   │
│  │ • Port: 6379                                                         │   │
│  │ • Image: redis:7-alpine                                              │   │
│  │ • Volume: redis_data                                                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ Adminer Container                                                    │   │
│  │ • Service: adminer                                                   │   │
│  │ • Port: 8081                                                         │   │
│  │ • Image: adminer                                                     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPONENT INTERACTIONS                                    │
└────────────────────────────────────────���────────────────────────────────────┘

React Dashboard (3000)
    │
    ├─→ HTTP GET /api/dashboard/stats
    │   └─→ Flask API (8000)
    │       └─→ SELECT * FROM analytics.*
    │           └─→ PostgreSQL (5432)
    │
    ├─→ HTTP GET /api/data-quality/metrics
    │   └─→ Flask API (8000)
    │       └─→ SELECT COUNT(*) FROM raw_data.*
    │           └─→ PostgreSQL (5432)
    │
    ├─→ HTTP GET /api/pipelines/status
    │   └─→ Flask API (8000)
    │       └─→ Airflow API (8080)
    │
    ├─→ HTTP GET /api/services/status
    │   └─→ Flask API (8000)
    │       └─→ Docker API
    │
    └─→ HTTP GET /api/analytics/revenue
        └─→ Flask API (8000)
            └─→ SELECT * FROM analytics.daily_sales
                └─→ PostgreSQL (5432)

Airflow (8080)
    │
    ├─→ ETL Pipeline
    │   ├─→ Extract from MinIO (9000)
    │   ├─→ Transform data
    │   └─→ Load to PostgreSQL (5432)
    │
    └─→ Maintenance Pipeline
        ├─→ VACUUM PostgreSQL (5432)
        ├─→ Quality checks
        └─→ Generate reports

Grafana (3001)
    │
    └��→ Data Source: PostgreSQL (5432)
        └─→ SELECT * FROM analytics.*

Jupyter (8888)
    │
    └─→ Connect to PostgreSQL (5432)
        └─→ Data analysis & visualization

MinIO (9000/9001)
    │
    └─→ Object Storage
        ├─→ Raw data files
        ├─→ Processed data
        └─→ Backups

Redis (6379)
    │
    ├─→ Cache queries
    ├─→ Session storage
    └─→ Rate limiting
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                                         │
└────────────────────────────────────────────────────────────────────────────��┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Layer 1: Network Security                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Docker network isolation (data-platform)                                   │
│ • Firewall rules (ports 3000-9001)                                           │
│ • VPN access (production)                                                    │
│ • SSL/TLS encryption (production)                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌────────────────��────────────────────────────────────────────────────────────┐
│ Layer 2: Application Security                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ • CORS configuration                                                         │
│ • Input validation                                                           │
│ • Error handling                                                             │
│ • Rate limiting (Redis)                                                      │
│ • API authentication (JWT - future)                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Layer 3: Database Security                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ • User authentication (datauser/datapass123)                                 │
│ • Role-based access control                                                  │
│ • Encryption at rest (production)                                            │
│ • Audit logging                                                              │
│ • Regular backups                                                            │
└────────────────────────────────────────────────��────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ Layer 4: Data Security                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Data classification                                                        │
│ • Sensitive data masking                                                     │
│ • Data retention policies                                                    │
│ • Secure deletion                                                            │
└───────────────────────────────────────────────────────────────────────���─────┘
```

## 📈 Scalability Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCALABILITY CONSIDERATIONS                                │
└─────────────────────────────────────────────────────────────────────────────┘

Current (Docker Compose)
    │
    ├─→ Single host deployment
    ├─→ LocalExecutor for Airflow
    ├─→ Single PostgreSQL instance
    └─→ Limited to host resources

Future (Kubernetes)
    │
    ├─→ Multi-node cluster
    ├─→ Distributed Airflow (CeleryExecutor)
    ├─→ PostgreSQL replication
    ├─→ Horizontal pod autoscaling
    ├─→ Load balancing
    └─→ Service mesh (Istio)

Scaling Strategies
    │
    ├─→ Horizontal Scaling
    │   ├─→ Multiple API instances
    │   ├─→ Multiple Airflow workers
    │   └─→ Database read replicas
    │
    ├─→ Vertical Scaling
    │   ├─→ Increase CPU/Memory
    │   ├─→ Larger database instance
    │   └─→ More cache memory
    │
    └─→ Performance Optimization
        ├─→ Query optimization
        ├─→ Indexing strategy
        ├─→ Caching strategy
        └─→ Connection pooling
```

---

**Last Updated:** 2024-01-06
**Version:** 1.0.0
