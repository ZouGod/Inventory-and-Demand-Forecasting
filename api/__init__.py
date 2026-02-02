"""
Vercel Serverless Function - Flask Wrapper
Converts Flask app to work with Vercel's serverless environment
"""

from flask import Flask, jsonify, request
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models_handler import ModelHandler
from api.data_processor import DataProcessor

app = Flask(__name__)

# Initialize handlers
model_handler = ModelHandler()
data_processor = DataProcessor()

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Wing Shop Random Forest Forecaster',
        'models_loaded': model_handler.is_ready()
    }), 200

# ============================================================================
# FORECAST ENDPOINTS
# ============================================================================

@app.route('/api/forecast', methods=['POST'])
def forecast():
    """
    Generate forecast using Random Forest model
    Expected JSON: {'days': 7, 'product': 'category_name', 'store': 44}
    """
    try:
        data = request.get_json() or {}
        days = data.get('days', 7)
        product = data.get('product', 'all')
        store = data.get('store', 44)
        
        if not model_handler.is_ready():
            return jsonify({'error': 'Model not loaded'}), 503
        
        forecast_data = model_handler.predict(
            days=days,
            product=product,
            store=store
        )
        
        return jsonify({
            'success': True,
            'forecast': forecast_data,
            'days': days,
            'product': product
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/forecast/bulk', methods=['POST'])
def forecast_bulk():
    """
    Generate forecasts for multiple products
    Expected JSON: {'days': 7, 'products': ['rice', 'water', 'oil']}
    """
    try:
        data = request.get_json() or {}
        days = data.get('days', 7)
        products = data.get('products', [])
        
        if not model_handler.is_ready():
            return jsonify({'error': 'Model not loaded'}), 503
        
        forecasts = {}
        for product in products:
            forecasts[product] = model_handler.predict(days=days, product=product)
        
        return jsonify({
            'success': True,
            'forecasts': forecasts,
            'days': days
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# DATA ENDPOINTS
# ============================================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get available products"""
    try:
        products = data_processor.get_products()
        return jsonify({
            'success': True,
            'products': products
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/historical', methods=['GET'])
def get_historical():
    """Get historical sales data"""
    try:
        days = request.args.get('days', 30, type=int)
        product = request.args.get('product', 'all')
        
        historical = data_processor.get_historical(days=days, product=product)
        
        return jsonify({
            'success': True,
            'historical': historical,
            'days': days,
            'product': product
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get performance metrics"""
    try:
        metrics = model_handler.get_metrics()
        return jsonify({
            'success': True,
            'metrics': metrics
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=False, port=5000)

# Export app for Vercel
wsgi = app
