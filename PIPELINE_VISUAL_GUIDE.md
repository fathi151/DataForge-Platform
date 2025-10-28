# Enterprise Airflow Pipelines - Visual Guide

## 🎯 Complete Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENTERPRISE DATA PLATFORM                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          RAW DATA LAYER                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ���──────────────┐   │
│  │  customers   │  │   orders     │  │  products    │  │ order_items  │   │
│  │  (5 records) │  │  (5 records) │  │  (5 records) │  │  (8 records) │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│              DATA PREPARATION PIPELINE (Runs Daily at 1 AM)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 1: PROFILING & DISCOVERY (1-2 min)                           │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ • Analyze data structure                                            │   │
│  │ • Count records, nulls, duplicates                                  │   │
│  │ • Identify patterns and ranges                                      │   │
│  │ • Output: Profiling report (XCom)                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌──────────────────────────────────���──────────────────────────────────┐   │
│  │ STAGE 2: DATA VALIDATION (1-2 min)                                 │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ ✓ No duplicate emails                                               │   │
│  │ ✓ No orphaned orders                                                │   │
│  │ ✓ No negative amounts                                               │   │
│  │ ✓ No future dates                                                   │   │
│  │ ✓ Valid email formats                                               │   │
│  │ ✓ No missing required fields                                        │   │
│  │ • Output: Validation results (XCom)                                 │   │
│  │ • FAIL: Pipeline stops if critical issues found                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 3: DATA CLEANING (2-3 min)                                   │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ Customers:                                                           │   │
│  │   • TRIM(first_name, last_name, phone)                              │   │
│  │   • LOWER(email)                                                    │   │
│  │   • UPPER(country)                                                  │   │
│  │   • Filter: email NOT NULL AND email LIKE '%@%.%'                   │   │
│  │                                                                      │   │
│  │ Orders:                                                              │   │
│  │   • ROUND(total_amount, 2)                                          │   │
│  │   • UPPER(status)                                                   │   │
│  │   • Filter: total_amount > 0 AND order_date <= TODAY                │   │
│  │                                                                      │   │
│  │ Products:                                                            │   │
│  │   • TRIM(product_name)                                              │   │
│  │   • UPPER(category)                                                 │   │
│  │   • ROUND(price, 2)                                                 │   │
│  │   • GREATEST(stock_quantity, 0)                                     │   │
│  │ • Output: Cleaned temp tables                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 4: DEDUPLICATION (1-2 min)                                   │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ Customers:                                                           │   │
│  │   • DISTINCT ON (email)                                             │   │
│  │   • ORDER BY email, updated_at DESC                                 │   │
│  │   • Keep most recent record                                         │   │
│  │                                                                      │   │
│  │ Orders:                                                              │   │
│  │   • DISTINCT ON (order_id)                                          │   │
│  │   • ORDER BY order_id, created_at DESC                              │   │
│  │ • Output: Deduplicated temp tables                                   │   │
│  │ • Metric: Duplicates removed (XCom)                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
��                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 5: DATA ENRICHMENT (2-3 min)                                 │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ Customer Enrichment:                                                 │   │
│  │   • total_orders = COUNT(orders)                                    │   │
│  │   • lifetime_value = SUM(order_amount)                              │   │
│  │   • avg_order_value = AVG(order_amount)                             │   │
│  │   • last_order_date = MAX(order_date)                               │   │
│  │   • customer_status = NEW|INACTIVE|AT_RISK|ACTIVE                   │   │
│  │   • customer_segment = VIP|PREMIUM|REGULAR|PROSPECT                 │   │
│  │                                                                      │   │
│  │ Order Enrichment:                                                    │   │
│  │   • order_year, order_month, order_quarter                          │   │
│  │   • order_day_of_week                                               │   │
│  │   • order_value_category = HIGH|MEDIUM|LOW                          │   │
│  │   • is_completed = 1|0                                              │   │
│  │ • Output: Enriched temp tables                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 6: LOAD TO STAGING (1-2 min)                                 │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ • TRUNCATE staging.customers_staging                                │   │
│  │ • INSERT cleaned & enriched customers                               │   │
│  │ • TRUNCATE staging.orders_staging                                   │   │
│  │ • INSERT cleaned & enriched orders                                  │   │
│  │ • Log record counts (XCom)                                          │   │
│  │ • Output: Staging tables populated                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 7: CLEANUP (<1 min)                                           │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │ • DROP temp_customers_cleaned                                       │   │
│  │ • DROP temp_customers_deduped                                       │   │
│  │ • DROP temp_customers_enriched                                      │   │
│  │ • DROP temp_orders_cleaned                                          │   │
│  │ • DROP temp_orders_deduped                                          │   │
│  │ • DROP temp_orders_enriched                                         │   │
│  │ • DROP temp_products_cleaned                                        │   │
│  │ • Output: Clean database                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Total Duration: ~10-15 minutes                                             │
│  Success Rate Target: > 95%                                                 │
│  Failure Handling: Automatic retry (2 times)                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          STAGING LAYER                                       │
│  ┌──────────────────────────┐  ┌──────────────────────────┐                │
│  │ customers_staging        │  │ orders_staging           │                │
│  │ (cleaned & enriched)     │  │ (cleaned & enriched)     │                │
��  └──────────────────────────┘  └──────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│           ADVANCED ANALYTICS PIPELINE (Runs Daily at 3 AM)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 1: BUILD DIMENSION TABLES (2-3 min)                          │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │ dim_customer (SCD Type 2):                                          │   │
│  │   • customer_key (PK)                                               │   │
│  │   • customer_id, first_name, last_name, email, phone, country      │   │
│  │   • customer_segment, customer_status                               │   │
│  │   • effective_date, end_date, is_current                            │   │
│  │   • Tracks historical changes                                       │   │
│  │   • Old records marked inactive, new records inserted               │   │
│  │                                                                      │   │
│  │ dim_product:                                                        │   │
│  │   • product_key (PK)                                                │   │
│  │   • product_id, product_name, category, price                       │   │
│  │   • is_active, created_at, updated_at                               │   │
│  │                                                                      │   │
│  │ dim_date:                                                           │   │
│  │   • date_key (YYYYMMDD format)                                      │   │
│  │   • date, year, quarter, month, day                                 │   │
│  │   • day_of_week, week_of_year                                       │   │
│  │   • is_weekend, is_holiday                                          │   │
│  │   • Coverage: 5 years back + 2 years forward                        │   │
│  │                                                                      │   │
│  │ Output: 3 dimension tables ready for facts                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 2: BUILD FACT TABLES (2-3 min)                               │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │ fact_sales:                                                         │   │
│  │   • sales_key (PK)                                                  │   │
│  │   • customer_key (FK → dim_customer)                                │   │
│  │   • product_key (FK → dim_product)                                  │   │
│  │   • date_key (FK → dim_date)                                        │   │
│  │   • order_id, quantity, unit_price, total_amount                    │   │
│  │   • discount_amount, tax_amount, net_amount                         │   │
│  │   • Grain: One row per order item                                   │   │
│  │   • Joined with dimensions for complete context                     │   │
│  │                                                                      │   │
│  │ Output: Fact table with all dimensions                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 3: BUILD AGGREGATE TABLES (2-3 min)                          │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │ customer_metrics:                                                   │   │
│  │   • customer_id (PK)                                                │   │
│  │   • total_orders, total_spent, average_order_value                  │   │
│  │   • last_order_date                                                 │   │
│  │                                                                      │   │
│  │ daily_sales:                                                        │   │
│  │   • sale_date (PK)                                                  │   │
│  │   • total_sales, total_orders, unique_customers                     │   │
│  │                                                                      │   │
│  │ monthly_revenue:                                                    │   │
│  │   • year_month (PK)                                                 │   │
│  │   • total_revenue, total_orders, average_order_value                │   │
│  │   • unique_customers                                                │   │
│  │                                                                      │   │
│  │ product_performance:                                                │   │
│  │   • product_id (PK)                                                 │   │
│  │   • total_sold, total_revenue, average_price                        │   │
│  │   • last_sold_date                                                  │   │
│  │                                                                      │   │
│  │ Output: 4 aggregate tables                                          │   │
│  └──────────────────────────────────────���──────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 4: BUILD ADVANCED METRICS (2-3 min)                          │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │ customer_segments (RFM Analysis):                                   │   │
│  │   • customer_id (PK)                                                │   │
│  │   • segment (VIP_ACTIVE, VIP_AT_RISK, PREMIUM_ACTIVE, etc.)        │   │
│  │   • lifetime_value, recency_days, frequency, monetary_value         │   │
│  │   • churn_risk (0.0 to 0.95)                                        │   │
│  │                                                                      │   │
│  │   Segmentation Logic:                                               │   │
│  │   ┌─────────────────────────────────────────────────────────────┐  │   │
│  │   │ VIP_ACTIVE:      LTV > 5000 AND Recency < 30 days          │  │   │
│  │   │ VIP_AT_RISK:     LTV > 5000 AND Recency < 90 days          │  │   │
│  │   │ PREMIUM_ACTIVE:  LTV > 1000 AND Recency < 30 days          │  │   │
│  │   │ PREMIUM_AT_RISK: LTV > 1000 AND Recency < 90 days          │  │   │
│  │   │ LOYAL_ACTIVE:    Frequency > 5 AND Recency < 30 days       │  │   │
│  │   │ LOYAL_AT_RISK:   Frequency > 5 AND Recency < 90 days       │  │   │
│  │   │ CHURNED:         Recency > 180 days                         │  │   │
│  │   │ AT_RISK:         Recency > 90 days                          │  │   │
│  │   │ NEW:             Frequency = 1                              │  │   │
│  │   │ REGULAR:         Others                                     │  │   │
│  │   └─────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │ cohort_analysis:                                                    │   │
│  │   • cohort_month (when customer first purchased)                    │   │
│  │   • cohort_age_months (months since first purchase)                 │   │
│  │   • customer_count (active customers in cohort)                     │   │
│  │   • revenue (revenue from cohort)                                   │   │
│  │   • retention_rate (% of original cohort still active)              │   │
│  │                                                                      │   │
│  │   Example:                                                          │   │
│  │   ┌─────────────────────────────────────────────────────────────┐  │   │
│  │   │ Cohort 2024-01:                                             │  │   │
│  │   │   Month 0: 100 customers, $10,000, 100% retention          │  │   │
│  │   │   Month 1: 85 customers, $8,500, 85% retention             │  │   │
│  │   │   Month 2: 72 customers, $7,200, 72% retention             │  │   │
│  │   └─────────────────────────────────────────────────────────────┘  │   │
│  │                                                                      │   │
│  │ Output: 2 advanced metric tables                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 5: CREATE MATERIALIZED VIEWS (1-2 min)                       │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │ mv_customer_summary:                                                │   │
│  │   • Fast customer lookup with aggregates                            │   │
│  │   • Indexed by total_spent                                          │   │
│  │                                                                      │   │
│  │ mv_sales_by_category:                                               │   │
│  │   • Sales metrics by product category                               │   │
│  │   • Indexed by total_revenue                                        │   │
│  │                                                                      │   │
│  │ mv_top_customers:                                                   │   │
│  │   • Top 1000 customers by spending                                  │   │
│  │   • Ranked and indexed                                              │   │
│  │                                                                      │   │
│  │ Output: 3 materialized views for fast queries                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 6: QUALITY CHECKS (1-2 min)                                  │   │
│  ├────────────────────���────────────────────────────────────────────────┤   │
│  │ ✓ Fact table not empty                                              │   │
│  │ ✓ No null dimension keys                                            │   │
│  │ ✓ No negative metrics                                               │   │
│  │ ✓ Aggregate consistency                                             │   │
│  │ • Output: Quality report                                            │   │
│  │ • FAIL: Alert if issues found                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Total Duration: ~12-18 minutes                                             │
│  Success Rate Target: > 95%                                                 │
│  Failure Handling: Automatic retry (2 times)                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ANALYTICS LAYER                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Dimensions       │  │ Facts            │  │ Aggregates       │          │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤          │
│  │ dim_customer     │  │ fact_sales       │  │ customer_metrics │          │
│  │ dim_product      │  │                  │  │ daily_sales      │          │
│  │ dim_date         │  │                  │  │ monthly_revenue  │          │
│  │                  │  │                  │  │ product_perf     │          │
│  │                  │  │                  │  │ customer_segs    │          │
│  │                  │  │                  │  │ cohort_analysis  │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                              │
│  Materialized Views:                                                         │
│  ├─ mv_customer_summary                                                     │
│  ├─ mv_sales_by_category                                                    │
│  └─ mv_top_customers                                                        │
└──────────────────────────────────────────────��──────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│         MONITORING PIPELINE (Runs Hourly)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Monitor Pipeline Health                                             │   │
│  │ • Success rates, execution times, failed tasks                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Monitor Data Quality                                                │   │
│  │ • Quality check results, trends, alerts                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   ��
│  │ Monitor Data Freshness                                              │   │
│  │ • Last update times, data age, staleness alerts                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Monitor Business Metrics                                            │   │
│  │ • Daily sales, customer counts, segments, trends                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Generate Monitoring Report                                          │   │
│  │ • Comprehensive report with all metrics and alerts                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Duration: 2-3 minutes                                                      │
│  Frequency: Every hour                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Grafana          │  │ Jupyter          │  │ Custom API       │          │
│  │ Dashboards       │  │ Notebooks        │  │ Endpoints        │          │
│  │                  │  │                  │  │                  │          │
│  │ • Sales Trends   │  │ • Data Analysis  │  │ • /metrics       │          │
│  │ • Segments       │  │ • Exploration    │  │ • /customers     │          │
│  │ • Performance    │  ��� • Modeling       │  │ • /products      │          │
│  │ • Health         │  │ • Forecasting    │  │ • /segments      │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Transformation Example: Customer Journey

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CUSTOMER DATA TRANSFORMATION                              │
└─────────────────────────────────────────────────────────────────────────────┘

RAW DATA:
┌──────────────────────────────────��───────────────────────────────────────┐
│ customer_id │ first_name │ last_name │ email                │ country    │
├──────────────────────────────────────────────────────────────────────────┤
│ 1           │ Jean       │ Dupont    │ jean.dupont@email.com│ france     │
│ 2           │ Marie      │ Martin    │ marie.martin@email.com│ FRANCE    │
│ 3           │ Pierre     │ Bernard   │ pierre.bernard@email │ France    │
│ 4           │ Sophie     │ Leclerc   │ sophie.leclerc@email │ france    │
│ 5           │ Luc        │ Moreau    │ luc.moreau@email.com │ FRANCE    │
└───────────────────────────────────────────────────────────��──────────────┘
                                    ↓
STAGE 1: PROFILING
┌──────────────────────────────────────────────────────────────────────────┐
│ Total Records: 5                                                         │
│ Unique Customers: 5                                                      │
│ Unique Emails: 5                                                         │
│ Null Emails: 0                                                           │
│ Unique Countries: 1                                                      │
│ Issues Found: 2 invalid emails (missing .com)                            │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
STAGE 2: VALIDATION
┌──────────────────────────────────────────────────────────────────────────┐
│ ✓ No duplicate emails                                                    │
│ ✓ No null emails                                                         │
│ ✗ 2 invalid email formats (pierre.bernard@email, sophie.leclerc@email)   │
│ ✓ No missing required fields                                             │
│ Action: WARN - Continue with filtering                                   │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
STAGE 3: CLEANING
┌──────────────────────────────────────────────────────────────────────────┐
│ customer_id │ first_name │ last_name │ email                │ country    │
├─────────────────────���────────────────────────────────────────────────────┤
│ 1           │ Jean       │ Dupont    │ jean.dupont@email.com│ FRANCE     │
│ 2           │ Marie      │ Martin    │ marie.martin@email.com│ FRANCE    │
│ 5           │ Luc        │ Moreau    │ luc.moreau@email.com │ FRANCE    │
└──────────────────────────────────────────────────────────────────────────┘
(Filtered out 2 records with invalid emails)
                                    ↓
STAGE 4: DEDUPLICATION
┌──────────────────────────────────────────────────────────────────────────┐
│ No duplicates found                                                      │
│ Records: 3 (unchanged)                                                   │
└───────────────────────────────────────────────────────────────────��──────┘
                                    ↓
STAGE 5: ENRICHMENT
┌──────────────────────────────────────────────────────────────────────────┐
│ customer_id │ email                │ total_orders │ lifetime_value │ seg │
├──────────────────────────────────────────────────────────────────────────┤
│ 1           │ jean.dupont@email.com│ 2            │ 1359.97        │ VIP │
│ 2           │ marie.martin@email.com│ 1           │ 399.99         │ REG │
│ 5           │ luc.moreau@email.com │ 2            │ 1449.97        │ VIP │
└──────────────────────────────────────────────────────���───────────────────┘
                                    ↓
STAGE 6: LOAD TO STAGING
┌──────────────────────────────────────────────────────────────────────────┐
│ Inserted into staging.customers_staging: 3 records                       │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
ANALYTICS PIPELINE
                                    ↓
DIMENSION TABLE (dim_customer)
┌──────────────────────────────────────────────────────────────────────────┐
│ customer_key │ customer_id │ email                │ segment │ is_current │
├───────────────────────────────���──────────────────────────────────────────┤
│ 1            │ 1           │ jean.dupont@email.com│ VIP     │ TRUE       │
│ 2            │ 2           │ marie.martin@email.com│ REGULAR │ TRUE       │
│ 3            │ 5           │ luc.moreau@email.com │ VIP     │ TRUE       │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
AGGREGATES (customer_metrics)
┌──────────────────────────────────────────────────────────────────────────┐
│ customer_id │ total_orders │ total_spent │ avg_order_value │ last_order │
├────────────────────────────────────────────────────────────────���─────────┤
│ 1           │ 2            │ 1359.97     │ 679.99          │ 2024-01-18 │
│ 2           │ 1            │ 399.99      │ 399.99          │ 2024-01-16 │
│ 5           │ 2            │ 1449.97     │ 724.99          │ 2024-01-19 │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
SEGMENTS (customer_segments - RFM)
┌──────────────────────────────────────────────────────────────────────────┐
│ customer_id │ segment     │ lifetime_value │ recency_days │ churn_risk  │
├──────────────────────────────────────────────────────────────────────────┤
│ 1           │ VIP_ACTIVE  │ 1359.97        │ 3            │ 0.0         │
│ 2           │ REGULAR     │ 399.99         │ 5            │ 0.0         │
│ 5           │ VIP_ACTIVE  │ 1449.97        │ 1            │ 0.0         │
└──────────────────────────────────────────────────────────────────────────┘
                                    ↓
READY FOR DASHBOARDS & REPORTS
```

---

## 🔄 Pipeline Execution Timeline

```
Daily Schedule:

00:00 ─────────────────────────────────────────────────────────────────
      │
01:00 ├─ DATA PREPARATION PIPELINE STARTS
      │  ├─ Stage 1: Profiling (1-2 min)
      │  ├─ Stage 2: Validation (1-2 min)
      │  ├─ Stage 3: Cleaning (2-3 min)
      │  ├─ Stage 4: Deduplication (1-2 min)
      │  ├─ Stage 5: Enrichment (2-3 min)
      │  ├─ Stage 6: Load to Staging (1-2 min)
      │  └─ Stage 7: Cleanup (<1 min)
      │  └─ TOTAL: ~10-15 minutes
      │
01:20 ├─ DATA PREPARATION COMPLETE
      │
03:00 ├─ ADVANCED ANALYTICS PIPELINE STARTS
      │  ├─ Stage 1: Build Dimensions (2-3 min)
      │  ├─ Stage 2: Build Facts (2-3 min)
      │  ├─ Stage 3: Build Aggregates (2-3 min)
      │  ├─ Stage 4: Advanced Metrics (2-3 min)
      │  ├─ Stage 5: Materialized Views (1-2 min)
      │  └─ Stage 6: Quality Checks (1-2 min)
      │  └─ TOTAL: ~12-18 minutes
      │
03:30 ├─ ADVANCED ANALYTICS COMPLETE
      │
04:00 ├─ DASHBOARDS & REPORTS READY
      │
      │ MONITORING PIPELINE (Every Hour)
      │ ├─ 01:00, 02:00, 03:00, 04:00, ...
      │ ├─ Duration: 2-3 minutes each
      │ └─ Tracks health, quality, freshness, metrics
      │
24:00 └─ END OF DAY
```

---

## 🎯 Key Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE METRICS DASHBOARD                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PIPELINE HEALTH                    DATA QUALITY                            │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │ Success Rate: 98.5%          │  │ Quality Checks: 6/6 PASS     │        │
│  │ Avg Duration: 14.2 min       │  │ Data Freshness: < 1 hour     │        │
│  │ Failed Tasks: 1              │  │ Duplicate Records: 0         │        │
│  │ Last Run: 2024-01-20 03:30   │  │ Invalid Records: 0           │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                              │
│  BUSINESS METRICS                   CUSTOMER SEGMENTS                       │
│  ┌──────────────────────────────┐  ┌──────────────────────────────┐        │
│  │ Daily Sales: $3,209.94       │  │ VIP_ACTIVE: 2 customers      │        │
│  │ Total Orders: 5              │  │ PREMIUM_ACTIVE: 0            │        │
│  │ Unique Customers: 3          │  │ LOYAL_ACTIVE: 0              │        │
│  │ Avg Order Value: $641.99     │  │ REGULAR: 1 customer          │        │
│  │ Lifetime Value: $3,209.94    │  │ AT_RISK: 0                   │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                              │
│  TOP PRODUCTS                       MONTHLY TRENDS                          │
│  ┌──────────────────────────────┐  ┌─────────────────────────���────┐        │
│  │ 1. Laptop Pro: $2,599.98     │  │ Jan 2024: $3,209.94          │        │
│  │ 2. Monitor 4K: $399.99       │  │ Trend: ↑ Increasing          │        │
│  │ 3. Keyboard: $299.98         │  │ Forecast: $3,500 (Feb)       │        │
│  │ 4. Mouse: $29.99             │  │ Growth: +9.0%                │        │
│  │ 5. Cable: $9.99              │  │                              │        │
│  └──────────────────────────────┘  └──────────────────────────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

1. **Start Services**
   ```bash
   docker-compose up -d
   ```

2. **Access Airflow**
   ```
   http://localhost:8082
   ```

3. **Trigger Pipelines**
   - data_preparation_pipeline
   - advanced_analytics_pipeline
   - monitoring_pipeline

4. **View Results**
   ```bash
   docker-compose exec postgres psql -U datauser -d datawarehouse
   SELECT * FROM analytics.customer_segments;
   ```

5. **Create Dashboards**
   ```
   http://localhost:3001 (Grafana)
   ```

---

**This is enterprise-grade Airflow setup!** 🎉
