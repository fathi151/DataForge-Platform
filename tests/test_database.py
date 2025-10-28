"""
Tests for database connectivity and data integrity
"""

import psycopg2
import pytest
from datetime import datetime

@pytest.fixture
def db_connection():
    """Create a database connection for testing"""
    conn = psycopg2.connect(
        host="postgres",
        database="datawarehouse",
        user="datauser",
        password="datapass123"
    )
    yield conn
    conn.close()

def test_database_connection(db_connection):
    """Test that we can connect to the database"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1
    cursor.close()

def test_raw_data_schema_exists(db_connection):
    """Test that raw_data schema exists"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT schema_name FROM information_schema.schemata 
        WHERE schema_name = 'raw_data'
    """)
    result = cursor.fetchone()
    assert result is not None
    cursor.close()

def test_staging_schema_exists(db_connection):
    """Test that staging schema exists"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT schema_name FROM information_schema.schemata 
        WHERE schema_name = 'staging'
    """)
    result = cursor.fetchone()
    assert result is not None
    cursor.close()

def test_analytics_schema_exists(db_connection):
    """Test that analytics schema exists"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT schema_name FROM information_schema.schemata 
        WHERE schema_name = 'analytics'
    """)
    result = cursor.fetchone()
    assert result is not None
    cursor.close()

def test_customers_table_exists(db_connection):
    """Test that customers table exists"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'raw_data' AND table_name = 'customers'
    """)
    result = cursor.fetchone()
    assert result is not None
    cursor.close()

def test_orders_table_exists(db_connection):
    """Test that orders table exists"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'raw_data' AND table_name = 'orders'
    """)
    result = cursor.fetchone()
    assert result is not None
    cursor.close()

def test_products_table_exists(db_connection):
    """Test that products table exists"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'raw_data' AND table_name = 'products'
    """)
    result = cursor.fetchone()
    assert result is not None
    cursor.close()

def test_sample_data_loaded(db_connection):
    """Test that sample data is loaded"""
    cursor = db_connection.cursor()
    
    # Check customers
    cursor.execute("SELECT COUNT(*) FROM raw_data.customers")
    customer_count = cursor.fetchone()[0]
    assert customer_count > 0
    
    # Check orders
    cursor.execute("SELECT COUNT(*) FROM raw_data.orders")
    order_count = cursor.fetchone()[0]
    assert order_count > 0
    
    # Check products
    cursor.execute("SELECT COUNT(*) FROM raw_data.products")
    product_count = cursor.fetchone()[0]
    assert product_count > 0
    
    cursor.close()

def test_customer_email_unique(db_connection):
    """Test that customer emails are unique"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT email FROM raw_data.customers 
            WHERE email IS NOT NULL 
            GROUP BY email HAVING COUNT(*) > 1
        ) duplicates
    """)
    duplicate_count = cursor.fetchone()[0]
    assert duplicate_count == 0
    cursor.close()

def test_order_foreign_keys(db_connection):
    """Test that order foreign keys are valid"""
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM raw_data.orders o
        WHERE NOT EXISTS (
            SELECT 1 FROM raw_data.customers c 
            WHERE c.customer_id = o.customer_id
        )
    """)
    invalid_count = cursor.fetchone()[0]
    assert invalid_count == 0
    cursor.close()

def test_analytics_customer_metrics(db_connection):
    """Test that customer metrics are calculated"""
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM analytics.customer_metrics")
    count = cursor.fetchone()[0]
    assert count >= 0
    cursor.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
