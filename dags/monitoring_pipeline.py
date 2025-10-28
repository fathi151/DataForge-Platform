"""
Monitoring & Alerting Pipeline
Tracks pipeline health, data quality, and business metrics
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
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
    'owner': 'data-operations',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email': ['ops-team@company.com'],
}

dag = DAG(
    'monitoring_pipeline',
    default_args=default_args,
    description='Monitor pipeline health, data quality, and business metrics',
    schedule_interval='0 * * * *',  # Every hour
    catchup=False,
    tags=['monitoring', 'operations', 'production'],
    max_active_runs=1,
)

def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)

def push_xcom_data(task_instance, key: str, value):
    """Push data to XCom"""
    task_instance.xcom_push(key=key, value=value)

# ============================================================================
# PIPELINE HEALTH MONITORING
# ============================================================================

def monitor_pipeline_health(**context):
    """
    Monitor Airflow pipeline health and execution metrics
    """
    logger.info("Monitoring pipeline health...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    health_metrics = {
        'timestamp': datetime.now().isoformat(),
        'pipelines': {},
        'alerts': []
    }
    
    try:
        # Get pipeline execution stats for last 24 hours
        cursor.execute("""
            SELECT 
                dag_id,
                COUNT(*) as total_runs,
                SUM(CASE WHEN state = 'success' THEN 1 ELSE 0 END) as successful_runs,
                SUM(CASE WHEN state = 'failed' THEN 1 ELSE 0 END) as failed_runs,
                AVG(EXTRACT(EPOCH FROM (end_date - start_date))) as avg_duration_seconds,
                MAX(end_date) as last_run_time
            FROM airflow.dag_run
            WHERE execution_date >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
            GROUP BY dag_id
        """)
        
        for row in cursor.fetchall():
            dag_id, total, success, failed, avg_duration, last_run = row
            success_rate = (success / total * 100) if total > 0 else 0
            
            health_metrics['pipelines'][dag_id] = {
                'total_runs': total,
                'successful_runs': success,
                'failed_runs': failed,
                'success_rate': round(success_rate, 2),
                'avg_duration_seconds': round(avg_duration, 2) if avg_duration else 0,
                'last_run_time': last_run.isoformat() if last_run else None
            }
            
            # Alert if success rate < 90%
            if success_rate < 90:
                health_metrics['alerts'].append({
                    'severity': 'HIGH',
                    'message': f"Pipeline {dag_id} has {success_rate}% success rate (< 90%)"
                })
        
        logger.info(f"Pipeline health: {json.dumps(health_metrics, indent=2)}")
        push_xcom_data(context['task_instance'], 'health_metrics', health_metrics)
        
        return health_metrics
        
    finally:
        cursor.close()
        conn.close()

def monitor_task_performance(**context):
    """
    Monitor individual task performance
    """
    logger.info("Monitoring task performance...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    performance_metrics = {
        'timestamp': datetime.now().isoformat(),
        'slow_tasks': [],
        'failed_tasks': []
    }
    
    try:
        # Find slow tasks (> 5 minutes average)
        cursor.execute("""
            SELECT 
                dag_id,
                task_id,
                COUNT(*) as run_count,
                AVG(EXTRACT(EPOCH FROM (end_date - start_date))) as avg_duration_seconds,
                MAX(EXTRACT(EPOCH FROM (end_date - start_date))) as max_duration_seconds
            FROM airflow.task_instance
            WHERE execution_date >= CURRENT_TIMESTAMP - INTERVAL '7 days'
            GROUP BY dag_id, task_id
            HAVING AVG(EXTRACT(EPOCH FROM (end_date - start_date))) > 300
            ORDER BY avg_duration_seconds DESC
            LIMIT 10
        """)
        
        for row in cursor.fetchall():
            dag_id, task_id, run_count, avg_duration, max_duration = row
            performance_metrics['slow_tasks'].append({
                'dag_id': dag_id,
                'task_id': task_id,
                'run_count': run_count,
                'avg_duration_seconds': round(avg_duration, 2),
                'max_duration_seconds': round(max_duration, 2)
            })
        
        # Find frequently failing tasks
        cursor.execute("""
            SELECT 
                dag_id,
                task_id,
                COUNT(*) as total_runs,
                SUM(CASE WHEN state = 'failed' THEN 1 ELSE 0 END) as failed_runs,
                ROUND(100.0 * SUM(CASE WHEN state = 'failed' THEN 1 ELSE 0 END) / COUNT(*), 2) as failure_rate
            FROM airflow.task_instance
            WHERE execution_date >= CURRENT_TIMESTAMP - INTERVAL '7 days'
            GROUP BY dag_id, task_id
            HAVING SUM(CASE WHEN state = 'failed' THEN 1 ELSE 0 END) > 0
            ORDER BY failure_rate DESC
            LIMIT 10
        """)
        
        for row in cursor.fetchall():
            dag_id, task_id, total, failed, failure_rate = row
            performance_metrics['failed_tasks'].append({
                'dag_id': dag_id,
                'task_id': task_id,
                'total_runs': total,
                'failed_runs': failed,
                'failure_rate': failure_rate
            })
        
        logger.info(f"Task performance: {json.dumps(performance_metrics, indent=2)}")
        push_xcom_data(context['task_instance'], 'performance_metrics', performance_metrics)
        
        return performance_metrics
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# DATA QUALITY MONITORING
# ============================================================================

def monitor_data_quality(**context):
    """
    Monitor data quality metrics and trends
    """
    logger.info("Monitoring data quality...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    quality_metrics = {
        'timestamp': datetime.now().isoformat(),
        'current_metrics': {},
        'trends': {},
        'alerts': []
    }
    
    try:
        # Get latest quality metrics
        cursor.execute("""
            SELECT 
                table_name,
                metric_name,
                metric_value,
                status
            FROM data_quality.dq_metrics
            WHERE check_date = CURRENT_DATE
            ORDER BY table_name, metric_name
        """)
        
        for row in cursor.fetchall():
            table_name, metric_name, metric_value, status = row
            key = f"{table_name}.{metric_name}"
            quality_metrics['current_metrics'][key] = {
                'value': float(metric_value) if metric_value else 0,
                'status': status
            }
            
            # Alert if status is FAIL
            if status == 'FAIL':
                quality_metrics['alerts'].append({
                    'severity': 'CRITICAL',
                    'message': f"Data quality check failed: {key}"
                })
        
        # Get quality trends (last 7 days)
        cursor.execute("""
            SELECT 
                check_date,
                table_name,
                metric_name,
                AVG(metric_value) as avg_value,
                MIN(metric_value) as min_value,
                MAX(metric_value) as max_value
            FROM data_quality.dq_metrics
            WHERE check_date >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY check_date, table_name, metric_name
            ORDER BY check_date DESC, table_name, metric_name
        """)
        
        for row in cursor.fetchall():
            check_date, table_name, metric_name, avg_val, min_val, max_val = row
            key = f"{table_name}.{metric_name}"
            if key not in quality_metrics['trends']:
                quality_metrics['trends'][key] = []
            
            quality_metrics['trends'][key].append({
                'date': check_date.isoformat(),
                'avg': float(avg_val) if avg_val else 0,
                'min': float(min_val) if min_val else 0,
                'max': float(max_val) if max_val else 0
            })
        
        logger.info(f"Data quality: {json.dumps(quality_metrics, indent=2)}")
        push_xcom_data(context['task_instance'], 'quality_metrics', quality_metrics)
        
        return quality_metrics
        
    finally:
        cursor.close()
        conn.close()

def monitor_data_freshness(**context):
    """
    Monitor how fresh the data is in each layer
    """
    logger.info("Monitoring data freshness...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    freshness_metrics = {
        'timestamp': datetime.now().isoformat(),
        'layers': {},
        'alerts': []
    }
    
    try:
        # Check raw data freshness
        cursor.execute("""
            SELECT 
                'raw_data.customers' as table_name,
                MAX(updated_at) as last_update,
                EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(updated_at))) / 3600 as hours_old
            FROM raw_data.customers
            UNION ALL
            SELECT 
                'raw_data.orders',
                MAX(created_at),
                EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(created_at))) / 3600
            FROM raw_data.orders
            UNION ALL
            SELECT 
                'staging.customers_staging',
                MAX(updated_at),
                EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(updated_at))) / 3600
            FROM staging.customers_staging
            UNION ALL
            SELECT 
                'analytics.customer_metrics',
                MAX(created_at),
                EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(created_at))) / 3600
            FROM analytics.customer_metrics
        """)
        
        for row in cursor.fetchall():
            table_name, last_update, hours_old = row
            freshness_metrics['layers'][table_name] = {
                'last_update': last_update.isoformat() if last_update else None,
                'hours_old': round(hours_old, 2) if hours_old else None
            }
            
            # Alert if data is older than 24 hours
            if hours_old and hours_old > 24:
                freshness_metrics['alerts'].append({
                    'severity': 'HIGH',
                    'message': f"Data in {table_name} is {round(hours_old, 1)} hours old (> 24 hours)"
                })
        
        logger.info(f"Data freshness: {json.dumps(freshness_metrics, indent=2)}")
        push_xcom_data(context['task_instance'], 'freshness_metrics', freshness_metrics)
        
        return freshness_metrics
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# BUSINESS METRICS MONITORING
# ============================================================================

def monitor_business_metrics(**context):
    """
    Monitor key business metrics
    """
    logger.info("Monitoring business metrics...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    business_metrics = {
        'timestamp': datetime.now().isoformat(),
        'daily_metrics': {},
        'customer_metrics': {},
        'product_metrics': {},
        'trends': {}
    }
    
    try:
        # Today's sales metrics
        cursor.execute("""
            SELECT 
                total_sales,
                total_orders,
                unique_customers
            FROM analytics.daily_sales
            WHERE sale_date = CURRENT_DATE
        """)
        
        result = cursor.fetchone()
        if result:
            business_metrics['daily_metrics'] = {
                'total_sales': float(result[0]) if result[0] else 0,
                'total_orders': result[1],
                'unique_customers': result[2]
            }
        
        # Customer metrics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_customers,
                SUM(total_orders) as total_orders,
                SUM(total_spent) as total_revenue,
                AVG(total_spent) as avg_customer_value,
                MAX(total_spent) as max_customer_value
            FROM analytics.customer_metrics
        """)
        
        result = cursor.fetchone()
        if result:
            business_metrics['customer_metrics'] = {
                'total_customers': result[0],
                'total_orders': result[1],
                'total_revenue': float(result[2]) if result[2] else 0,
                'avg_customer_value': float(result[3]) if result[3] else 0,
                'max_customer_value': float(result[4]) if result[4] else 0
            }
        
        # Product metrics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_products,
                SUM(total_sold) as total_units_sold,
                SUM(total_revenue) as total_product_revenue,
                AVG(total_revenue) as avg_product_revenue
            FROM analytics.product_performance
        """)
        
        result = cursor.fetchone()
        if result:
            business_metrics['product_metrics'] = {
                'total_products': result[0],
                'total_units_sold': result[1],
                'total_product_revenue': float(result[2]) if result[2] else 0,
                'avg_product_revenue': float(result[3]) if result[3] else 0
            }
        
        # 7-day trend
        cursor.execute("""
            SELECT 
                sale_date,
                total_sales,
                total_orders,
                unique_customers
            FROM analytics.daily_sales
            WHERE sale_date >= CURRENT_DATE - INTERVAL '7 days'
            ORDER BY sale_date DESC
        """)
        
        business_metrics['trends']['last_7_days'] = []
        for row in cursor.fetchall():
            business_metrics['trends']['last_7_days'].append({
                'date': row[0].isoformat(),
                'total_sales': float(row[1]) if row[1] else 0,
                'total_orders': row[2],
                'unique_customers': row[3]
            })
        
        logger.info(f"Business metrics: {json.dumps(business_metrics, indent=2)}")
        push_xcom_data(context['task_instance'], 'business_metrics', business_metrics)
        
        return business_metrics
        
    finally:
        cursor.close()
        conn.close()

# ============================================================================
# GENERATE MONITORING REPORT
# ============================================================================

def generate_monitoring_report(**context):
    """
    Generate comprehensive monitoring report
    """
    logger.info("Generating monitoring report...")
    
    # Pull all metrics from XCom
    ti = context['task_instance']
    health = ti.xcom_pull(task_ids='monitor_pipeline_health', key='health_metrics')
    performance = ti.xcom_pull(task_ids='monitor_task_performance', key='performance_metrics')
    quality = ti.xcom_pull(task_ids='monitor_data_quality', key='quality_metrics')
    freshness = ti.xcom_pull(task_ids='monitor_data_freshness', key='freshness_metrics')
    business = ti.xcom_pull(task_ids='monitor_business_metrics', key='business_metrics')
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_alerts': 0,
            'critical_alerts': 0,
            'high_alerts': 0
        },
        'sections': {
            'pipeline_health': health,
            'task_performance': performance,
            'data_quality': quality,
            'data_freshness': freshness,
            'business_metrics': business
        }
    }
    
    # Count alerts
    for section in [health, performance, quality, freshness]:
        if section and 'alerts' in section:
            for alert in section['alerts']:
                report['summary']['total_alerts'] += 1
                if alert.get('severity') == 'CRITICAL':
                    report['summary']['critical_alerts'] += 1
                elif alert.get('severity') == 'HIGH':
                    report['summary']['high_alerts'] += 1
    
    logger.info(f"Monitoring report: {json.dumps(report, indent=2)}")
    
    # Store report in database
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS monitoring.reports (
                report_id SERIAL PRIMARY KEY,
                report_date DATE,
                report_time TIMESTAMP,
                report_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT INTO monitoring.reports (report_date, report_time, report_data)
            VALUES (%s, %s, %s)
        """, (datetime.now().date(), datetime.now(), json.dumps(report)))
        
        conn.commit()
        logger.info("Monitoring report stored in database")
        
    finally:
        cursor.close()
        conn.close()
    
    return report

# ============================================================================
# DAG DEFINITION
# ============================================================================

# Pipeline Health Monitoring
with TaskGroup("pipeline_monitoring", dag=dag) as pipeline_group:
    health_task = PythonOperator(
        task_id='monitor_pipeline_health',
        python_callable=monitor_pipeline_health,
        provide_context=True,
    )
    
    performance_task = PythonOperator(
        task_id='monitor_task_performance',
        python_callable=monitor_task_performance,
        provide_context=True,
    )

# Data Quality Monitoring
with TaskGroup("data_quality_monitoring", dag=dag) as quality_group:
    quality_task = PythonOperator(
        task_id='monitor_data_quality',
        python_callable=monitor_data_quality,
        provide_context=True,
    )
    
    freshness_task = PythonOperator(
        task_id='monitor_data_freshness',
        python_callable=monitor_data_freshness,
        provide_context=True,
    )

# Business Metrics Monitoring
business_task = PythonOperator(
    task_id='monitor_business_metrics',
    python_callable=monitor_business_metrics,
    provide_context=True,
)

# Generate Report
report_task = PythonOperator(
    task_id='generate_monitoring_report',
    python_callable=generate_monitoring_report,
    provide_context=True,
)

# DAG Flow
[pipeline_group, quality_group, business_task] >> report_task
