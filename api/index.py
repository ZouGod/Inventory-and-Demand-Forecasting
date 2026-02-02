"""
Vercel Serverless Entry Point
This file serves as the WSGI application for Vercel
"""

from flask import Flask, jsonify, request
import os
import sys
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models_handler import ModelHandler
from api.data_processor import DataProcessor

app = Flask(__name__)

# Initialize handlers
model_handler = ModelHandler()
data_processor = DataProcessor()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'})

# Forecast endpoint
@app.route('/api/forecast', methods=['POST'])
def forecast():
    """Generate forecast for a product"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        days = data.get('days', 7)
        
        if not product_id:
            return jsonify({'error': 'product_id is required'}), 400
        
        forecast_result = model_handler.predict(product_id, days)
        return jsonify(forecast_result)
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

# Products endpoint
@app.route('/api/products', methods=['GET'])
def products():
    """Get list of available products"""
    try:
        products_list = data_processor.get_products()
        return jsonify({'products': products_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Historical data endpoint
@app.route('/api/historical', methods=['GET'])
def historical():
    """Get historical sales data"""
    try:
        product_id = request.args.get('product_id')
        if not product_id:
            return jsonify({'error': 'product_id is required'}), 400
        
        historical_data = data_processor.get_historical(product_id)
        return jsonify({'data': historical_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Metrics endpoint
@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Get model performance metrics"""
    try:
        model_metrics = model_handler.get_metrics()
        return jsonify(model_metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Root endpoint - serve static files
@app.route('/', methods=['GET'])
def index():
    """Serve main dashboard"""
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'index.html'), 'r') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': f'Could not load index.html: {str(e)}'}), 500

@app.route('/<path:path>', methods=['GET'])
def static_files(path):
    """Serve static files"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), '..', path)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500
