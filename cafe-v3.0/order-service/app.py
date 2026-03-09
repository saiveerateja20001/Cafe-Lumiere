from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor, Json
import os
from datetime import datetime
import time
import json

app = Flask(__name__)
CORS(app)

# Version Info
APP_VERSION = "3.0"
APP_NAME = "Café Lumière Order Service v3.0"

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'cafe_lumiere'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}

def get_db_connection():
    """Create database connection with retry logic"""
    max_retries = 10
    retry_delay = 3
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.set_session(autocommit=False)
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed, retrying in {retry_delay}s... ({attempt + 1}/{max_retries})")
                print(f"Error: {e}")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create orders table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            order_number VARCHAR(20) UNIQUE NOT NULL,
            customer_name VARCHAR(100) NOT NULL,
            items JSONB NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) DEFAULT 'ordered',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint with database connectivity check"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return jsonify({
            'status': 'healthy', 
            'service': 'order-service',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'service': 'order-service',
            'database': 'disconnected',
            'error': str(e)
        }), 503

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.json
        customer_name = data.get('customer_name')
        items = data.get('items', [])
        total_price = data.get('total_price', 0)
        
        if not customer_name or not items:
            return jsonify({'error': 'Customer name and items are required'}), 400
        
        # Generate order number
        order_number = f"CL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Convert items list to JSON properly
        items_json = Json(items)
        
        cur.execute('''
            INSERT INTO orders (order_number, customer_name, items, total_price, status)
            VALUES (%s, %s, %s, %s, 'ordered')
            RETURNING *
        ''', (order_number, customer_name, items_json, total_price))
        
        order = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        # Convert order to dict and handle JSON serialization
        order_dict = dict(order)
        if isinstance(order_dict.get('created_at'), datetime):
            order_dict['created_at'] = order_dict['created_at'].isoformat()
        if isinstance(order_dict.get('updated_at'), datetime):
            order_dict['updated_at'] = order_dict['updated_at'].isoformat()
        
        return jsonify(order_dict), 201
    
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        status = request.args.get('status')
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        if status:
            cur.execute('SELECT * FROM orders WHERE status = %s ORDER BY created_at DESC', (status,))
        else:
            cur.execute('SELECT * FROM orders ORDER BY created_at DESC')
        
        orders = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert to list of dicts with datetime serialization
        orders_list = []
        for order in orders:
            order_dict = dict(order)
            if isinstance(order_dict.get('created_at'), datetime):
                order_dict['created_at'] = order_dict['created_at'].isoformat()
            if isinstance(order_dict.get('updated_at'), datetime):
                order_dict['updated_at'] = order_dict['updated_at'].isoformat()
            orders_list.append(order_dict)
        
        return jsonify(orders_list), 200
    
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    """Get specific order by order number"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('SELECT * FROM orders WHERE order_number = %s', (order_number,))
        order = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if order:
            order_dict = dict(order)
            if isinstance(order_dict.get('created_at'), datetime):
                order_dict['created_at'] = order_dict['created_at'].isoformat()
            if isinstance(order_dict.get('updated_at'), datetime):
                order_dict['updated_at'] = order_dict['updated_at'].isoformat()
            return jsonify(order_dict), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    
    except Exception as e:
        print(f"Error fetching order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<order_number>', methods=['PUT'])
def update_order_status(order_number):
    """Update order status"""
    try:
        data = request.json
        new_status = data.get('status')
        
        if new_status not in ['ordered', 'preparing', 'ready', 'served']:
            return jsonify({'error': 'Invalid status'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute('''
            UPDATE orders 
            SET status = %s, updated_at = CURRENT_TIMESTAMP
            WHERE order_number = %s
            RETURNING *
        ''', (new_status, order_number))
        
        order = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if order:
            order_dict = dict(order)
            if isinstance(order_dict.get('created_at'), datetime):
                order_dict['created_at'] = order_dict['created_at'].isoformat()
            if isinstance(order_dict.get('updated_at'), datetime):
                order_dict['updated_at'] = order_dict['updated_at'].isoformat()
            return jsonify(order_dict), 200
        else:
            return jsonify({'error': 'Order not found'}), 404
    
    except Exception as e:
        print(f"Error updating order: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)
