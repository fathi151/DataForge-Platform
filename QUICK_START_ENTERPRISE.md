# Quick Start: Enterprise Airflow Setup

## 🚀 Get Started in 5 Minutes

### Step 1: Start Docker Services

```bash
cd c:\Users\TUF\Desktop\docker
docker-compose up -d
```

Wait for all services to be healthy:
```bash
docker-compose ps
```

Expected output:
```
NAME                          STATUS
data-platform-postgres        Up (healthy)
data-platform-airflow         Up (healthy)
data-platform-grafana         Up (healthy)
data-platform-jupyter         Up (healthy)
data-platform-minio           Up (healthy)
data-platform-redis           Up (healthy)
data-platform-adminer         Up (healthy)
data-platform-api             Up (healthy)
data-platform-frontend        Up (healthy)
```

### Step 2: Access Airflow UI

Open browser: **http://localhost:8082**

Login:
- Username: `admin`
- Password: `admin`

### Step 3: Verify New Pipelines

You should see 3 new DAGs:

1. **data_preparation_pipeline** - Data cleaning & enrichment
2. **advanced_analytics_pipeline** - Dimensional modeling & metrics
3. **monitoring_pipeline** - Health & quality monitoring

### Step 4: Trigger Data Preparation Pipeline

1. Click on `data_preparation_pipeline`
2. Click "Trigger DAG" button
3. Watch the 7 stages execute:
   - Stage 1: Profiling & Discovery
   - Stage 2: Data Validation
   - Stage 3: Data Cleaning
   - Stage 4: Deduplication
   - Stage 5: Data Enrichment
   - Stage 6: Load to Staging
   - Stage 7: Cleanup

### Step 5: Trigger Analytics Pipeline

1. Click on `advanced_analytics_pipeline`
2. Click "Trigger DAG" button
3. Watch the 6 stages execute:
   - Stage 1: Build Dimension Tables
   - Stage 2: Build Fact Tables
   - Stage 3: Build Aggregate Tables
   - Stage 4: Build Advanced Metrics
   - Stage 5: Create Materialized Views
   - Stage 6: Quality Checks

### Step 6: Check Results in Database

```bash
# Connect to database
docker-compose exec postgres psql -U datauser -d datawarehouse

# View customer segments
SELECT segment, COUNT(*) FROM analytics.customer_segments GROUP BY segment;

# View daily sales
SELECT * FROM analytics.daily_sales ORDER BY sale_date DESC LIMIT 10;

# View customer metrics
SELECT * FROM analytics.customer_metrics LIMIT 5;
```

### Step 7: View in Grafana

Open browser: **http://localhost:3001**

Login:
- Username: `admin`
- Password: `admin`

Create dashboards to visualize:
- Daily sales trends
- Customer segments
- Product performance
- Pipeline health

---

## 📊 What Each Pipeline Does

### Data Preparation Pipeline

**Purpose:** Clean and prepare raw data

**7 Stages:**

| Stage | What it does | Output |
|-------|------------|--------|
| 1. Profiling | Analyzes data structure & quality | Profiling report |
| 2. Validation | Checks for critical issues | Validation results |
| 3. Cleaning | Trims, standardizes, handles nulls | Cleaned tables |
| 4. Deduplication | Removes duplicates | Deduplicated tables |
| 5. Enrichment | Adds calculated fields & segments | Enriched tables |
| 6. Load to Staging | Moves to staging layer | Staging tables |
| 7. Cleanup | Removes temporary tables | Clean database |

**Key Features:**
- ✅ Comprehensive data quality checks
- ✅ Automatic error handling
- ✅ Detailed logging
- ✅ XCom data sharing between tasks

### Advanced Analytics Pipeline

**Purpose:** Build enterprise analytics layer

**6 Stages:**

| Stage | What it does | Output |
|-------|------------|--------|
| 1. Dimensions | Build dim_customer, dim_product, dim_date | Dimension tables |
| 2. Facts | Build fact_sales table | Fact table |
| 3. Aggregates | Build metrics tables | Aggregate tables |
| 4. Advanced Metrics | RFM analysis, cohort analysis | Segment tables |
| 5. Materialized Views | Create fast query views | Materialized views |
| 6. Quality Checks | Validate analytics layer | Quality report |

**Key Features:**
- ✅ Slowly Changing Dimensions (SCD Type 2)
- ✅ Star schema design
- ✅ RFM customer segmentation
- ✅ Cohort retention analysis
- ✅ Materialized views for performance

### Monitoring Pipeline

**Purpose:** Monitor pipeline health & data quality

**Runs hourly and tracks:**
- Pipeline success rates
- Task performance
- Data quality metrics
- Data freshness
- Business metrics

---

## 🔍 Monitoring & Debugging

### View Pipeline Logs

```bash
# All logs
docker-compose logs -f airflow-webserver

# Specific pipeline
docker-compose logs -f airflow-webserver | grep data_preparation_pipeline

# Specific task
docker-compose exec airflow-webserver airflow tasks logs data_preparation_pipeline profile_raw_data 2024-01-01
```

### Check Data Quality

```bash
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT * FROM data_quality.dq_metrics 
WHERE check_date = CURRENT_DATE 
ORDER BY table_name, metric_name;
"
```

### View Customer Segments

```bash
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT 
    segment,
    COUNT(*) as customer_count,
    ROUND(AVG(lifetime_value), 2) as avg_ltv,
    ROUND(AVG(churn_risk), 2) as avg_churn_risk
FROM analytics.customer_segments
GROUP BY segment
ORDER BY customer_count DESC;
"
```

### Check Pipeline Performance

```bash
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT 
    dag_id,
    task_id,
    COUNT(*) as runs,
    ROUND(AVG(EXTRACT(EPOCH FROM (end_date - start_date))), 2) as avg_seconds,
    MAX(EXTRACT(EPOCH FROM (end_date - start_date))) as max_seconds
FROM airflow.task_instance
WHERE execution_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY dag_id, task_id
ORDER BY avg_seconds DESC
LIMIT 20;
"
```

---

## 🛠️ Common Tasks

### Manually Trigger a Pipeline

```bash
docker-compose exec airflow-webserver airflow dags trigger data_preparation_pipeline
```

### View DAG Structure

```bash
docker-compose exec airflow-webserver airflow dags show data_preparation_pipeline
```

### Reset a DAG

```bash
docker-compose exec airflow-webserver airflow dags delete data_preparation_pipeline
```

### View XCom Data (Inter-task Communication)

```bash
docker-compose exec airflow-webserver airflow tasks list data_preparation_pipeline
```

### Check Database Connection

```bash
docker-compose exec postgres pg_isready -U datauser
```

### Backup Database

```bash
docker-compose exec postgres pg_dump -U datauser datawarehouse > backup.sql
```

### Restore Database

```bash
docker-compose exec -T postgres psql -U datauser datawarehouse < backup.sql
```

---

## 📈 Key Metrics to Monitor

### Pipeline Health
- Success rate (target: > 95%)
- Average execution time
- Failed task count

### Data Quality
- Null values
- Duplicate records
- Invalid formats
- Data freshness

### Business Metrics
- Daily sales
- Customer count
- Average order value
- Customer segments

---

## 🚨 Troubleshooting

### Pipeline Won't Start

**Check if services are running:**
```bash
docker-compose ps
```

**Check Airflow logs:**
```bash
docker-compose logs airflow-webserver
```

**Restart Airflow:**
```bash
docker-compose restart airflow-webserver
```

### Database Connection Error

**Check PostgreSQL:**
```bash
docker-compose exec postgres pg_isready -U datauser
```

**Check connection string in DAG:**
```python
DB_CONFIG = {
    'host': 'postgres',  # Should be 'postgres' not 'localhost'
    'database': 'datawarehouse',
    'user': 'datauser',
    'password': 'datapass123'
}
```

### Out of Memory

**Increase Docker resources:**
- Docker Desktop → Preferences → Resources
- Increase CPU and Memory

**Or use batch processing in DAG:**
```python
BATCH_SIZE = 10000
for i in range(0, total_records, BATCH_SIZE):
    process_batch(data[i:i+BATCH_SIZE])
```

### Slow Queries

**Add indexes:**
```bash
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
CREATE INDEX idx_customers_email ON raw_data.customers(email);
CREATE INDEX idx_orders_date ON raw_data.orders(order_date);
"
```

**Check query performance:**
```bash
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
EXPLAIN ANALYZE
SELECT * FROM raw_data.customers WHERE email = 'test@example.com';
"
```

---

## 📚 Next Steps

1. **Customize for your data**
   - Modify data sources in DAGs
   - Add your business logic
   - Extend dimension tables

2. **Set up monitoring**
   - Create Grafana dashboards
   - Configure alerting rules
   - Set up email notifications

3. **Optimize performance**
   - Add indexes as needed
   - Tune query performance
   - Monitor resource usage

4. **Deploy to production**
   - Use Kubernetes instead of Docker Compose
   - Set up managed PostgreSQL
   - Configure backup & disaster recovery

5. **Document your setup**
   - Create runbooks
   - Document data lineage
   - Train your team

---

## 📖 Documentation

- **ENTERPRISE_AIRFLOW_GUIDE.md** - Comprehensive guide
- **DATA_WAREHOUSE_GUIDE.md** - Data warehouse architecture
- **ARCHITECTURE.md** - System architecture
- **README.md** - Project overview

---

## 🎯 Success Criteria

✅ All 3 pipelines running successfully  
✅ Data flowing through all 3 layers  
✅ Customer segments created  
✅ Dashboards displaying metrics  
✅ Monitoring alerts configured  
✅ Data quality checks passing  

---

## 💡 Tips & Tricks

### Use XCom for Data Sharing

```python
# Push data
task_instance.xcom_push(key='record_count', value=1000)

# Pull data
count = task_instance.xcom_pull(task_ids='previous_task', key='record_count')
```

### Use Task Groups for Organization

```python
with TaskGroup("stage_1_profiling", dag=dag) as profiling_group:
    task1 = PythonOperator(...)
    task2 = PythonOperator(...)
```

### Use Templating for Dynamic Values

```python
sql = """
    SELECT * FROM {{ params.table_name }}
    WHERE created_at >= '{{ ds }}'
"""
```

### Set Task Dependencies

```python
# Sequential
task1 >> task2 >> task3

# Parallel
[task1, task2, task3] >> task4
```

---

## 🔗 Useful Links

- Airflow UI: http://localhost:8082
- Grafana: http://localhost:3001
- Jupyter: http://localhost:8888
- Adminer: http://localhost:8081
- MinIO: http://localhost:9001
- API: http://localhost:8000
- Frontend: http://localhost:3000

---

## 📞 Support

For issues or questions:

1. Check the logs: `docker-compose logs`
2. Review the documentation
3. Check data quality metrics
4. Verify database connection

---

**Last Updated:** 2024  
**Version:** 1.0.0  
**Status:** Ready to Use
