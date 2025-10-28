from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import psycopg2
from psycopg2.extras import execute_values

default_args = {
    'owner': 'data-platform',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL Pipeline for Data Platform',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
)

def extract_data():
    """Extract data from raw layer"""
    print("Extracting data from raw_data schema...")
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM raw_data.customers")
    count = cursor.fetchone()[0]
    print(f"Found {count} customers in raw data")
    cursor.close()
    conn.close()

def transform_data():
    """Transform data to staging layer"""
    print("Transforming data to staging layer...")
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    cursor = conn.cursor()
    
    # Clear staging
    cursor.execute("TRUNCATE TABLE staging.customers_staging")
    
    # Transform and load
    cursor.execute("""
        INSERT INTO staging.customers_staging
        SELECT * FROM raw_data.customers
    """)
    
    conn.commit()
    print(f"Transformed {cursor.rowcount} records")
    cursor.close()
    conn.close()

def load_analytics():
    """Load data to analytics layer"""
    print("Loading data to analytics layer...")
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    cursor = conn.cursor()
    
    # Update customer metrics
    cursor.execute("""
        INSERT INTO analytics.customer_metrics (customer_id, total_orders, total_spent, average_order_value, last_order_date)
        SELECT 
            c.customer_id,
            COUNT(o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_spent,
            COALESCE(AVG(o.total_amount), 0) as average_order_value,
            MAX(o.order_date) as last_order_date
        FROM raw_data.customers c
        LEFT JOIN raw_data.orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id
        ON CONFLICT (customer_id) DO UPDATE SET
            total_orders = EXCLUDED.total_orders,
            total_spent = EXCLUDED.total_spent,
            average_order_value = EXCLUDED.average_order_value,
            last_order_date = EXCLUDED.last_order_date
    """)
    
    # Update daily sales
    cursor.execute("""
        INSERT INTO analytics.daily_sales (sale_date, total_sales, total_orders, unique_customers)
        SELECT 
            o.order_date,
            SUM(o.total_amount) as total_sales,
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(DISTINCT o.customer_id) as unique_customers
        FROM raw_data.orders o
        GROUP BY o.order_date
        ON CONFLICT (sale_date) DO UPDATE SET
            total_sales = EXCLUDED.total_sales,
            total_orders = EXCLUDED.total_orders,
            unique_customers = EXCLUDED.unique_customers
    """)
    
    conn.commit()
    print("Analytics layer updated successfully")
    cursor.close()
    conn.close()

# Tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_analytics',
    python_callable=load_analytics,
    dag=dag,
)

# DAG flow
extract_task >> transform_task >> load_task
