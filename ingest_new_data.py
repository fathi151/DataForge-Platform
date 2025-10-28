import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import random
from datetime import datetime, timedelta

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="datawarehouse",
    user="datauser",
    password="datapass123"
)
cursor = conn.cursor()

print("🔄 Generating new data...")

# Generate new customers
new_customers = []
for i in range(100):
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'Robert', 'Lisa', 'James', 'Mary']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    countries = ['USA', 'UK', 'Canada', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands', 'Belgium', 'Sweden']
    segments = ['Premium', 'Standard', 'Basic']
    
    new_customers.append((
        random.choice(first_names),
        random.choice(last_names),
        f"customer{i}@email.com",
        f"+1{random.randint(2000000000, 9999999999)}",
        random.choice(countries),
        random.choice(segments),
        datetime.now()
    ))

# Insert new customers
execute_values(cursor,
    "INSERT INTO raw_data.customers (first_name, last_name, email, phone, country, segment, created_at) VALUES %s",
    new_customers)
conn.commit()
print(f"✅ Inserted {len(new_customers)} new customers")

# Generate new products
new_products = []
product_names = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'USB Hub', 'Desk Lamp', 'Phone Stand', 'Cable']
categories = ['Electronics', 'Accessories', 'Peripherals', 'Audio', 'Networking']

for i in range(20):
    new_products.append((
        f"{random.choice(product_names)} {i}",
        random.choice(categories),
        round(random.uniform(10, 500), 2),
        random.randint(10, 500)
    ))

execute_values(cursor,
    "INSERT INTO raw_data.products (product_name, category, price, stock_quantity) VALUES %s",
    new_products)
conn.commit()
print(f"✅ Inserted {len(new_products)} new products")

# Generate new orders
new_orders = []
for i in range(150):
    customer_id = random.randint(1, 700)  # Mix of old and new customers
    order_date = datetime.now() - timedelta(days=random.randint(0, 30))
    total_amount = round(random.uniform(50, 2000), 2)
    statuses = ['completed', 'pending', 'cancelled', 'shipped']
    
    new_orders.append((
        customer_id,
        order_date.date(),
        total_amount,
        random.choice(statuses),
        datetime.now()
    ))

execute_values(cursor,
    "INSERT INTO raw_data.orders (customer_id, order_date, total_amount, status, created_at) VALUES %s",
    new_orders)
conn.commit()
print(f"✅ Inserted {len(new_orders)} new orders")

# Get the order IDs we just inserted
cursor.execute("SELECT order_id FROM raw_data.orders ORDER BY order_id DESC LIMIT %s", (len(new_orders),))
order_ids = [row[0] for row in cursor.fetchall()]

# Generate new order items
new_order_items = []
for order_id in order_ids:
    num_items = random.randint(1, 5)
    for _ in range(num_items):
        product_id = random.randint(1, 70)  # Mix of old and new products
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10, 500), 2)
        
        new_order_items.append((
            order_id,
            product_id,
            quantity,
            unit_price,
            datetime.now()
        ))

execute_values(cursor,
    "INSERT INTO raw_data.order_items (order_id, product_id, quantity, unit_price, created_at) VALUES %s",
    new_order_items)
conn.commit()
print(f"✅ Inserted {len(new_order_items)} new order items")

# Get updated counts
cursor.execute("SELECT COUNT(*) FROM raw_data.customers")
total_customers = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM raw_data.orders")
total_orders = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM raw_data.products")
total_products = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM raw_data.order_items")
total_order_items = cursor.fetchone()[0]

cursor.close()
conn.close()

print("\n" + "="*50)
print("📊 NEW DATA SUMMARY")
print("="*50)
print(f"Total Customers: {total_customers}")
print(f"Total Orders: {total_orders}")
print(f"Total Products: {total_products}")
print(f"Total Order Items: {total_order_items}")
print("="*50)
print("\n✨ New data ingested successfully!")
print("🔄 Now trigger the Airflow ETL pipeline to process the data")
print("📍 Go to: http://localhost:8080")
print("📍 Find 'etl_pipeline' DAG and click the play button")
