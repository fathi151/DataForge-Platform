from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import psycopg2

default_args = {
    'owner': 'data-platform',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    'maintenance_pipeline',
    default_args=default_args,
    description='Maintenance tasks for Data Platform',
    schedule_interval='0 3 * * 0',  # Weekly on Sunday at 3 AM
    catchup=False,
)

def vacuum_database():
    """Vacuum and analyze database"""
    print("Running VACUUM and ANALYZE...")
    conn = psycopg2.connect(
        host="postgres",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    cursor.execute("VACUUM ANALYZE")
    print("VACUUM ANALYZE completed")
    
    cursor.close()
    conn.close()

def check_data_quality():
    """Check data quality metrics"""
    print("Checking data quality...")
    conn = psycopg2.connect(
        host="postgres",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    cursor = conn.cursor()
    
    # Check for null values in critical fields
    cursor.execute("""
        SELECT COUNT(*) FROM raw_data.customers WHERE email IS NULL
    """)
    null_emails = cursor.fetchone()[0]
    print(f"Customers with NULL email: {null_emails}")
    
    # Check for duplicate emails
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT email FROM raw_data.customers 
            WHERE email IS NOT NULL 
            GROUP BY email HAVING COUNT(*) > 1
        ) duplicates
    """)
    duplicate_emails = cursor.fetchone()[0]
    print(f"Duplicate emails found: {duplicate_emails}")
    
    cursor.close()
    conn.close()

def generate_report():
    """Generate data platform report"""
    print("Generating platform report...")
    conn = psycopg2.connect(
        host="postgres",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM raw_data.customers")
    total_customers = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM raw_data.orders")
    total_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(total_amount) FROM raw_data.orders")
    total_revenue = cursor.fetchone()[0] or 0
    
    report = f"""
    ===== DATA PLATFORM REPORT =====
    Total Customers: {total_customers}
    Total Orders: {total_orders}
    Total Revenue: ${total_revenue:.2f}
    Report Generated: {datetime.now()}
    ================================
    """
    print(report)
    
    cursor.close()
    conn.close()

# Tasks
vacuum_task = PythonOperator(
    task_id='vacuum_database',
    python_callable=vacuum_database,
    dag=dag,
)

quality_task = PythonOperator(
    task_id='check_data_quality',
    python_callable=check_data_quality,
    dag=dag,
)

report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)

# DAG flow
vacuum_task >> quality_task >> report_task
