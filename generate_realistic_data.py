import csv
import random
from datetime import datetime, timedelta
import os

os.makedirs('data', exist_ok=True)

# Realistic data
FIRST_NAMES = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Luc', 'Anne', 'Marc', 'Claire', 'Paul', 'Julie',
               'Thomas', 'Isabelle', 'Laurent', 'Nathalie', 'Michel', 'Francoise', 'Jacques', 'Monique',
               'Philippe', 'Sylvie', 'Alain', 'Martine', 'Bernard', 'Danielle', 'Serge', 'Jacqueline',
               'David', 'Christine', 'Christian', 'Veronique', 'Robert', 'Dominique', 'Joseph', 'Helene',
               'Richard', 'Brigitte', 'Charles', 'Micheline', 'Andre', 'Josette', 'Georges', 'Yvette']

LAST_NAMES = ['Dupont', 'Martin', 'Bernard', 'Leclerc', 'Moreau', 'Simon', 'Laurent', 'Lefebvre',
              'Michel', 'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier', 'Morel',
              'Girard', 'Andre', 'Lefevre', 'Blanc', 'Bonnet', 'Fontaine', 'Chevalier', 'Renard',
              'Gaillard', 'Fabre', 'Caron', 'Clement', 'Gauthier', 'Perrin', 'Perrot', 'Petit',
              'Picard', 'Piron', 'Poulain', 'Poullet', 'Poupard', 'Poussin', 'Praud', 'Precheur']

COUNTRIES = ['France', 'Germany', 'Italy', 'Spain', 'Belgium', 'Netherlands', 'Switzerland', 'Austria',
             'Poland', 'Portugal', 'Greece', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Ireland',
             'United Kingdom', 'Czech Republic', 'Hungary', 'Romania']

# Realistic products with categories and price ranges
PRODUCTS = {
    'Laptops': [
        ('MacBook Pro 16"', 2499.99),
        ('MacBook Air M2', 1299.99),
        ('Dell XPS 15', 1899.99),
        ('Dell XPS 13', 999.99),
        ('HP Pavilion 15', 749.99),
        ('Lenovo ThinkPad X1', 1299.99),
        ('ASUS VivoBook 15', 599.99),
        ('Acer Aspire 5', 699.99),
    ],
    'Desktops': [
        ('iMac 27"', 1999.99),
        ('Mac Mini M2', 699.99),
        ('Dell OptiPlex 7090', 1299.99),
        ('HP Pavilion Desktop', 899.99),
        ('Lenovo ThinkCentre', 799.99),
    ],
    'Monitors': [
        ('LG UltraWide 34"', 799.99),
        ('Dell U2723DE 27"', 599.99),
        ('ASUS ProArt 32"', 1299.99),
        ('BenQ SW240 24"', 499.99),
        ('LG 27UP550 4K', 699.99),
        ('Dell S2722DC 27"', 549.99),
    ],
    'Keyboards': [
        ('Logitech MX Keys', 99.99),
        ('Apple Magic Keyboard', 149.99),
        ('Corsair K95 Platinum', 199.99),
        ('Keychron K8 Pro', 129.99),
        ('Ducky One 3', 179.99),
        ('SteelSeries Apex Pro', 249.99),
    ],
    'Mice': [
        ('Logitech MX Master 3S', 99.99),
        ('Apple Magic Mouse', 79.99),
        ('Corsair Dark Core RGB', 69.99),
        ('Razer DeathAdder V3', 69.99),
        ('SteelSeries Rival 3', 29.99),
        ('Logitech G Pro X', 129.99),
    ],
    'Monitors_Accessories': [
        ('USB-C Cable 2m', 19.99),
        ('HDMI 2.1 Cable', 24.99),
        ('DisplayPort Cable', 29.99),
        ('Monitor Arm', 149.99),
        ('Monitor Stand Riser', 49.99),
    ],
    'Storage': [
        ('Samsung 990 Pro 2TB', 249.99),
        ('WD Black SN850X 1TB', 129.99),
        ('Crucial P5 Plus 1TB', 99.99),
        ('SK Hynix Platinum P41 1TB', 119.99),
        ('Seagate Barracuda 4TB', 79.99),
        ('WD Blue 2TB', 49.99),
    ],
    'Peripherals': [
        ('Logitech Webcam C920', 79.99),
        ('Razer Kiyo Pro', 199.99),
        ('Blue Yeti Microphone', 99.99),
        ('Audio-Technica AT2020', 149.99),
        ('Shure SM7B', 399.99),
        ('Sony WH-1000XM5 Headphones', 379.99),
    ],
    'Networking': [
        ('ASUS RT-AX88U Router', 299.99),
        ('Netgear Nighthawk AX12', 199.99),
        ('TP-Link Archer AX6000', 149.99),
        ('Ubiquiti UniFi 6 Pro', 229.99),
        ('Netgear Mesh WiFi 6', 179.99),
    ],
    'Power': [
        ('Corsair RM1000x 1000W', 179.99),
        ('EVGA SuperNOVA 850W', 129.99),
        ('Seasonic Focus GX 750W', 119.99),
        ('Anker PowerCore 26800', 49.99),
        ('Belkin USB-C PD Charger', 79.99),
    ]
}

ORDER_STATUSES = ['completed', 'pending', 'shipped', 'delivered', 'cancelled', 'processing', 'on_hold']

# Customer segments for realistic behavior
CUSTOMER_SEGMENTS = {
    'premium': {'probability': 0.15, 'avg_order_value': 1500, 'order_frequency': 0.8},
    'regular': {'probability': 0.50, 'avg_order_value': 400, 'order_frequency': 0.5},
    'budget': {'probability': 0.35, 'avg_order_value': 150, 'order_frequency': 0.3},
}

print("=" * 70)
print("GENERATING REALISTIC PRODUCTION DATA")
print("=" * 70)

# Generate Customers with segments
print("\n1. Generating customers.csv (1000 customers)...")
customers = []
customer_segments = {}

with open('data/customers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['customer_id', 'first_name', 'last_name', 'email', 'phone', 'country', 'segment', 'created_at'])
    
    for i in range(1, 1001):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        email = f"{first_name.lower()}.{last_name.lower()}{i}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'company.com'])}"
        phone = f"+33{random.randint(600000000, 799999999)}"
        country = random.choice(COUNTRIES)
        
        # Assign segment
        rand = random.random()
        if rand < CUSTOMER_SEGMENTS['premium']['probability']:
            segment = 'premium'
        elif rand < CUSTOMER_SEGMENTS['premium']['probability'] + CUSTOMER_SEGMENTS['regular']['probability']:
            segment = 'regular'
        else:
            segment = 'budget'
        
        customer_segments[i] = segment
        created_at = (datetime.now() - timedelta(days=random.randint(30, 730))).isoformat()
        
        writer.writerow([i, first_name, last_name, email, phone, country, segment, created_at])

print("   ✓ Created 1000 customers with segments")

# Generate Products
print("\n2. Generating products.csv (100+ products)...")
product_id = 1
product_list = []

with open('data/products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['product_id', 'product_name', 'category', 'price', 'stock_quantity', 'created_at'])
    
    for category, products in PRODUCTS.items():
        for product_name, price in products:
            stock = random.randint(5, 500)
            created_at = (datetime.now() - timedelta(days=random.randint(30, 730))).isoformat()
            writer.writerow([product_id, product_name, category, price, stock, created_at])
            product_list.append((product_id, price))
            product_id += 1

print(f"   ✓ Created {product_id - 1} products across 10 categories")

# Generate Orders with realistic patterns
print("\n3. Generating orders.csv (10000 orders)...")
order_dates = []

with open('data/orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id', 'customer_id', 'order_date', 'total_amount', 'status', 'created_at'])
    
    for order_id in range(1, 10001):
        # Select customer with segment-based probability
        customer_id = random.randint(1, 1000)
        segment = customer_segments[customer_id]
        
        # Generate order based on segment
        segment_data = CUSTOMER_SEGMENTS[segment]
        
        # Realistic order value with variance
        base_value = segment_data['avg_order_value']
        total_amount = round(random.gauss(base_value, base_value * 0.5), 2)
        total_amount = max(10, total_amount)  # Minimum order value
        
        # Order date distribution (more recent orders)
        days_ago = int(random.expovariate(1/180))  # Exponential distribution
        order_date = (datetime.now() - timedelta(days=min(days_ago, 730))).date()
        order_dates.append(order_date)
        
        # Status distribution (realistic)
        status_rand = random.random()
        if status_rand < 0.70:
            status = 'completed'
        elif status_rand < 0.85:
            status = 'delivered'
        elif status_rand < 0.92:
            status = 'shipped'
        elif status_rand < 0.97:
            status = 'pending'
        else:
            status = 'cancelled'
        
        created_at = (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat()
        
        writer.writerow([order_id, customer_id, order_date, total_amount, status, created_at])
        
        if order_id % 2000 == 0:
            print(f"   ✓ Generated {order_id}/10000 orders...")

print("   ✓ Created 10000 orders")

# Generate Order Items with realistic basket composition
print("\n4. Generating order_items.csv (~35000 items)...")
item_id = 1

with open('data/order_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'created_at'])
    
    for order_id in range(1, 10001):
        # Realistic basket size (1-5 items, with most orders having 1-2 items)
        basket_size_rand = random.random()
        if basket_size_rand < 0.50:
            num_items = 1
        elif basket_size_rand < 0.80:
            num_items = 2
        elif basket_size_rand < 0.95:
            num_items = 3
        else:
            num_items = random.randint(4, 5)
        
        for _ in range(num_items):
            product_id, base_price = random.choice(product_list)
            quantity = random.randint(1, 3)
            
            # Realistic pricing (with small variations)
            unit_price = round(base_price * random.uniform(0.95, 1.05), 2)
            
            created_at = (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat()
            
            writer.writerow([item_id, order_id, product_id, quantity, unit_price, created_at])
            item_id += 1
        
        if order_id % 2000 == 0:
            print(f"   ✓ Generated items for {order_id}/10000 orders...")

print(f"   ✓ Created {item_id - 1} order items")

print("\n" + "=" * 70)
print("✓ REALISTIC DATA GENERATION COMPLETE!")
print("=" * 70)
print("\nGenerated Files:")
print("  ✓ data/customers.csv (1000 rows)")
print("  ✓ data/products.csv (60+ rows)")
print("  ✓ data/orders.csv (10000 rows)")
print("  ✓ data/order_items.csv (~35000 rows)")
print("\nData Characteristics:")
print("  • Customer segments: Premium (15%), Regular (50%), Budget (35%)")
print("  • Realistic order values based on customer segment")
print("  • Order status distribution: 70% completed, 15% delivered, etc.")
print("  • Basket composition: 1-5 items per order")
print("  • Date distribution: Exponential (more recent orders)")
print("  • 20 countries represented")
print("  • 10 product categories")
print("\nNext Steps:")
print("  1. Import CSV files into PostgreSQL")
print("  2. Run Airflow ETL pipeline")
print("  3. Check analytics for realistic business metrics")
print("=" * 70)
