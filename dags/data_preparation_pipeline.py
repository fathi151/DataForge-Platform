"""
Enterprise-Grade Data Preparation Pipeline
Handles data cleaning, validation, deduplication, and enrichment
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple
import json

logger = logging.getLogger(__name__)

# Database connection parameters
DB_CONFIG = {
    'host': 'postgres',
    'database': 'datawarehouse',
    'user': 'datauser',
    'password': 'datapass123'
}

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email': ['data-team@company.com'],
    'execution_timeout': timedelta(hours=2),
}

dag = DAG(
    'data_preparation_pipeline',
    default_args=default_args,
    description='Enterprise Data Preparation with Deep Cleaning & Validation',
    schedule_interval='0 1 * * *',  # Daily at 1 AM
    catchup=False,
    tags=['data-preparation', 'enterprise', 'production'],
    max_active_runs=1,
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)

def log_data_quality_metric(metric_name: str, metric_value: float, table_name: str, status: str):
    """Log data quality metrics to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO data_quality.dq_metrics 
            (check_date, table_name, metric_name, metric_value, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (datetime.now().date(), table_name, metric_name, metric_value, status))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def push_xcom_data(task_instance, key: str, value):
    """Push data to XCom for inter-task communication"""
    task_instance.xcom_push(key=key, value=value)

def pull_xcom_data(task_instance, task_id: str, key: str):
    """Pull data from XCom"""
    return task_instance.xcom_pull(task_ids=task_id, key=key)

# ============================================================================
# STAGE 1: DATA PROFILING & DISCOVERY
# ============================================================================

def profile_raw_data(**context):
    """
    Profile raw data to understand structure, quality, and patterns
    """
    logger.info("Starting data profiling...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    profiling_results = {}
    
    try:
        # Profile customers table
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT customer_id) as unique_customers,
                COUNT(DISTINCT email) as unique_emails,
                COUNT(CASE WHEN email IS NULL THEN 1 END) as null_emails,
                COUNT(CASE WHEN first_name IS NULL THEN 1 END) as null_first_names,
                COUNT(CASE WHEN last_name IS NULL THEN 1 END) as null_last_names,
                COUNT(DISTINCT country) as unique_countries,
                MIN(created_at) as earliest_record,
                MAX(created_at) as latest_record
            FROM raw_data.customers
        """)
        
        result = cursor.fetchone()
        profiling_results['customers'] = {
            'total_records': result[0],
            'unique_customers': result[1],
            'unique_emails': result[2],
            'null_emails': result[3],
            'null_first_names': result[4],
            'null_last_names': result[5],
            'unique_countries': result[6],
            'earliest_record': result[7].isoformat() if result[7] else None,
            'latest_record': result[8].isoformat() if result[8] else None,
        }
        
        # Profile orders table
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT order_id) as unique_orders,
                COUNT(DISTINCT customer_id) as unique_customers,
                COUNT(CASE WHEN total_amount IS NULL THEN 1 END) as null_amounts,
                COUNT(CASE WHEN total_amount <= 0 THEN 1 END) as invalid_amounts,
                COUNT(CASE WHEN status IS NULL THEN 1 END) as null_status,
                MIN(total_amount) as min_amount,
                MAX(total_amount) as max_amount,
                AVG(total_amount) as avg_amount,
                STDDEV(total_amount) as stddev_amount,
                MIN(order_date) as earliest_order,
                MAX(order_date) as latest_order
            FROM raw_data.orders
        """)
        
        result = cursor.fetchone()
        profiling_results['orders'] = {
            'total_records': result[0],
            'unique_orders': result[1],
            'unique_customers': result[2],
            'null_amounts': result[3],
            'invalid_amounts': result[4],
            'null_status': result[5],
            'min_amount': float(result[6]) if result[6] else None,
            'max_amount': float(result[7]) if result[7] else None,
            'avg_amount': float(result[8]) if result[8] else None,
            'stddev_amount': float(result[9]) if result[9] else None,
            'earliest_order': result[10].isoformat() if result[10] else None,
            'latest_order': result[11].isoformat() if result[11] else None,
        }
        
        # Profile products table
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT product_id) as unique_products,
                COUNT(DISTINCT category) as unique_categories,
                COUNT(CASE WHEN price IS NULL THEN 1 END) as null_prices,
                COUNT(CASE WHEN price <= 0 THEN 1 END) as invalid_prices,
                MIN(price) as min_price,
                MAX(price) as max_price,
                AVG(price) as avg_price,
                COUNT(CASE WHEN stock_quantity < 0 THEN 1 END) as negative_stock
            FROM raw_data.products
        """)
        
        result = cursor.fetchone()
        profiling_results['products'] = {
            'total_records': result[0],
            'unique_products': result[1],
            'unique_categories': result[2],
            'null_prices': result[3],
            'invalid_prices': result[4],
            'min_price': float(result[5]) if result[5] else None,
            'max_price': float(result[6]) if result[6] else None,
            'avg_price': float(result[7]) if result[7] else None,
            'negative_stock': result[8],
        }
        
        logger.info(f"Data profiling completed: {json.dumps(profiling_results, indent=2)}")
        
        # Push to XCom for downstream tasks
        push_xcom_data(context['task_instance'], 'profiling_results', profiling_results)
        
        return profiling_results
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 2: DATA VALIDATION
# ============================================================================

def validate_data_quality(**context):
    """
    Comprehensive data quality validation
    """
    logger.info("Starting data quality validation...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    validation_results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }
    
    try:
        # Validation 1: Check for duplicate emails
        cursor.execute("""
            SELECT email, COUNT(*) as count
            FROM raw_data.customers
            WHERE email IS NOT NULL
            GROUP BY email
            HAVING COUNT(*) > 1
        """)
        
        duplicate_emails = cursor.fetchall()
        if duplicate_emails:
            validation_results['warnings'].append({
                'check': 'duplicate_emails',
                'count': len(duplicate_emails),
                'severity': 'HIGH',
                'message': f'Found {len(duplicate_emails)} duplicate email addresses'
            })
        else:
            validation_results['passed'].append('no_duplicate_emails')
        
        # Validation 2: Check for orphaned orders (customer_id not in customers table)
        cursor.execute("""
            SELECT COUNT(*) FROM raw_data.orders o
            WHERE NOT EXISTS (
                SELECT 1 FROM raw_data.customers c 
                WHERE c.customer_id = o.customer_id
            )
        """)
        
        orphaned_orders = cursor.fetchone()[0]
        if orphaned_orders > 0:
            validation_results['failed'].append({
                'check': 'orphaned_orders',
                'count': orphaned_orders,
                'severity': 'CRITICAL',
                'message': f'Found {orphaned_orders} orders with non-existent customers'
            })
        else:
            validation_results['passed'].append('no_orphaned_orders')
        
        # Validation 3: Check for negative amounts
        cursor.execute("""
            SELECT COUNT(*) FROM raw_data.orders
            WHERE total_amount < 0
        """)
        
        negative_amounts = cursor.fetchone()[0]
        if negative_amounts > 0:
            validation_results['failed'].append({
                'check': 'negative_amounts',
                'count': negative_amounts,
                'severity': 'CRITICAL',
                'message': f'Found {negative_amounts} orders with negative amounts'
            })
        else:
            validation_results['passed'].append('no_negative_amounts')
        
        # Validation 4: Check for future dates
        cursor.execute("""
            SELECT COUNT(*) FROM raw_data.orders
            WHERE order_date > CURRENT_DATE
        """)
        
        future_dates = cursor.fetchone()[0]
        if future_dates > 0:
            validation_results['warnings'].append({
                'check': 'future_dates',
                'count': future_dates,
                'severity': 'MEDIUM',
                'message': f'Found {future_dates} orders with future dates'
            })
        else:
            validation_results['passed'].append('no_future_dates')
        
        # Validation 5: Check for invalid email formats
        cursor.execute("""
            SELECT COUNT(*) FROM raw_data.customers
            WHERE email IS NOT NULL 
            AND email NOT LIKE '%@%.%'
        """)
        
        invalid_emails = cursor.fetchone()[0]
        if invalid_emails > 0:
            validation_results['warnings'].append({
                'check': 'invalid_email_format',
                'count': invalid_emails,
                'severity': 'MEDIUM',
                'message': f'Found {invalid_emails} customers with invalid email formats'
            })
        else:
            validation_results['passed'].append('valid_email_formats')
        
        # Validation 6: Check for missing required fields
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN first_name IS NULL OR first_name = '' THEN 1 END) as missing_first_name,
                COUNT(CASE WHEN last_name IS NULL OR last_name = '' THEN 1 END) as missing_last_name,
                COUNT(CASE WHEN email IS NULL OR email = '' THEN 1 END) as missing_email
            FROM raw_data.customers
        """)
        
        result = cursor.fetchone()
        missing_fields = {
            'first_name': result[0],
            'last_name': result[1],
            'email': result[2]
        }
        
        for field, count in missing_fields.items():
            if count > 0:
                validation_results['failed'].append({
                    'check': f'missing_{field}',
                    'count': count,
                    'severity': 'HIGH',
                    'message': f'Found {count} customers with missing {field}'
                })
            else:
                validation_results['passed'].append(f'no_missing_{field}')
        
        logger.info(f"Validation Results: {json.dumps(validation_results, indent=2)}")
        
        # Store validation results
        push_xcom_data(context['task_instance'], 'validation_results', validation_results)
        
        # Log metrics
        log_data_quality_metric('validation_passed', len(validation_results['passed']), 'all_tables', 'PASS')
        log_data_quality_metric('validation_failed', len(validation_results['failed']), 'all_tables', 'FAIL')
        log_data_quality_metric('validation_warnings', len(validation_results['warnings']), 'all_tables', 'WARNING')
        
        # Fail if critical issues found
        if validation_results['failed']:
            raise Exception(f"Critical data quality issues found: {validation_results['failed']}")
        
        return validation_results
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 3: DATA CLEANING
# ============================================================================

def clean_customer_data(**context):
    """
    Clean customer data: trim whitespace, standardize formats, handle nulls
    """
    logger.info("Cleaning customer data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create temporary table for cleaned data
        cursor.execute("""
            DROP TABLE IF EXISTS temp_customers_cleaned;
            
            CREATE TABLE temp_customers_cleaned AS
            SELECT 
                customer_id,
                TRIM(first_name) as first_name,
                TRIM(last_name) as last_name,
                LOWER(TRIM(email)) as email,
                TRIM(phone) as phone,
                UPPER(TRIM(country)) as country,
                created_at,
                updated_at,
                CURRENT_TIMESTAMP as cleaned_at
            FROM raw_data.customers
            WHERE 
                first_name IS NOT NULL AND first_name != ''
                AND last_name IS NOT NULL AND last_name != ''
                AND email IS NOT NULL AND email != ''
                AND email LIKE '%@%.%'
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM temp_customers_cleaned")
        cleaned_count = cursor.fetchone()[0]
        
        logger.info(f"Cleaned {cleaned_count} customer records")
        push_xcom_data(context['task_instance'], 'cleaned_customers_count', cleaned_count)
        
        return cleaned_count
        
    finally:
        cursor.close()
        conn.close()

def clean_order_data(**context):
    """
    Clean order data: validate amounts, standardize status, handle dates
    """
    logger.info("Cleaning order data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_orders_cleaned;
            
            CREATE TABLE temp_orders_cleaned AS
            SELECT 
                order_id,
                customer_id,
                order_date,
                ROUND(total_amount::numeric, 2) as total_amount,
                UPPER(TRIM(COALESCE(status, 'UNKNOWN'))) as status,
                created_at,
                CURRENT_TIMESTAMP as cleaned_at
            FROM raw_data.orders
            WHERE 
                total_amount > 0
                AND order_date <= CURRENT_DATE
                AND customer_id IN (SELECT customer_id FROM temp_customers_cleaned)
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM temp_orders_cleaned")
        cleaned_count = cursor.fetchone()[0]
        
        logger.info(f"Cleaned {cleaned_count} order records")
        push_xcom_data(context['task_instance'], 'cleaned_orders_count', cleaned_count)
        
        return cleaned_count
        
    finally:
        cursor.close()
        conn.close()

def clean_product_data(**context):
    """
    Clean product data: validate prices, standardize categories
    """
    logger.info("Cleaning product data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_products_cleaned;
            
            CREATE TABLE temp_products_cleaned AS
            SELECT 
                product_id,
                TRIM(product_name) as product_name,
                UPPER(TRIM(category)) as category,
                ROUND(price::numeric, 2) as price,
                GREATEST(stock_quantity, 0) as stock_quantity,
                created_at,
                CURRENT_TIMESTAMP as cleaned_at
            FROM raw_data.products
            WHERE 
                product_name IS NOT NULL AND product_name != ''
                AND price > 0
                AND category IS NOT NULL AND category != ''
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM temp_products_cleaned")
        cleaned_count = cursor.fetchone()[0]
        
        logger.info(f"Cleaned {cleaned_count} product records")
        push_xcom_data(context['task_instance'], 'cleaned_products_count', cleaned_count)
        
        return cleaned_count
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 4: DEDUPLICATION
# ============================================================================

def deduplicate_customers(**context):
    """
    Remove duplicate customers, keeping the most recent record
    """
    logger.info("Deduplicating customer data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_customers_deduped;
            
            CREATE TABLE temp_customers_deduped AS
            SELECT DISTINCT ON (email)
                customer_id,
                first_name,
                last_name,
                email,
                phone,
                country,
                created_at,
                updated_at,
                cleaned_at
            FROM temp_customers_cleaned
            ORDER BY email, updated_at DESC
        """)
        
        conn.commit()
        
        cursor.execute("""
            SELECT COUNT(*) FROM temp_customers_cleaned
        """)
        before_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM temp_customers_deduped
        """)
        after_count = cursor.fetchone()[0]
        
        duplicates_removed = before_count - after_count
        logger.info(f"Removed {duplicates_removed} duplicate customer records")
        push_xcom_data(context['task_instance'], 'duplicates_removed_customers', duplicates_removed)
        
        return duplicates_removed
        
    finally:
        cursor.close()
        conn.close()

def deduplicate_orders(**context):
    """
    Remove duplicate orders, keeping the most recent record
    """
    logger.info("Deduplicating order data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_orders_deduped;
            
            CREATE TABLE temp_orders_deduped AS
            SELECT DISTINCT ON (order_id)
                order_id,
                customer_id,
                order_date,
                total_amount,
                status,
                created_at,
                cleaned_at
            FROM temp_orders_cleaned
            ORDER BY order_id, created_at DESC
        """)
        
        conn.commit()
        
        cursor.execute("""
            SELECT COUNT(*) FROM temp_orders_cleaned
        """)
        before_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM temp_orders_deduped
        """)
        after_count = cursor.fetchone()[0]
        
        duplicates_removed = before_count - after_count
        logger.info(f"Removed {duplicates_removed} duplicate order records")
        push_xcom_data(context['task_instance'], 'duplicates_removed_orders', duplicates_removed)
        
        return duplicates_removed
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 5: DATA ENRICHMENT
# ============================================================================

def enrich_customer_data(**context):
    """
    Enrich customer data with calculated fields and reference data
    """
    logger.info("Enriching customer data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_customers_enriched;
            
            CREATE TABLE temp_customers_enriched AS
            SELECT 
                c.customer_id,
                c.first_name,
                c.last_name,
                c.email,
                c.phone,
                c.country,
                c.created_at,
                c.updated_at,
                c.cleaned_at,
                -- Enrichment fields
                COUNT(o.order_id) as total_orders,
                COALESCE(SUM(o.total_amount), 0) as lifetime_value,
                COALESCE(AVG(o.total_amount), 0) as avg_order_value,
                MAX(o.order_date) as last_order_date,
                CASE 
                    WHEN COUNT(o.order_id) = 0 THEN 'NEW'
                    WHEN MAX(o.order_date) < CURRENT_DATE - INTERVAL '90 days' THEN 'INACTIVE'
                    WHEN MAX(o.order_date) < CURRENT_DATE - INTERVAL '30 days' THEN 'AT_RISK'
                    ELSE 'ACTIVE'
                END as customer_status,
                CASE 
                    WHEN COALESCE(SUM(o.total_amount), 0) > 5000 THEN 'VIP'
                    WHEN COALESCE(SUM(o.total_amount), 0) > 1000 THEN 'PREMIUM'
                    WHEN COALESCE(SUM(o.total_amount), 0) > 0 THEN 'REGULAR'
                    ELSE 'PROSPECT'
                END as customer_segment,
                CURRENT_TIMESTAMP as enriched_at
            FROM temp_customers_deduped c
            LEFT JOIN temp_orders_deduped o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone, 
                     c.country, c.created_at, c.updated_at, c.cleaned_at
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM temp_customers_enriched")
        enriched_count = cursor.fetchone()[0]
        
        logger.info(f"Enriched {enriched_count} customer records")
        push_xcom_data(context['task_instance'], 'enriched_customers_count', enriched_count)
        
        return enriched_count
        
    finally:
        cursor.close()
        conn.close()

def enrich_order_data(**context):
    """
    Enrich order data with product information and calculated metrics
    """
    logger.info("Enriching order data...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_orders_enriched;
            
            CREATE TABLE temp_orders_enriched AS
            SELECT 
                o.order_id,
                o.customer_id,
                o.order_date,
                o.total_amount,
                o.status,
                o.created_at,
                o.cleaned_at,
                -- Enrichment fields
                EXTRACT(YEAR FROM o.order_date) as order_year,
                EXTRACT(MONTH FROM o.order_date) as order_month,
                EXTRACT(QUARTER FROM o.order_date) as order_quarter,
                TO_CHAR(o.order_date, 'Day') as order_day_of_week,
                CASE 
                    WHEN o.total_amount > 1000 THEN 'HIGH_VALUE'
                    WHEN o.total_amount > 500 THEN 'MEDIUM_VALUE'
                    ELSE 'LOW_VALUE'
                END as order_value_category,
                CASE 
                    WHEN o.status = 'COMPLETED' THEN 1
                    ELSE 0
                END as is_completed,
                CURRENT_TIMESTAMP as enriched_at
            FROM temp_orders_deduped o
        """)
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM temp_orders_enriched")
        enriched_count = cursor.fetchone()[0]
        
        logger.info(f"Enriched {enriched_count} order records")
        push_xcom_data(context['task_instance'], 'enriched_orders_count', enriched_count)
        
        return enriched_count
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 6: LOAD TO STAGING
# ============================================================================

def load_to_staging(**context):
    """
    Load cleaned and enriched data to staging layer
    """
    logger.info("Loading data to staging layer...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Truncate staging tables
        cursor.execute("TRUNCATE TABLE staging.customers_staging")
        cursor.execute("TRUNCATE TABLE staging.orders_staging")
        
        # Load customers
        cursor.execute("""
            INSERT INTO staging.customers_staging
            SELECT 
                customer_id, first_name, last_name, email, phone, country,
                created_at, updated_at
            FROM temp_customers_enriched
        """)
        
        customers_loaded = cursor.rowcount
        
        # Load orders
        cursor.execute("""
            INSERT INTO staging.orders_staging
            SELECT 
                order_id, customer_id, order_date, total_amount, status, created_at
            FROM temp_orders_enriched
        """)
        
        orders_loaded = cursor.rowcount
        
        conn.commit()
        
        logger.info(f"Loaded {customers_loaded} customers and {orders_loaded} orders to staging")
        push_xcom_data(context['task_instance'], 'staging_load_summary', {
            'customers': customers_loaded,
            'orders': orders_loaded
        })
        
        return {'customers': customers_loaded, 'orders': orders_loaded}
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# STAGE 7: CLEANUP
# ============================================================================

def cleanup_temp_tables(**context):
    """
    Clean up temporary tables
    """
    logger.info("Cleaning up temporary tables...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DROP TABLE IF EXISTS temp_customers_cleaned;
            DROP TABLE IF EXISTS temp_customers_deduped;
            DROP TABLE IF EXISTS temp_customers_enriched;
            DROP TABLE IF EXISTS temp_orders_cleaned;
            DROP TABLE IF EXISTS temp_orders_deduped;
            DROP TABLE IF EXISTS temp_orders_enriched;
            DROP TABLE IF EXISTS temp_products_cleaned;
        """)
        
        conn.commit()
        logger.info("Temporary tables cleaned up")
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# DAG DEFINITION
# ============================================================================

# Stage 1: Profiling & Discovery
with TaskGroup("stage_1_profiling", dag=dag) as profiling_group:
    profile_task = PythonOperator(
        task_id='profile_raw_data',
        python_callable=profile_raw_data,
        provide_context=True,
    )

# Stage 2: Validation
with TaskGroup("stage_2_validation", dag=dag) as validation_group:
    validate_task = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality,
        provide_context=True,
    )

# Stage 3: Cleaning
with TaskGroup("stage_3_cleaning", dag=dag) as cleaning_group:
    clean_customers_task = PythonOperator(
        task_id='clean_customers',
        python_callable=clean_customer_data,
        provide_context=True,
    )
    
    clean_orders_task = PythonOperator(
        task_id='clean_orders',
        python_callable=clean_order_data,
        provide_context=True,
    )
    
    clean_products_task = PythonOperator(
        task_id='clean_products',
        python_callable=clean_product_data,
        provide_context=True,
    )

# Stage 4: Deduplication
with TaskGroup("stage_4_deduplication", dag=dag) as dedup_group:
    dedup_customers_task = PythonOperator(
        task_id='deduplicate_customers',
        python_callable=deduplicate_customers,
        provide_context=True,
    )
    
    dedup_orders_task = PythonOperator(
        task_id='deduplicate_orders',
        python_callable=deduplicate_orders,
        provide_context=True,
    )

# Stage 5: Enrichment
with TaskGroup("stage_5_enrichment", dag=dag) as enrichment_group:
    enrich_customers_task = PythonOperator(
        task_id='enrich_customers',
        python_callable=enrich_customer_data,
        provide_context=True,
    )
    
    enrich_orders_task = PythonOperator(
        task_id='enrich_orders',
        python_callable=enrich_order_data,
        provide_context=True,
    )

# Stage 6: Load to Staging
load_staging_task = PythonOperator(
    task_id='load_to_staging',
    python_callable=load_to_staging,
    provide_context=True,
)

# Stage 7: Cleanup
cleanup_task = PythonOperator(
    task_id='cleanup_temp_tables',
    python_callable=cleanup_temp_tables,
    provide_context=True,
)

# DAG Flow
profiling_group >> validation_group >> cleaning_group >> dedup_group >> enrichment_group >> load_staging_task >> cleanup_task
