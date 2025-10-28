# Enterprise-Grade Airflow Setup Guide
## Deep Data Preparation & Advanced Analytics Like Big Companies

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Data Preparation Pipeline](#data-preparation-pipeline)
4. [Advanced Analytics Pipeline](#advanced-analytics-pipeline)
5. [Monitoring & Alerting](#monitoring--alerting)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## Overview

This guide shows you how to build an **enterprise-grade Airflow setup** with:

✅ **Deep Data Preparation** - 7-stage data cleaning pipeline  
✅ **Advanced Analytics** - Dimensional modeling & complex aggregations  
✅ **Data Quality** - Comprehensive validation & monitoring  
✅ **Scalability** - Production-ready architecture  
✅ **Observability** - Logging, metrics, and alerting  

### What Big Companies Do

1. **Data Preparation** - Multiple stages of cleaning, validation, deduplication
2. **Dimensional Modeling** - Star schema with dimensions and facts
3. **Advanced Metrics** - RFM analysis, cohort analysis, customer segmentation
4. **Data Quality** - Automated checks at every stage
5. **Monitoring** - Real-time dashboards and alerts
6. **Documentation** - Data lineage and metadata tracking

---

## Architecture

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAW DATA LAYER                                │
│  (Original data from sources)                                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│         DATA PREPARATION PIPELINE (7 Stages)                    │
├────────────────────────────���────────────────────────────────────┤
│ 1. Profiling & Discovery                                        │
│ 2. Data Validation                                              │
│ 3. Data Cleaning                                                │
│ 4. Deduplication                                                │
│ 5. Data Enrichment                                              │
│ 6. Load to Staging                                              │
│ 7. Cleanup                                                      │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STAGING LAYER                                 │
│  (Cleaned, validated, enriched data)                            │
└────────────────────────────────────────────────────���────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│      ADVANCED ANALYTICS PIPELINE (6 Stages)                     │
├─────────────────────────────────────────────────────────────────┤
│ 1. Build Dimension Tables (SCD Type 2)                          │
│ 2. Build Fact Tables                                            │
│ 3. Build Aggregate Tables                                       │
│ 4. Build Advanced Metrics (RFM, Cohorts)                        │
│ 5. Create Materialized Views                                    │
│ 6. Quality Checks                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────��────────────────┐
│                   ANALYTICS LAYER                                │
│  (Dimensional model, aggregates, metrics)                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                                  │
│  (Dashboards, Reports, APIs)                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Orchestration** | Apache Airflow 2.7 | DAG scheduling & monitoring |
| **Data Warehouse** | PostgreSQL 15 | OLAP database |
| **Processing** | Python | Data transformation logic |
| **Caching** | Redis | Query result caching |
| **Visualization** | Grafana | Dashboards & monitoring |
| **Monitoring** | Prometheus | Metrics collection |

---

## Data Preparation Pipeline

### Overview

The **data_preparation_pipeline.py** implements a 7-stage data cleaning process:

```
Stage 1: Profiling & Discovery
    ↓ (Understand data structure & quality)
Stage 2: Data Validation
    ↓ (Check for critical issues)
Stage 3: Data Cleaning
    ↓ (Trim, standardize, handle nulls)
Stage 4: Deduplication
    ↓ (Remove duplicates)
Stage 5: Data Enrichment
    ↓ (Add calculated fields & segments)
Stage 6: Load to Staging
    ↓ (Move to staging layer)
Stage 7: Cleanup
    (Remove temporary tables)
```

### Stage 1: Profiling & Discovery

**What it does:**
- Analyzes data structure and quality
- Counts records, nulls, duplicates
- Identifies data ranges and patterns

**Output:**
```json
{
  "customers": {
    "total_records": 5,
    "unique_customers": 5,
    "unique_emails": 5,
    "null_emails": 0,
    "unique_countries": 1
  },
  "orders": {
    "total_records": 5,
    "unique_orders": 5,
    "null_amounts": 0,
    "invalid_amounts": 0,
    "avg_amount": 835.98
  }
}
```

### Stage 2: Data Validation

**Checks performed:**
- ✅ No duplicate emails
- ✅ No orphaned orders (customer_id exists)
- ✅ No negative amounts
- ✅ No future dates
- ✅ Valid email formats
- ✅ No missing required fields

**Failure handling:**
- CRITICAL issues → Pipeline fails
- WARNINGS → Pipeline continues with logging

### Stage 3: Data Cleaning

**Transformations:**
```sql
-- Customers
TRIM(first_name)
LOWER(TRIM(email))
UPPER(TRIM(country))

-- Orders
ROUND(total_amount, 2)
UPPER(TRIM(status))
Filter: total_amount > 0 AND order_date <= TODAY

-- Products
TRIM(product_name)
UPPER(TRIM(category))
ROUND(price, 2)
GREATEST(stock_quantity, 0)  -- Handle negative stock
```

### Stage 4: Deduplication

**Strategy:**
- Group by unique key (email for customers, order_id for orders)
- Keep most recent record (ORDER BY updated_at DESC)
- Remove duplicates

**Example:**
```sql
SELECT DISTINCT ON (email)
    customer_id, first_name, last_name, email, ...
FROM temp_customers_cleaned
ORDER BY email, updated_at DESC
```

### Stage 5: Data Enrichment

**Customer Enrichment:**
```sql
-- Calculated fields
total_orders = COUNT(orders)
lifetime_value = SUM(order_amount)
avg_order_value = AVG(order_amount)
last_order_date = MAX(order_date)

-- Segmentation
customer_status = CASE
    WHEN COUNT(orders) = 0 THEN 'NEW'
    WHEN MAX(order_date) < 90 days ago THEN 'INACTIVE'
    WHEN MAX(order_date) < 30 days ago THEN 'AT_RISK'
    ELSE 'ACTIVE'
END

customer_segment = CASE
    WHEN lifetime_value > 5000 THEN 'VIP'
    WHEN lifetime_value > 1000 THEN 'PREMIUM'
    WHEN lifetime_value > 0 THEN 'REGULAR'
    ELSE 'PROSPECT'
END
```

**Order Enrichment:**
```sql
-- Time dimensions
order_year = EXTRACT(YEAR FROM order_date)
order_month = EXTRACT(MONTH FROM order_date)
order_quarter = EXTRACT(QUARTER FROM order_date)
order_day_of_week = TO_CHAR(order_date, 'Day')

-- Value categorization
order_value_category = CASE
    WHEN total_amount > 1000 THEN 'HIGH_VALUE'
    WHEN total_amount > 500 THEN 'MEDIUM_VALUE'
    ELSE 'LOW_VALUE'
END
```

### Stage 6: Load to Staging

**Actions:**
- Truncate staging tables
- Load cleaned & enriched data
- Log record counts

### Stage 7: Cleanup

**Actions:**
- Drop temporary tables
- Free up database space

### Running the Pipeline

```bash
# View in Airflow UI
http://localhost:8082

# Trigger manually
docker-compose exec airflow-webserver airflow dags trigger data_preparation_pipeline

# View logs
docker-compose logs -f airflow-webserver | grep data_preparation_pipeline

# Check XCom data (inter-task communication)
docker-compose exec airflow-webserver airflow tasks list data_preparation_pipeline
```

---

## Advanced Analytics Pipeline

### Overview

The **advanced_analytics_pipeline.py** implements enterprise analytics:

```
Stage 1: Build Dimension Tables
    ├── dim_customer (SCD Type 2)
    ├── dim_product
    └── dim_date
    ↓
Stage 2: Build Fact Tables
    └── fact_sales
    ↓
Stage 3: Build Aggregate Tables
    ├── customer_metrics
    ├── daily_sales
    ├── monthly_revenue
    └── product_performance
    ↓
Stage 4: Build Advanced Metrics
    ├── customer_segments (RFM)
    └── cohort_analysis
    ↓
Stage 5: Create Materialized Views
    ├── mv_customer_summary
    ├── mv_sales_by_category
    └── mv_top_customers
    ↓
Stage 6: Quality Checks
    (Validate analytics layer)
```

### Stage 1: Dimension Tables

#### dim_customer (Slowly Changing Dimension Type 2)

**Purpose:** Track customer changes over time

**Structure:**
```sql
customer_key (PK)
customer_id
first_name, last_name, email, phone, country
customer_segment, customer_status
effective_date, end_date
is_current (TRUE/FALSE)
```

**How it works:**
1. When customer data changes, old record marked as inactive
2. New record inserted with is_current = TRUE
3. Enables historical analysis

**Example:**
```
Customer 1 (John Doe) - effective 2024-01-01, end 2024-01-15, is_current FALSE
Customer 1 (John Smith) - effective 2024-01-15, end 9999-12-31, is_current TRUE
```

#### dim_product

**Purpose:** Product reference data

**Structure:**
```sql
product_key (PK)
product_id (UNIQUE)
product_name, category, price
is_active
created_at, updated_at
```

#### dim_date

**Purpose:** Time dimension for time-based analysis

**Structure:**
```sql
date_key (YYYYMMDD format)
date (DATE)
year, quarter, month, day
day_of_week, week_of_year
is_weekend, is_holiday
```

**Coverage:** 5 years back + 2 years forward

### Stage 2: Fact Tables

#### fact_sales

**Purpose:** Transactional sales data

**Structure:**
```sql
sales_key (PK)
customer_key (FK → dim_customer)
product_key (FK → dim_product)
date_key (FK → dim_date)
order_id
quantity, unit_price, total_amount
discount_amount, tax_amount, net_amount
created_at
```

**Grain:** One row per order item

### Stage 3: Aggregate Tables

#### customer_metrics

**Metrics:**
- total_orders
- total_spent (lifetime value)
- average_order_value
- last_order_date

#### daily_sales

**Metrics:**
- total_sales
- total_orders
- unique_customers

#### monthly_revenue

**Metrics:**
- total_revenue
- total_orders
- average_order_value
- unique_customers

#### product_performance

**Metrics:**
- total_sold (quantity)
- total_revenue
- average_price
- last_sold_date

### Stage 4: Advanced Metrics

#### Customer Segments (RFM Analysis)

**RFM = Recency, Frequency, Monetary**

**Segments:**
```
VIP_ACTIVE: lifetime_value > 5000 AND last_order < 30 days
VIP_AT_RISK: lifetime_value > 5000 AND last_order < 90 days
PREMIUM_ACTIVE: lifetime_value > 1000 AND last_order < 30 days
PREMIUM_AT_RISK: lifetime_value > 1000 AND last_order < 90 days
LOYAL_ACTIVE: frequency > 5 AND last_order < 30 days
LOYAL_AT_RISK: frequency > 5 AND last_order < 90 days
CHURNED: last_order > 180 days
AT_RISK: last_order > 90 days
NEW: frequency = 1
REGULAR: others
```

**Churn Risk Score:**
```
0.95 - last_order > 180 days (very high risk)
0.70 - last_order > 90 days (high risk)
0.40 - last_order > 60 days (medium risk)
0.10 - last_order > 30 days (low risk)
0.00 - last_order <= 30 days (no risk)
```

#### Cohort Analysis

**Purpose:** Track customer retention by cohort

**Structure:**
```sql
cohort_month (when customer first purchased)
cohort_age_months (months since first purchase)
customer_count (active customers in cohort)
revenue (revenue from cohort)
retention_rate (% of original cohort still active)
```

**Example:**
```
Cohort: 2024-01-01
  Month 0: 100 customers, $10,000 revenue, 100% retention
  Month 1: 85 customers, $8,500 revenue, 85% retention
  Month 2: 72 customers, $7,200 revenue, 72% retention
```

### Stage 5: Materialized Views

**mv_customer_summary**
- Fast customer lookup with aggregates
- Indexed by total_spent

**mv_sales_by_category**
- Sales metrics by product category
- Indexed by total_revenue

**mv_top_customers**
- Top 1000 customers by spending
- Ranked and indexed

### Stage 6: Quality Checks

**Checks:**
- ✅ Fact table not empty
- ✅ No null dimension keys
- ✅ No negative metrics
- ✅ Aggregate consistency

---

## Monitoring & Alerting

### Key Metrics to Monitor

```sql
-- Pipeline execution time
SELECT 
    dag_id,
    task_id,
    AVG(EXTRACT(EPOCH FROM (end_date - start_date))) as avg_duration_seconds
FROM airflow.task_instance
GROUP BY dag_id, task_id;

-- Data freshness
SELECT 
    'customers' as table_name,
    MAX(updated_at) as last_update,
    CURRENT_TIMESTAMP - MAX(updated_at) as age
FROM raw_data.customers;

-- Data quality metrics
SELECT 
    table_name,
    metric_name,
    metric_value,
    status
FROM data_quality.dq_metrics
WHERE check_date = CURRENT_DATE
ORDER BY table_name, metric_name;

-- Pipeline success rate
SELECT 
    dag_id,
    COUNT(*) as total_runs,
    SUM(CASE WHEN state = 'success' THEN 1 ELSE 0 END) as successful_runs,
    ROUND(100.0 * SUM(CASE WHEN state = 'success' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM airflow.dag_run
WHERE execution_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY dag_id;
```

### Grafana Dashboards

**Create dashboards for:**
1. Pipeline Health
   - Success/failure rates
   - Execution times
   - Data volumes

2. Data Quality
   - Validation results
   - Data freshness
   - Quality metrics

3. Business Metrics
   - Daily sales
   - Customer segments
   - Product performance

4. System Performance
   - Database query times
   - Cache hit rates
   - Resource utilization

### Alerting Rules

```yaml
# Alert if pipeline fails
- alert: AirflowPipelineFailed
  expr: airflow_dag_run_duration_seconds{state="failed"} > 0
  for: 5m
  annotations:
    summary: "Airflow pipeline {{ $labels.dag_id }} failed"

# Alert if data is stale
- alert: DataNotFresh
  expr: (time() - data_last_update_timestamp) > 86400
  for: 1h
  annotations:
    summary: "Data in {{ $labels.table_name }} is older than 24 hours"

# Alert if quality check fails
- alert: DataQualityFailed
  expr: data_quality_check_failed > 0
  for: 5m
  annotations:
    summary: "Data quality check failed for {{ $labels.table_name }}"
```

---

## Best Practices

### 1. Task Design

```python
# ✅ GOOD: Single responsibility
def clean_customer_data():
    """Clean customer data only"""
    pass

# ❌ BAD: Multiple responsibilities
def clean_and_validate_and_enrich():
    """Does too much"""
    pass
```

### 2. Error Handling

```python
# ✅ GOOD: Proper error handling
def extract_data(**context):
    conn = None
    try:
        conn = get_db_connection()
        # Do work
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        if conn:
            conn.close()

# ❌ BAD: No error handling
def extract_data():
    conn = get_db_connection()
    # Do work
    conn.close()
```

### 3. Logging

```python
# ✅ GOOD: Detailed logging
logger.info(f"Processing {record_count} records")
logger.warning(f"Found {duplicate_count} duplicates")
logger.error(f"Failed to process: {error_message}")

# ❌ BAD: No logging
print("Done")
```

### 4. Data Validation

```python
# ✅ GOOD: Validate before processing
if not data or len(data) == 0:
    raise ValueError("No data to process")

# ❌ BAD: Assume data is valid
process_data(data)
```

### 5. XCom Communication

```python
# ✅ GOOD: Use XCom for inter-task data
task_instance.xcom_push(key='record_count', value=1000)
count = task_instance.xcom_pull(task_ids='previous_task', key='record_count')

# ❌ BAD: Use global variables
global_count = 1000
```

### 6. Task Dependencies

```python
# ✅ GOOD: Clear dependencies
extract >> transform >> load

# ❌ BAD: Implicit dependencies
# Tasks run in undefined order
```

### 7. Idempotency

```python
# ✅ GOOD: Idempotent (safe to run multiple times)
cursor.execute("TRUNCATE TABLE staging.customers")
cursor.execute("INSERT INTO staging.customers SELECT * FROM raw_data.customers")

# ❌ BAD: Not idempotent (fails on retry)
cursor.execute("INSERT INTO staging.customers SELECT * FROM raw_data.customers")
# Second run fails due to duplicates
```

---

## Troubleshooting

### Issue: Pipeline Fails with "Connection Refused"

**Cause:** PostgreSQL not running or wrong host

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check connection
docker-compose exec postgres pg_isready -U datauser

# Verify host in DAG
# Should be 'postgres' (service name) not 'localhost'
```

### Issue: Slow Pipeline Execution

**Cause:** Missing indexes or inefficient queries

**Solution:**
```bash
# Check query performance
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
EXPLAIN ANALYZE
SELECT * FROM raw_data.customers WHERE email = 'test@example.com'
"

# Add missing indexes
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
CREATE INDEX idx_customers_email ON raw_data.customers(email);
"
```

### Issue: Out of Memory

**Cause:** Processing too much data at once

**Solution:**
```python
# Use batch processing
BATCH_SIZE = 10000

for i in range(0, total_records, BATCH_SIZE):
    batch = data[i:i+BATCH_SIZE]
    process_batch(batch)
```

### Issue: Data Quality Checks Fail

**Cause:** Invalid data in source

**Solution:**
```bash
# Investigate the issue
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT * FROM raw_data.customers WHERE email IS NULL LIMIT 10;
"

# Fix the data
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
UPDATE raw_data.customers SET email = 'unknown@example.com' WHERE email IS NULL;
"
```

---

## Production Deployment

### Pre-Production Checklist

- [ ] Change all default passwords
- [ ] Enable SSL/TLS for connections
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerting
- [ ] Implement data retention policies
- [ ] Configure disaster recovery
- [ ] Load test with production data volume
- [ ] Document runbooks
- [ ] Set up audit logging
- [ ] Configure resource limits

### Scaling Considerations

**Horizontal Scaling:**
```yaml
# Use Kubernetes instead of Docker Compose
# Deploy multiple Airflow workers
# Use managed PostgreSQL (RDS, Cloud SQL)
```

**Performance Tuning:**
```sql
-- Partition large tables
CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

-- Create indexes strategically
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- Use materialized views for complex aggregations
CREATE MATERIALIZED VIEW mv_daily_sales AS ...;
```

**Resource Management:**
```yaml
# Set resource limits in docker-compose.yml
services:
  postgres:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
```

### Monitoring in Production

```bash
# Set up Prometheus scraping
# Configure Grafana dashboards
# Set up alerting rules
# Enable audit logging
# Monitor resource usage
# Track SLAs
```

---

## Quick Reference

### Common Commands

```bash
# List all DAGs
docker-compose exec airflow-webserver airflow dags list

# Trigger a DAG
docker-compose exec airflow-webserver airflow dags trigger data_preparation_pipeline

# View DAG structure
docker-compose exec airflow-webserver airflow dags show data_preparation_pipeline

# View task logs
docker-compose exec airflow-webserver airflow tasks logs data_preparation_pipeline profile_raw_data 2024-01-01

# Reset DAG
docker-compose exec airflow-webserver airflow dags delete data_preparation_pipeline

# View XCom data
docker-compose exec airflow-webserver airflow tasks list data_preparation_pipeline
```

### Database Queries

```bash
# Check data quality
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT * FROM data_quality.dq_metrics WHERE check_date = CURRENT_DATE;
"

# View customer segments
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT segment, COUNT(*) FROM analytics.customer_segments GROUP BY segment;
"

# Check pipeline performance
docker-compose exec postgres psql -U datauser -d datawarehouse -c "
SELECT dag_id, task_id, AVG(EXTRACT(EPOCH FROM (end_date - start_date)))
FROM airflow.task_instance
GROUP BY dag_id, task_id;
"
```

---

## Next Steps

1. **Deploy the pipelines**
   ```bash
   docker-compose up -d
   ```

2. **Verify in Airflow UI**
   - http://localhost:8082
   - Login: admin / admin

3. **Trigger pipelines manually**
   ```bash
   docker-compose exec airflow-webserver airflow dags trigger data_preparation_pipeline
   docker-compose exec airflow-webserver airflow dags trigger advanced_analytics_pipeline
   ```

4. **Monitor execution**
   - Check Airflow UI for DAG runs
   - View logs for any errors
   - Check data quality metrics

5. **Create Grafana dashboards**
   - Connect to PostgreSQL datasource
   - Create visualizations
   - Set up alerts

6. **Optimize performance**
   - Add indexes as needed
   - Tune query performance
   - Monitor resource usage

---

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Dimensional Modeling Guide](https://www.kimballgroup.com/)
- [Data Quality Best Practices](https://www.dataqualitygov.org/)
- [RFM Analysis](https://en.wikipedia.org/wiki/RFM_(customer_value))

---

**Last Updated:** 2024  
**Version:** 1.0.0  
**Status:** Production Ready
