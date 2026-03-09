-- ☕ Café Lumière - Database Initialization Script
-- PostgreSQL 15

-- Create database (if running this manually outside of docker-compose)
-- CREATE DATABASE cafe_lumiere;

-- Connect to the database
\c cafe_lumiere

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    items JSONB NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'ordered' CHECK (status IN ('ordered', 'preparing', 'ready', 'served')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on order_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_orders_order_number ON orders(order_number);

-- Create index on status for filtering
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);

-- Create a function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to auto-update updated_at
DROP TRIGGER IF EXISTS update_orders_updated_at ON orders;
CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data (optional - for testing)
-- Uncomment the lines below to add test orders

/*
INSERT INTO orders (order_number, customer_name, items, total_price, status) VALUES
('CL20260129000001', 'Marie Dubois', '[{"id":1,"name":"Espresso","price":3.50,"quantity":2}]'::jsonb, 7.00, 'ordered'),
('CL20260129000002', 'Jean Pierre', '[{"id":2,"name":"Cappuccino","price":4.50,"quantity":1},{"id":5,"name":"Croissant","price":3.25,"quantity":1}]'::jsonb, 7.75, 'preparing'),
('CL20260129000003', 'Sophie Martin', '[{"id":3,"name":"Café Latte","price":4.75,"quantity":1}]'::jsonb, 4.75, 'ready'),
('CL20260129000004', 'Pierre Rousseau', '[{"id":7,"name":"Éclair","price":4.50,"quantity":2},{"id":4,"name":"Americano","price":3.75,"quantity":1}]'::jsonb, 12.75, 'served');
*/

-- Verify table creation
\dt

-- Show table structure
\d orders

-- Display message
SELECT 'Database initialized successfully!' as message;
