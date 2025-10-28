import csv
import random
from datetime import datetime, timedelta
import os

os.makedirs('data', exist_ok=True)

NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 100
NUM_ORDERS = 10000

first_names = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Luc', 'Anne', 'Marc', 'Claire', 'Paul', 'Julie']
last_names = ['Dupont', 'Martin', 'Bernard', 'Leclerc', 'Moreau', 'Simon', 'Laurent', 'Lefebvre']
countries = ['France', 'Germany', 'Italy', 'Spain', 'Belgium', 'Netherlands', 'Switzerland', 'Austria']
product_names = ['Laptop Pro', 'Monitor 4K', 'Keyboard', 'Mouse', 'USB Cable', 'Headphones', 'Speaker', 'Webcam', 'Router', 'SSD']
categories = ['Electronics', 'Accessories', 'Peripherals', 'Storage', 'Networking']
statuses = ['completed', 'pending', 'cancelled', 'shipped', 'delivered']

print('Generating customers.csv...')
with open('data/customers.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['customer_id', 'first_name', 'last_name', 'email', 'phone', 'country', 'created_at'])
    for i in range(1, NUM_CUSTOMERS + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f'{first.lower()}.{last.lower()}{i}@email.com'
        phone = f'+33{random.randint(600000000, 799999999)}'
        country = random.choice(countries)
        created = (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        writer.writerow([i, first, last, email, phone, country, created])
print(f'✓ Created {NUM_CUSTOMERS} customers')

print('Generating products.csv...')
with open('data/products.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['product_id', 'product_name', 'category', 'price', 'stock_quantity', 'created_at'])
    for i in range(1, NUM_PRODUCTS + 1):
        name = random.choice(product_names)
        cat = random.choice(categories)
        price = round(random.uniform(9.99, 1999.99), 2)
        stock = random.randint(0, 500)
        created = (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        writer.writerow([i, name, cat, price, stock, created])
print(f'✓ Created {NUM_PRODUCTS} products')

print('Generating orders.csv...')
customer_ids = list(range(1, NUM_CUSTOMERS + 1))
with open('data/orders.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id', 'customer_id', 'order_date', 'total_amount', 'status', 'created_at'])
    for i in range(1, NUM_ORDERS + 1):
        cust_id = random.choice(customer_ids)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 365))).date()
        amount = round(random.uniform(10, 5000), 2)
        status = random.choice(statuses)
        created = (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        writer.writerow([i, cust_id, order_date, amount, status, created])
        if i % 2000 == 0:
            print(f'  {i}/{NUM_ORDERS}...')
print(f'✓ Created {NUM_ORDERS} orders')

print('Generating order_items.csv...')
product_ids = list(range(1, NUM_PRODUCTS + 1))
item_id = 1
with open('data/order_items.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'created_at'])
    for order_id in range(1, NUM_ORDERS + 1):
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            prod_id = random.choice(product_ids)
            qty = random.randint(1, 10)
            price = round(random.uniform(9.99, 1999.99), 2)
            created = (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
            writer.writerow([item_id, order_id, prod_id, qty, price, created])
            item_id += 1
        if order_id % 2000 == 0:
            print(f'  {order_id}/{NUM_ORDERS}...')
print(f'✓ Created {item_id - 1} order items')

print('\n✓ All CSV files created successfully!')
print('\nFiles created:')
print('  - data/customers.csv (1000 rows)')
print('  - data/products.csv (100 rows)')
print('  - data/orders.csv (10000 rows)')
print('  - data/order_items.csv (~40000 rows)')
