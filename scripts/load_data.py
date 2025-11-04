import pandas as pd
import psycopg2


conn=psycopg2.connect(
    host="localhost",
    database="datawarehouse",
    user="datauser",
    password="datapass123"
)
cursor=conn.cursor()

df = pd.read_csv(r'c:\Users\TUF\Desktop\docker\data\customers.csv')
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO raw_data.customers (first_name, last_name, email, phone, country, segment, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (row['first_name'], row['last_name'], row['email'], row['phone'], row['country'], row.get('segment', 'regular'), row.get('created_at'))
    )

df = pd.read_csv(r'c:\Users\TUF\Desktop\docker\data\products.csv')
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO raw_data.products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)",
        (row['product_name'], row['category'], row['price'], row['stock_quantity'])
    )

df = pd.read_csv(r'c:\Users\TUF\Desktop\docker\data\orders.csv')
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO raw_data.orders (customer_id, order_date, total_amount, status, created_at) VALUES (%s, %s, %s, %s, %s)",
        (row['customer_id'], row['order_date'], row['total_amount'], row['status'], row.get('created_at'))
    )

df = pd.read_csv(r'c:\Users\TUF\Desktop\docker\data\order_items.csv')
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO raw_data.order_items (order_id, product_id, quantity, unit_price, created_at) VALUES (%s, %s, %s, %s, %s)",
        (row['order_id'], row['product_id'], row['quantity'], row['unit_price'], row.get('created_at'))
    )
conn.commit()
cursor.close()
conn.close()
print("Data loaded successfully!")

