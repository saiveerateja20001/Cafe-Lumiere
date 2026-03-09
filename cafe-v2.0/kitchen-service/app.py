from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

app = Flask(__name__)
CORS(app)

# Version Info
APP_VERSION = "2.0"
APP_NAME = "Café Lumière Kitchen Service v2.0"

ORDER_SERVICE_URL = os.environ.get('ORDER_SERVICE_URL', 'http://order-service:5001')

def get_requests_session():
    """Create a requests session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504)
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        # Check if order service is reachable
        session = get_requests_session()
        response = session.get(f'{ORDER_SERVICE_URL}/health', timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'healthy', 'order_service': 'connected'}), 200
        else:
            return jsonify({'status': 'unhealthy', 'order_service': 'unreachable'}), 503
    except:
        return jsonify({'status': 'healthy', 'order_service': 'pending'}), 200

@app.route('/kitchen/orders', methods=['GET'])
def get_kitchen_orders():
    """Get orders that need kitchen attention (ordered, preparing, ready)."""
    try:
        session = get_requests_session()
        response = session.get(f'{ORDER_SERVICE_URL}/orders', timeout=5)
        if response.status_code == 200:
            all_orders = response.json()
            kitchen_orders = [order for order in all_orders if order['status'] in ['ordered', 'preparing', 'ready']]
            return jsonify(kitchen_orders), 200
        else:
            return jsonify({'error': 'Failed to fetch orders'}), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error fetching kitchen orders: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/kitchen/orders/<order_number>/prepare', methods=['PUT'])
def start_preparing(order_number):
    """Start preparing an order."""
    try:
        session = get_requests_session()
        response = session.put(
            f'{ORDER_SERVICE_URL}/orders/{order_number}',
            json={'status': 'preparing'},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to update order', 'details': response.text}), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error starting order preparation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/kitchen/orders/<order_number>/ready', methods=['PUT'])
def mark_ready(order_number):
    """Mark an order as ready."""
    try:
        session = get_requests_session()
        response = session.put(
            f'{ORDER_SERVICE_URL}/orders/{order_number}',
            json={'status': 'ready'},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to update order', 'details': response.text}), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error marking order as ready: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/kitchen/orders/<order_number>/serve', methods=['PUT'])
def serve_order(order_number):
    """Mark an order as served."""
    try:
        session = get_requests_session()
        response = session.put(
            f'{ORDER_SERVICE_URL}/orders/{order_number}',
            json={'status': 'served'},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to update order', 'details': response.text}), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error serving order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/kitchen/orders/<order_number>/start', methods=['POST'])
def start_order_post(order_number):
    """POST endpoint to start preparing an order (wrapper around PUT /prepare)."""
    try:
        session = get_requests_session()
        response = session.put(
            f'{ORDER_SERVICE_URL}/orders/{order_number}',
            json={'status': 'preparing'},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to update order', 'details': response.text}), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error starting order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/kitchen/orders/<order_number>/ready', methods=['POST'])
def ready_order_post(order_number):
    """POST endpoint to mark order as ready (wrapper around PUT /ready)."""
    try:
        session = get_requests_session()
        response = session.put(
            f'{ORDER_SERVICE_URL}/orders/{order_number}',
            json={'status': 'ready'},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to update order', 'details': response.text}), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error marking order ready: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/kitchen/orders/<order_number>/serve', methods=['POST'])
def serve_order_post(order_number):
    """POST endpoint to mark order as served (wrapper around PUT /serve)."""
    try:
        session = get_requests_session()
        response = session.put(
            f'{ORDER_SERVICE_URL}/orders/{order_number}',
            json={'status': 'served'},
            timeout=5
        )
        
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({'error': 'Failed to update order', 'details': response.text}), response.status_code
    
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error serving order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/display/orders', methods=['GET'])
def get_display_orders():
    """Get orders for display board (preparing and ready only)."""
    try:
        session = get_requests_session()
        response = session.get(f'{ORDER_SERVICE_URL}/orders', timeout=5)
        if response.status_code == 200:
            all_orders = response.json()
            display_orders = [order for order in all_orders if order['status'] in ['preparing', 'ready']]
            return jsonify(display_orders), 200
        else:
            return jsonify({'error': 'Failed to fetch orders'}), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to order service'}), 503
    except Exception as e:
        print(f"Error fetching display orders: {e}")
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
    app.run(host='0.0.0.0', port=5002, debug=True)
