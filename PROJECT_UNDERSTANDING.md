# Data Platform - Complete Project Understanding Guide

## 🎯 What is This Project?

This is a **complete, production-ready data platform demonstrator** that shows how to build a modern data infrastructure using open-source tools and Docker. It's designed to help you understand how real-world data platforms work.

Think of it as a **mini version of enterprise data platforms** like those used by companies like Netflix, Uber, or Airbnb.

## 🏗️ The Big Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR DATA PLATFORM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Users Access Dashboard → React Frontend (Port 3000)             │
│                              ↓                                    │
│                         Flask API (Port 8000)                    │
│                              ↓                                    │
│                      PostgreSQL Database (Port 5432)             │
│                              ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Data Layers:                                            │    │
│  │ • Raw Data (original data)                              │    │
│  │ • Staging (cleaned data)                                │    │
│  │ • Analytics (aggregated data)                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  Supporting Services:                                            │
│  • Apache Airflow (schedules data jobs)                          │
│  • Grafana (creates dashboards)                                  │
│  • Jupyter (data analysis)                                       │
│  • MinIO (stores files)                                          │
│  • Redis (caches data)                                           │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 How Data Flows Through the System

```
1. DATA INGESTION
   ↓
   Raw data comes in (customers, orders, products)
   ↓
   Stored in PostgreSQL raw_data schema
   
2. TRANSFORMATION (via Airflow)
   ↓
   Data is cleaned and validated
   ↓
   Moved to staging schema
   
3. AGGREGATION
   ↓
   Data is summarized and calculated
   ↓
   Moved to analytics schema
   
4. VISUALIZATION
   ↓
   React Dashboard fetches from API
   ↓
   API queries PostgreSQL
   ↓
   Beautiful charts and metrics displayed
```

## 📊 The Three Layers of Data

### Layer 1: RAW DATA (Original)
```
raw_data schema
├── customers (5,000 records)
│   ├── customer_id
│   ├─�� first_name
│   ├── last_name
│   ├── email
│   └── country
│
├── orders (45,000 records)
│   ├── order_id
│   ├── customer_id
│   ├── order_date
│   ├── total_amount
│   └── status
│
├── products (2,000 records)
│   ├── product_id
│   ├── product_name
│   ├── category
│   ├── price
│   └── stock_quantity
│
└── order_items (73,000 records)
    ├── order_item_id
    ├── order_id
    ├── product_id
    ├── quantity
    └── unit_price
```

### Layer 2: STAGING (Cleaned)
```
staging schema
├── customers_staging
│   └── Same as raw but cleaned/validated
│
└── orders_staging
    └── Same as raw but cleaned/validated
```

### Layer 3: ANALYTICS (Aggregated)
```
analytics schema
├── customer_metrics
│   ├── customer_id
│   ├── total_orders
│   ├── total_spent
│   ├── average_order_value
│   └── last_order_date
│
└── daily_sales
    ├── sale_date
    ├── total_sales
    ├── total_orders
    └── unique_customers
```

## 🎨 The React Dashboard (What Users See)

### 5 Main Pages:

#### 1. **Dashboard** (Home Page)
Shows the most important metrics at a glance:
- Total Records: 125,430
- Active Users: 1,234
- Pipeline Success: 98.5%
- Average Response Time: 245ms

Charts:
- Daily Sales (line chart showing revenue over 7 days)
- Customer Metrics (pie chart showing customer types)
- Data Quality (pie chart showing data health)
- Recent Activities (feed of recent events)

#### 2. **Data Quality**
Monitors how clean and reliable the data is:
- Overall Quality Score: 98.5%
- Quality Trend (line chart over 6 days)
- Table Quality Scores (bar chart)
- Data Issues List (with severity levels)

#### 3. **Pipelines**
Shows the status of automated data jobs:
- ETL Pipeline (running, 65% complete)
- Maintenance Pipeline (completed)
- Data Validation (failed)

Each pipeline shows:
- Status (running/completed/failed)
- Progress bar
- Individual tasks and their status
- Control buttons (play, pause, restart)

#### 4. **Services**
Monitors all the services running:
- System Resources (CPU, Memory, Disk, Network)
- Service Status Table (PostgreSQL, Airflow, Grafana, etc.)
- Quick Links to access each service

#### 5. **Analytics**
Business metrics and performance:
- Revenue Trends (area chart)
- Customer Segmentation (bar chart)
- Product Performance (bar chart)
- Hourly Activity (line chart)
- Top Products Table

## 🔌 How the Frontend Talks to the Backend

```
React Dashboard (Port 3000)
    │
    ├─→ HTTP GET /api/dashboard/stats
    │   └─→ Returns: KPIs, daily sales, customer metrics
    │
    ├─→ HTTP GET /api/data-quality/metrics
    │   └─→ Returns: Quality scores, issues
    │
    ├─→ HTTP GET /api/pipelines/status
    │   └─→ Returns: Pipeline status and progress
    │
    ├─→ HTTP GET /api/services/status
    │   └─→ Returns: Service health
    │
    └─→ HTTP GET /api/analytics/revenue
        └─→ Returns: Revenue data and trends
```

## 🛠️ The Backend (Flask API)

The Flask API is a simple Python web server that:
1. Receives requests from the React dashboard
2. Queries the PostgreSQL database
3. Returns data as JSON

Example:
```python
@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    # Connect to database
    # Run SQL queries
    # Return results as JSON
```

## 🗄️ The Database (PostgreSQL)

PostgreSQL is where all the data lives. It's organized into 3 schemas:

```
datawarehouse (database)
├── raw_data (schema)
│   ├── customers (table)
│   ├── orders (table)
│   ├── products (table)
│   └── order_items (table)
│
├── staging (schema)
│   ├── customers_staging (table)
│   └── orders_staging (table)
│
└── analytics (schema)
    ├── customer_metrics (table)
    └── daily_sales (table)
```

## ⚙️ The Orchestration (Apache Airflow)

Airflow is like a scheduler that runs data jobs automatically:

### ETL Pipeline (runs daily at 2 AM)
```
Extract → Transform → Load
   ↓         ↓          ↓
Read raw  Clean &    Write to
data      validate   analytics
```

### Maintenance Pipeline (runs weekly on Sunday at 3 AM)
```
Vacuum → Quality Check → Report
  ↓          ↓            ↓
Optimize  Validate    Generate
database  data        reports
```

## 🔄 The Complete Data Journey

```
1. DATA ARRIVES
   ↓
   Stored in raw_data schema (unchanged)
   
2. AIRFLOW TRIGGERS (Daily at 2 AM)
   ↓
   Extract: Read from raw_data
   ↓
   Transform: Clean, validate, enrich
   ↓
   Load: Write to staging, then analytics
   
3. DASHBOARD QUERIES
   ↓
   React asks API for data
   ↓
   API queries analytics schema
   ↓
   Results displayed in charts
   
4. USER SEES
   ↓
   Beautiful dashboard with insights
```

## 🌐 All Services and Their Ports

| Service | Port | Purpose | URL |
|---------|------|---------|-----|
| React Dashboard | 3000 | User interface | http://localhost:3000 |
| Flask API | 8000 | Data API | http://localhost:8000 |
| PostgreSQL | 5432 | Database | localhost:5432 |
| Apache Airflow | 8080 | Job scheduler | http://localhost:8080 |
| Grafana | 3001 | Dashboards | http://localhost:3001 |
| Jupyter | 8888 | Data analysis | http://localhost:8888 |
| Adminer | 8081 | DB management | http://localhost:8081 |
| MinIO | 9001 | File storage | http://localhost:9001 |
| Redis | 6379 | Cache | localhost:6379 |

## 🎯 Key Concepts Explained

### ETL (Extract, Transform, Load)
- **Extract**: Get data from source
- **Transform**: Clean, validate, enrich
- **Load**: Store in database

### Data Warehouse
A database optimized for analysis, organized in layers (raw, staging, analytics)

### Dashboard
A visual interface showing important metrics and charts

### API (Application Programming Interface)
A way for programs to talk to each other (React talks to Flask via API)

### Docker
A way to package applications so they run the same everywhere

### Orchestration
Automatically scheduling and running jobs (Airflow does this)

## 📈 What You Can Do With This

1. **Learn Data Engineering**
   - Understand ETL pipelines
   - Learn database design
   - See how data flows

2. **Build Your Own Platform**
   - Use as a template
   - Add your own data sources
   - Create custom dashboards

3. **Demonstrate to Others**
   - Show how data platforms work
   - Explain architecture
   - Run live demos

4. **Experiment**
   - Add new data sources
   - Create new dashboards
   - Test different tools

## 🚀 Quick Start (3 Steps)

### Step 1: Start Everything
```bash
docker-compose up -d
```

### Step 2: Wait for Services
```bash
docker-compose ps
# Wait until all show "healthy"
```

### Step 3: Open Dashboard
```
http://localhost:3000
```

That's it! You now have a fully functional data platform running.

## 📚 What Each Component Does

### React Frontend
- **What**: User interface
- **Why**: Beautiful, interactive way to view data
- **Technology**: React, Recharts, Tailwind CSS

### Flask API
- **What**: Data server
- **Why**: Provides data to frontend
- **Technology**: Flask, PostgreSQL driver

### PostgreSQL
- **What**: Data storage
- **Why**: Reliable, powerful database
- **Technology**: SQL database

### Apache Airflow
- **What**: Job scheduler
- **Why**: Automates data pipelines
- **Technology**: Python-based orchestration

### Grafana
- **What**: Dashboard builder
- **Why**: Create custom dashboards
- **Technology**: Visualization platform

### Jupyter
- **What**: Data analysis notebook
- **Why**: Explore and analyze data
- **Technology**: Python notebook

### MinIO
- **What**: File storage
- **Why**: Store raw data files
- **Technology**: S3-compatible storage

### Redis
- **What**: Cache
- **Why**: Speed up queries
- **Technology**: In-memory cache

## 🔐 Security Notes

### Default Credentials (Development Only!)
- PostgreSQL: datauser / datapass123
- Grafana: admin / admin
- Airflow: admin / admin
- MinIO: minioadmin / minioadmin123

⚠️ **CHANGE THESE IN PRODUCTION!**

## 🎓 Learning Path

1. **Start**: Run the project and explore the dashboard
2. **Understand**: Read the architecture documentation
3. **Explore**: Check the database with Adminer
4. **Experiment**: Load sample data and see it in dashboards
5. **Modify**: Change code and see what happens
6. **Deploy**: Deploy to production with Docker

## 🤔 Common Questions

**Q: Why 3 layers of data?**
A: Separation of concerns - raw data stays unchanged, staging is for cleaning, analytics is for reporting

**Q: Why use Airflow?**
A: Automates data jobs, handles failures, provides monitoring

**Q: Why React for frontend?**
A: Modern, responsive, fast, great for dashboards

**Q: Why PostgreSQL?**
A: Reliable, powerful, open-source, great for data warehousing

**Q: Can I use different tools?**
A: Yes! This is just an example. You can swap any component.

## 📊 Example Data Flow

```
Customer places order
    ↓
Order data arrives
    ↓
Stored in raw_data.orders
    ↓
Airflow runs at 2 AM
    ↓
Extract: Read raw_data.orders
    ↓
Transform: Validate, clean
    ↓
Load: Write to analytics.daily_sales
    ↓
Dashboard queries API
    ↓
API queries analytics.daily_sales
    ↓
Chart shows "Today's Sales: $5,000"
    ↓
User sees beautiful dashboard
```

## 🎯 Project Goals

✅ Demonstrate modern data platform architecture
✅ Show how to build with open-source tools
✅ Provide working example code
✅ Include comprehensive documentation
✅ Make it easy to understand and modify
✅ Production-ready setup

## 📝 Files You Should Know About

| File | Purpose |
|------|---------|
| docker-compose.yml | Defines all services |
| frontend/ | React dashboard code |
| api/ | Flask API code |
| dags/ | Airflow pipeline definitions |
| init-scripts/ | Database setup SQL |
| README.md | Project overview |
| ARCHITECTURE.md | System design |
| DEPLOYMENT_GUIDE.md | How to deploy |

## 🎉 You Now Understand!

You now have a complete understanding of:
- What this project does
- How all the pieces fit together
- What each component is for
- How data flows through the system
- How to use it

**Next Steps:**
1. Run the project: `docker-compose up -d`
2. Open dashboard: http://localhost:3000
3. Explore the services
4. Load sample data
5. Create your own dashboards

---

**Happy learning! 🚀**

This is a real, working data platform. Everything you see is production-ready code that you can learn from and build upon.
