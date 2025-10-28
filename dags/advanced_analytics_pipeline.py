"""
Enterprise-Grade Advanced Analytics Pipeline
Implements dimensional modeling, aggregations, and business metrics
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
import psycopg2
import logging
import json

logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'postgres',
    'database': 'datawarehouse',
    'user': 'datauser',
    'password': 'datapass123'
}

default_args = {
    'owner': 'data-analytics',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email': ['analytics-team@company.com'],
    'execution_timeout': timedelta(hours=3),
}

dag = DAG(
    'advanced_analytics_pipeline',
    default_args=default_args,
    description='Enterprise Analytics with Dimensional Modeling & Advanced Metrics',
    schedule_interval='0 3 * * *',  # Daily at 3 AM
    catchup=False,
    tags=['analytics', 'enterprise', 'production'],
    max_active_runs=1,
)

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)

def push_xcom_data(task_instance, key: str, value):
    """Push data to XCom"""
    task_instance.xcom_push(key=key, value=value)

# ============================================================================
# STAGE 1: BUILD DIMENSION TABLES
# ============================================================================

def build_dim_customer(**context):
    """
    Build customer dimension table with SCD Type 2
    """
    logger.info("Building customer dimension table...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create dimension table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.dim_customer (
                customer_key SERIAL PRIMARY KEY,
                customer_id INTEGER,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(20),
                country VARCHAR(50),
                customer_segment VARCHAR(50),
                customer_status VARCHAR(50),
                effective_date DATE,
                end_date DATE,
                is_current BOOLEAN,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        # Mark old records as inactive
        cursor.execute("""
            UPDATE analytics.dim_customer
            SET is_current = FALSE, end_date = CURRENT_DATE - INTERVAL '1 day'
            WHERE is_current = TRUE
            AND customer_id IN (
                SELECT DISTINCT customer_id FROM staging.customers_staging
            )
        """)
        
        # Insert new/updated records
        cursor.execute("""
            INSERT INTO analytics.dim_customer 
            (customer_id, first_name, last_name, email, phone, country, 
             customer_segment, customer_status, effective_date, end_date, is_current, created_at, updated_at)
            SELECT DISTINCT 
                c.customer_id,
                c.first_name,
                c.last_name,
                c.email,
                c.phone,
                c.country,
                'STANDARD' as customer_segment,
                'ACTIVE' as customer_status,
                CURRENT_DATE,
                '9999-12-31'::DATE,
                TRUE,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            FROM staging.customers_staging c
            WHERE NOT EXISTS (
                SELECT 1 FROM analytics.dim_customer dc 
                WHERE dc.customer_id = c.customer_id AND dc.is_current = TRUE
            )
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.dim_customer WHERE is_current = TRUE")
        active_customers = cursor.fetchone()[0]
        
        logger.info(f"Built customer dimension with {active_customers} active records")
        push_xcom_data(context['task_instance'], 'dim_customer_count', active_customers)
        
        return active_customers
        
    finally:
        cursor.close()
        conn.close()

def build_dim_product(**context):
    """
    Build product dimension table
    """
    logger.info("Building product dimension table...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.dim_product (
                product_key SERIAL PRIMARY KEY,
                product_id INTEGER UNIQUE,
                product_name VARCHAR(200),
                category VARCHAR(100),
                price DECIMAL(10, 2),
                is_active BOOLEAN,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO analytics.dim_product 
            (product_id, product_name, category, price, is_active, created_at, updated_at)
            SELECT 
                product_id,
                product_name,
                category,
                price,
                TRUE,
                created_at,
                CURRENT_TIMESTAMP
            FROM raw_data.products
            ON CONFLICT (product_id) DO UPDATE SET
                product_name = EXCLUDED.product_name,
                category = EXCLUDED.category,
                price = EXCLUDED.price,
                updated_at = CURRENT_TIMESTAMP
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.dim_product WHERE is_active = TRUE")
        active_products = cursor.fetchone()[0]
        
        logger.info(f"Built product dimension with {active_products} active records")
        push_xcom_data(context['task_instance'], 'dim_product_count', active_products)
        
        return active_products
        
    finally:
        cursor.close()
        conn.close()

def build_dim_date(**context):
    """
    Build date dimension table for time-based analysis
    """
    logger.info("Building date dimension table...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.dim_date (
                date_key INTEGER PRIMARY KEY,
                date DATE UNIQUE,
                year INTEGER,
                quarter INTEGER,
                month INTEGER,
                day INTEGER,
                day_of_week VARCHAR(10),
                week_of_year INTEGER,
                is_weekend BOOLEAN,
                is_holiday BOOLEAN,
                created_at TIMESTAMP
            )
        """)
        
        # Generate dates for the last 5 years and next 2 years
        cursor.execute("""
            INSERT INTO analytics.dim_date 
            (date_key, date, year, quarter, month, day, day_of_week, week_of_year, is_weekend, is_holiday, created_at)
            SELECT 
                TO_CHAR(d, 'YYYYMMDD')::INTEGER as date_key,
                d as date,
                EXTRACT(YEAR FROM d)::INTEGER as year,
                EXTRACT(QUARTER FROM d)::INTEGER as quarter,
                EXTRACT(MONTH FROM d)::INTEGER as month,
                EXTRACT(DAY FROM d)::INTEGER as day,
                TO_CHAR(d, 'Day') as day_of_week,
                EXTRACT(WEEK FROM d)::INTEGER as week_of_year,
                EXTRACT(DOW FROM d) IN (0, 6) as is_weekend,
                FALSE as is_holiday,
                CURRENT_TIMESTAMP
            FROM (
                SELECT CURRENT_DATE - INTERVAL '5 years' + (n || ' days')::INTERVAL as d
                FROM GENERATE_SERIES(0, 2555) n
            ) dates
            ON CONFLICT (date_key) DO NOTHING
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.dim_date")
        date_count = cursor.fetchone()[0]
        
        logger.info(f"Built date dimension with {date_count} records")
        push_xcom_data(context['task_instance'], 'dim_date_count', date_count)
        
        return date_count
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 2: BUILD FACT TABLES
# ============================================================================

def build_fact_sales(**context):
    """
    Build fact sales table from staging data
    """
    logger.info("Building fact sales table...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.fact_sales (
                sales_key SERIAL PRIMARY KEY,
                customer_key INTEGER REFERENCES analytics.dim_customer(customer_key),
                product_key INTEGER REFERENCES analytics.dim_product(product_key),
                date_key INTEGER REFERENCES analytics.dim_date(date_key),
                order_id INTEGER,
                quantity INTEGER,
                unit_price DECIMAL(10, 2),
                total_amount DECIMAL(12, 2),
                discount_amount DECIMAL(10, 2) DEFAULT 0,
                tax_amount DECIMAL(10, 2) DEFAULT 0,
                net_amount DECIMAL(12, 2),
                created_at TIMESTAMP
            )
        """)
        
        # Truncate and reload
        cursor.execute("TRUNCATE TABLE analytics.fact_sales")
        
        cursor.execute("""
            INSERT INTO analytics.fact_sales 
            (customer_key, product_key, date_key, order_id, quantity, unit_price, 
             total_amount, discount_amount, tax_amount, net_amount, created_at)
            SELECT 
                dc.customer_key,
                dp.product_key,
                dd.date_key,
                oi.order_id,
                oi.quantity,
                oi.unit_price,
                oi.quantity * oi.unit_price as total_amount,
                0 as discount_amount,
                0 as tax_amount,
                oi.quantity * oi.unit_price as net_amount,
                CURRENT_TIMESTAMP
            FROM raw_data.order_items oi
            JOIN raw_data.orders o ON oi.order_id = o.order_id
            JOIN analytics.dim_customer dc ON o.customer_id = dc.customer_id AND dc.is_current = TRUE
            JOIN analytics.dim_product dp ON oi.product_id = dp.product_id
            JOIN analytics.dim_date dd ON o.order_date = dd.date
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.fact_sales")
        sales_count = cursor.fetchone()[0]
        
        logger.info(f"Built fact sales table with {sales_count} records")
        push_xcom_data(context['task_instance'], 'fact_sales_count', sales_count)
        
        return sales_count
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 3: BUILD AGGREGATE TABLES
# ============================================================================

def build_customer_metrics(**context):
    """
    Build comprehensive customer metrics
    """
    logger.info("Building customer metrics...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            TRUNCATE TABLE analytics.customer_metrics;
            
            INSERT INTO analytics.customer_metrics 
            (customer_id, total_orders, total_spent, average_order_value, last_order_date)
            SELECT 
                c.customer_id,
                COUNT(DISTINCT o.order_id) as total_orders,
                COALESCE(SUM(o.total_amount), 0) as total_spent,
                COALESCE(AVG(o.total_amount), 0) as average_order_value,
                MAX(o.order_date) as last_order_date
            FROM staging.customers_staging c
            LEFT JOIN staging.orders_staging o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.customer_metrics")
        metrics_count = cursor.fetchone()[0]
        
        logger.info(f"Built customer metrics for {metrics_count} customers")
        push_xcom_data(context['task_instance'], 'customer_metrics_count', metrics_count)
        
        return metrics_count
        
    finally:
        cursor.close()
        conn.close()

def build_daily_sales(**context):
    """
    Build daily sales aggregations
    """
    logger.info("Building daily sales metrics...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            TRUNCATE TABLE analytics.daily_sales;
            
            INSERT INTO analytics.daily_sales 
            (sale_date, total_sales, total_orders, unique_customers)
            SELECT 
                o.order_date,
                SUM(o.total_amount) as total_sales,
                COUNT(DISTINCT o.order_id) as total_orders,
                COUNT(DISTINCT o.customer_id) as unique_customers
            FROM staging.orders_staging o
            GROUP BY o.order_date
            ORDER BY o.order_date DESC
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.daily_sales")
        daily_count = cursor.fetchone()[0]
        
        logger.info(f"Built daily sales metrics for {daily_count} days")
        push_xcom_data(context['task_instance'], 'daily_sales_count', daily_count)
        
        return daily_count
        
    finally:
        cursor.close()
        conn.close()

def build_monthly_revenue(**context):
    """
    Build monthly revenue aggregations
    """
    logger.info("Building monthly revenue metrics...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.monthly_revenue (
                year_month DATE PRIMARY KEY,
                total_revenue DECIMAL(12, 2),
                total_orders INTEGER,
                average_order_value DECIMAL(10, 2),
                unique_customers INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            TRUNCATE TABLE analytics.monthly_revenue;
            
            INSERT INTO analytics.monthly_revenue 
            (year_month, total_revenue, total_orders, average_order_value, unique_customers)
            SELECT 
                DATE_TRUNC('month', o.order_date)::DATE as year_month,
                SUM(o.total_amount) as total_revenue,
                COUNT(DISTINCT o.order_id) as total_orders,
                AVG(o.total_amount) as average_order_value,
                COUNT(DISTINCT o.customer_id) as unique_customers
            FROM staging.orders_staging o
            GROUP BY DATE_TRUNC('month', o.order_date)
            ORDER BY year_month DESC
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.monthly_revenue")
        monthly_count = cursor.fetchone()[0]
        
        logger.info(f"Built monthly revenue metrics for {monthly_count} months")
        push_xcom_data(context['task_instance'], 'monthly_revenue_count', monthly_count)
        
        return monthly_count
        
    finally:
        cursor.close()
        conn.close()

def build_product_performance(**context):
    """
    Build product performance metrics
    """
    logger.info("Building product performance metrics...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.product_performance (
                product_id INTEGER PRIMARY KEY,
                product_name VARCHAR(200),
                category VARCHAR(100),
                total_sold INTEGER,
                total_revenue DECIMAL(12, 2),
                average_price DECIMAL(10, 2),
                last_sold_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            TRUNCATE TABLE analytics.product_performance;
            
            INSERT INTO analytics.product_performance 
            (product_id, product_name, category, total_sold, total_revenue, average_price, last_sold_date)
            SELECT 
                p.product_id,
                p.product_name,
                p.category,
                COALESCE(SUM(oi.quantity), 0) as total_sold,
                COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue,
                COALESCE(AVG(oi.unit_price), 0) as average_price,
                MAX(o.order_date) as last_sold_date
            FROM raw_data.products p
            LEFT JOIN raw_data.order_items oi ON p.product_id = oi.product_id
            LEFT JOIN raw_data.orders o ON oi.order_id = o.order_id
            GROUP BY p.product_id, p.product_name, p.category
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.product_performance")
        product_count = cursor.fetchone()[0]
        
        logger.info(f"Built product performance metrics for {product_count} products")
        push_xcom_data(context['task_instance'], 'product_performance_count', product_count)
        
        return product_count
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 4: BUILD ADVANCED METRICS
# ============================================================================

def build_customer_segments(**context):
    """
    Build customer segmentation based on RFM analysis
    """
    logger.info("Building customer segments...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.customer_segments (
                customer_id INTEGER PRIMARY KEY,
                segment VARCHAR(50),
                lifetime_value DECIMAL(12, 2),
                recency_days INTEGER,
                frequency INTEGER,
                monetary_value DECIMAL(12, 2),
                churn_risk DECIMAL(3, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            TRUNCATE TABLE analytics.customer_segments;
            
            INSERT INTO analytics.customer_segments 
            (customer_id, segment, lifetime_value, recency_days, frequency, monetary_value, churn_risk)
            WITH rfm AS (
                SELECT 
                    c.customer_id,
                    COALESCE(SUM(o.total_amount), 0) as lifetime_value,
                    COALESCE(EXTRACT(DAY FROM CURRENT_DATE - MAX(o.order_date)), 999) as recency_days,
                    COUNT(DISTINCT o.order_id) as frequency,
                    COALESCE(AVG(o.total_amount), 0) as monetary_value
                FROM staging.customers_staging c
                LEFT JOIN staging.orders_staging o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id
            )
            SELECT 
                customer_id,
                CASE 
                    WHEN lifetime_value > 5000 AND recency_days < 30 THEN 'VIP_ACTIVE'
                    WHEN lifetime_value > 5000 AND recency_days < 90 THEN 'VIP_AT_RISK'
                    WHEN lifetime_value > 1000 AND recency_days < 30 THEN 'PREMIUM_ACTIVE'
                    WHEN lifetime_value > 1000 AND recency_days < 90 THEN 'PREMIUM_AT_RISK'
                    WHEN frequency > 5 AND recency_days < 30 THEN 'LOYAL_ACTIVE'
                    WHEN frequency > 5 AND recency_days < 90 THEN 'LOYAL_AT_RISK'
                    WHEN recency_days > 180 THEN 'CHURNED'
                    WHEN recency_days > 90 THEN 'AT_RISK'
                    WHEN frequency = 1 THEN 'NEW'
                    ELSE 'REGULAR'
                END as segment,
                lifetime_value,
                recency_days,
                frequency,
                monetary_value,
                CASE 
                    WHEN recency_days > 180 THEN 0.95
                    WHEN recency_days > 90 THEN 0.70
                    WHEN recency_days > 60 THEN 0.40
                    WHEN recency_days > 30 THEN 0.10
                    ELSE 0.0
                END as churn_risk
            FROM rfm
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.customer_segments")
        segment_count = cursor.fetchone()[0]
        
        logger.info(f"Built customer segments for {segment_count} customers")
        push_xcom_data(context['task_instance'], 'customer_segments_count', segment_count)
        
        return segment_count
        
    finally:
        cursor.close()
        conn.close()

def build_cohort_analysis(**context):
    """
    Build cohort analysis for customer retention tracking
    """
    logger.info("Building cohort analysis...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics.cohort_analysis (
                cohort_month DATE,
                cohort_age_months INTEGER,
                customer_count INTEGER,
                revenue DECIMAL(12, 2),
                retention_rate DECIMAL(5, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            TRUNCATE TABLE analytics.cohort_analysis;
            
            INSERT INTO analytics.cohort_analysis 
            (cohort_month, cohort_age_months, customer_count, revenue, retention_rate)
            WITH cohorts AS (
                SELECT 
                    DATE_TRUNC('month', MIN(o.order_date))::DATE as cohort_month,
                    c.customer_id,
                    DATE_TRUNC('month', o.order_date)::DATE as order_month
                FROM staging.customers_staging c
                LEFT JOIN staging.orders_staging o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, DATE_TRUNC('month', o.order_date)
            ),
            cohort_data AS (
                SELECT 
                    cohort_month,
                    (EXTRACT(YEAR FROM order_month) - EXTRACT(YEAR FROM cohort_month)) * 12 +
                    (EXTRACT(MONTH FROM order_month) - EXTRACT(MONTH FROM cohort_month)) as cohort_age_months,
                    COUNT(DISTINCT customer_id) as customer_count,
                    COALESCE(SUM(o.total_amount), 0) as revenue
                FROM cohorts c
                LEFT JOIN staging.orders_staging o ON c.customer_id = o.customer_id 
                    AND DATE_TRUNC('month', o.order_date) = c.order_month
                WHERE order_month IS NOT NULL
                GROUP BY cohort_month, cohort_age_months
            )
            SELECT 
                cohort_month,
                cohort_age_months,
                customer_count,
                revenue,
                ROUND(100.0 * customer_count / 
                    (SELECT customer_count FROM cohort_data cd2 
                     WHERE cd2.cohort_month = cohort_data.cohort_month 
                     AND cd2.cohort_age_months = 0), 2) as retention_rate
            FROM cohort_data
            ORDER BY cohort_month, cohort_age_months
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM analytics.cohort_analysis")
        cohort_count = cursor.fetchone()[0]
        
        logger.info(f"Built cohort analysis with {cohort_count} records")
        push_xcom_data(context['task_instance'], 'cohort_analysis_count', cohort_count)
        
        return cohort_count
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 5: CREATE MATERIALIZED VIEWS
# ============================================================================

def create_materialized_views(**context):
    """
    Create materialized views for fast query performance
    """
    logger.info("Creating materialized views...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Customer summary view
        cursor.execute("""
            DROP MATERIALIZED VIEW IF EXISTS analytics.mv_customer_summary CASCADE;
            
            CREATE MATERIALIZED VIEW analytics.mv_customer_summary AS
            SELECT 
                c.customer_id,
                c.first_name,
                c.last_name,
                c.email,
                c.country,
                COUNT(o.order_id) as total_orders,
                SUM(o.total_amount) as total_spent,
                AVG(o.total_amount) as avg_order_value,
                MAX(o.order_date) as last_order_date,
                CURRENT_TIMESTAMP as refresh_time
            FROM staging.customers_staging c
            LEFT JOIN staging.orders_staging o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.country
        """)
        
        # Sales by category view
        cursor.execute("""
            DROP MATERIALIZED VIEW IF EXISTS analytics.mv_sales_by_category CASCADE;
            
            CREATE MATERIALIZED VIEW analytics.mv_sales_by_category AS
            SELECT 
                p.category,
                COUNT(DISTINCT oi.order_id) as order_count,
                SUM(oi.quantity) as total_quantity,
                SUM(oi.quantity * oi.unit_price) as total_revenue,
                AVG(oi.unit_price) as avg_price,
                CURRENT_TIMESTAMP as refresh_time
            FROM raw_data.products p
            LEFT JOIN raw_data.order_items oi ON p.product_id = oi.product_id
            GROUP BY p.category
        """)
        
        # Top customers view
        cursor.execute("""
            DROP MATERIALIZED VIEW IF EXISTS analytics.mv_top_customers CASCADE;
            
            CREATE MATERIALIZED VIEW analytics.mv_top_customers AS
            SELECT 
                c.customer_id,
                c.first_name,
                c.last_name,
                c.email,
                COUNT(o.order_id) as order_count,
                SUM(o.total_amount) as total_spent,
                ROW_NUMBER() OVER (ORDER BY SUM(o.total_amount) DESC) as rank,
                CURRENT_TIMESTAMP as refresh_time
            FROM staging.customers_staging c
            LEFT JOIN staging.orders_staging o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email
            ORDER BY total_spent DESC
            LIMIT 1000
        """)
        
        # Create indexes on materialized views
        cursor.execute("""
            CREATE INDEX idx_mv_customer_summary_spent ON analytics.mv_customer_summary(total_spent DESC);
            CREATE INDEX idx_mv_sales_by_category_revenue ON analytics.mv_sales_by_category(total_revenue DESC);
            CREATE INDEX idx_mv_top_customers_rank ON analytics.mv_top_customers(rank);
        """)
        
        conn.commit()
        logger.info("Materialized views created successfully")
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 6: DATA QUALITY CHECKS
# ============================================================================

def run_analytics_quality_checks(**context):
    """
    Run quality checks on analytics layer
    """
    logger.info("Running analytics quality checks...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    quality_results = {
        'checks_passed': 0,
        'checks_failed': 0,
        'issues': []
    }
    
    try:
        # Check 1: Fact table row count
        cursor.execute("SELECT COUNT(*) FROM analytics.fact_sales")
        fact_count = cursor.fetchone()[0]
        
        if fact_count > 0:
            quality_results['checks_passed'] += 1
        else:
            quality_results['checks_failed'] += 1
            quality_results['issues'].append('Fact sales table is empty')
        
        # Check 2: Dimension table completeness
        cursor.execute("""
            SELECT COUNT(*) FROM analytics.fact_sales fs
            WHERE fs.customer_key IS NULL OR fs.product_key IS NULL OR fs.date_key IS NULL
        """)
        
        null_keys = cursor.fetchone()[0]
        if null_keys == 0:
            quality_results['checks_passed'] += 1
        else:
            quality_results['checks_failed'] += 1
            quality_results['issues'].append(f'Found {null_keys} records with null dimension keys')
        
        # Check 3: Aggregate consistency
        cursor.execute("""
            SELECT COUNT(*) FROM analytics.customer_metrics
            WHERE total_spent < 0 OR average_order_value < 0
        """)
        
        invalid_metrics = cursor.fetchone()[0]
        if invalid_metrics == 0:
            quality_results['checks_passed'] += 1
        else:
            quality_results['checks_failed'] += 1
            quality_results['issues'].append(f'Found {invalid_metrics} invalid metrics')
        
        logger.info(f"Quality checks completed: {json.dumps(quality_results, indent=2)}")
        push_xcom_data(context['task_instance'], 'quality_results', quality_results)
        
        return quality_results
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# DAG DEFINITION
# ============================================================================

# Stage 1: Build Dimensions
with TaskGroup("stage_1_dimensions", dag=dag) as dimensions_group:
    dim_customer_task = PythonOperator(
        task_id='build_dim_customer',
        python_callable=build_dim_customer,
        provide_context=True,
    )
    
    dim_product_task = PythonOperator(
        task_id='build_dim_product',
        python_callable=build_dim_product,
        provide_context=True,
    )
    
    dim_date_task = PythonOperator(
        task_id='build_dim_date',
        python_callable=build_dim_date,
        provide_context=True,
    )

# Stage 2: Build Facts
with TaskGroup("stage_2_facts", dag=dag) as facts_group:
    fact_sales_task = PythonOperator(
        task_id='build_fact_sales',
        python_callable=build_fact_sales,
        provide_context=True,
    )

# Stage 3: Build Aggregates
with TaskGroup("stage_3_aggregates", dag=dag) as aggregates_group:
    customer_metrics_task = PythonOperator(
        task_id='build_customer_metrics',
        python_callable=build_customer_metrics,
        provide_context=True,
    )
    
    daily_sales_task = PythonOperator(
        task_id='build_daily_sales',
        python_callable=build_daily_sales,
        provide_context=True,
    )
    
    monthly_revenue_task = PythonOperator(
        task_id='build_monthly_revenue',
        python_callable=build_monthly_revenue,
        provide_context=True,
    )
    
    product_performance_task = PythonOperator(
        task_id='build_product_performance',
        python_callable=build_product_performance,
        provide_context=True,
    )

# Stage 4: Build Advanced Metrics
with TaskGroup("stage_4_advanced_metrics", dag=dag) as advanced_group:
    customer_segments_task = PythonOperator(
        task_id='build_customer_segments',
        python_callable=build_customer_segments,
        provide_context=True,
    )
    
    cohort_analysis_task = PythonOperator(
        task_id='build_cohort_analysis',
        python_callable=build_cohort_analysis,
        provide_context=True,
    )

# Stage 5: Materialized Views
materialized_views_task = PythonOperator(
    task_id='create_materialized_views',
    python_callable=create_materialized_views,
    provide_context=True,
)

# Stage 6: Quality Checks
quality_check_task = PythonOperator(
    task_id='run_quality_checks',
    python_callable=run_analytics_quality_checks,
    provide_context=True,
)

# DAG Flow
dimensions_group >> facts_group >> aggregates_group >> advanced_group >> materialized_views_task >> quality_check_task
