DROP TABLE IF EXISTS inventory, orders, customers, products, dealers CASCADE;
CREATE TABLE dealers (dealer_id TEXT PRIMARY KEY, dealer_name TEXT NOT NULL, region TEXT NOT NULL);
CREATE TABLE products (product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL, unit_price NUMERIC(14,2) NOT NULL, unit_cost NUMERIC(14,2) NOT NULL, reorder_point INTEGER NOT NULL);
CREATE TABLE customers (customer_id TEXT PRIMARY KEY, segment TEXT NOT NULL);
CREATE TABLE orders (order_id TEXT PRIMARY KEY, order_date DATE NOT NULL, dealer_id TEXT NOT NULL REFERENCES dealers, customer_id TEXT NOT NULL REFERENCES customers, product_id TEXT NOT NULL REFERENCES products, quantity INTEGER NOT NULL CHECK (quantity > 0), unit_price NUMERIC(14,2) NOT NULL, unit_cost NUMERIC(14,2) NOT NULL, discount_rate NUMERIC(5,2) NOT NULL, status TEXT NOT NULL CHECK (status IN ('Fulfilled', 'Pending', 'Cancelled')), fulfilled_date DATE);
CREATE TABLE inventory (dealer_id TEXT NOT NULL REFERENCES dealers, product_id TEXT NOT NULL REFERENCES products, snapshot_date DATE NOT NULL, on_hand_units INTEGER NOT NULL, reorder_point INTEGER NOT NULL, PRIMARY KEY (dealer_id, product_id, snapshot_date));
CREATE INDEX idx_orders_date ON orders (order_date);
CREATE INDEX idx_orders_dealer ON orders (dealer_id);
CREATE INDEX idx_orders_product ON orders (product_id);
