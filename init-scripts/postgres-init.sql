-- Create schemas
CREATE SCHEMA IF NOT EXISTS raw_data;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Raw Data Layer
CREATE TABLE IF NOT EXISTS raw_data.customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_data.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES raw_data.customers(customer_id),
    order_date DATE,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_data.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    stock_quantity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_data.order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES raw_data.orders(order_id),
    product_id INTEGER REFERENCES raw_data.products(product_id),
    quantity INTEGER,
    unit_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Staging Layer
CREATE TABLE IF NOT EXISTS staging.customers_staging AS
SELECT * FROM raw_data.customers WHERE 1=0;

CREATE TABLE IF NOT EXISTS staging.orders_staging AS
SELECT * FROM raw_data.orders WHERE 1=0;

-- Analytics Layer
CREATE TABLE IF NOT EXISTS analytics.customer_metrics (
    customer_id INTEGER PRIMARY KEY,
    total_orders INTEGER,
    total_spent DECIMAL(10, 2),
    average_order_value DECIMAL(10, 2),
    last_order_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics.daily_sales (
    sale_date DATE PRIMARY KEY,
    total_sales DECIMAL(10, 2),
    total_orders INTEGER,
    unique_customers INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO raw_data.customers (first_name, last_name, email, phone, country) VALUES
('Jean', 'Dupont', 'jean.dupont@email.com', '+33612345678', 'France'),
('Marie', 'Martin', 'marie.martin@email.com', '+33687654321', 'France'),
('Pierre', 'Bernard', 'pierre.bernard@email.com', '+33698765432', 'France'),
('Sophie', 'Leclerc', 'sophie.leclerc@email.com', '+33645678901', 'France'),
('Luc', 'Moreau', 'luc.moreau@email.com', '+33656789012', 'France');

INSERT INTO raw_data.products (product_name, category, price, stock_quantity) VALUES
('Laptop Pro', 'Electronics', 1299.99, 50),
('Wireless Mouse', 'Electronics', 29.99, 200),
('USB-C Cable', 'Accessories', 9.99, 500),
('Monitor 4K', 'Electronics', 399.99, 30),
('Keyboard Mechanical', 'Electronics', 149.99, 75);

INSERT INTO raw_data.orders (customer_id, order_date, total_amount, status) VALUES
(1, '2024-01-15', 1329.98, 'completed'),
(2, '2024-01-16', 399.99, 'completed'),
(3, '2024-01-17', 179.98, 'pending'),
(1, '2024-01-18', 29.99, 'completed'),
(4, '2024-01-19', 1449.97, 'completed');

INSERT INTO raw_data.order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 1299.99),
(1, 3, 1, 9.99),
(2, 4, 1, 399.99),
(3, 2, 1, 29.99),
(3, 5, 1, 149.99),
(4, 2, 1, 29.99),
(5, 1, 1, 1299.99),
(5, 5, 1, 149.99);

-- Create indexes for performance
CREATE INDEX idx_customers_email ON raw_data.customers(email);
CREATE INDEX idx_orders_customer_id ON raw_data.orders(customer_id);
CREATE INDEX idx_orders_date ON raw_data.orders(order_date);
CREATE INDEX idx_order_items_order_id ON raw_data.order_items(order_id);
CREATE INDEX idx_order_items_product_id ON raw_data.order_items(product_id);

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA raw_data TO datauser;
GRANT ALL PRIVILEGES ON SCHEMA staging TO datauser;
GRANT ALL PRIVILEGES ON SCHEMA analytics TO datauser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA raw_data TO datauser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO datauser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO datauser;
