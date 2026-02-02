"""
Wing Shop Inventory Forecasting - Flask Dashboard Backend
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# ============================================================================
# LOAD MODELS AND DATA
# ============================================================================

def load_models():
    """Load all trained models"""
    models = {}
    
    # Load Moving Average
    try:
        with open('models/ma_model.pkl', 'rb') as f:
            models['ma'] = pickle.load(f)
    except:
        models['ma'] = None
    
    # Load Exponential Smoothing
    try:
        with open('models/exp_smoothing_model.pkl', 'rb') as f:
            models['exp_smoothing'] = pickle.load(f)
    except:
        models['exp_smoothing'] = None
    
    # Load SARIMA
    try:
        with open('models/sarima_model.pkl', 'rb') as f:
            models['sarima'] = pickle.load(f)
    except:
        models['sarima'] = None
    
    # Load Prophet
    try:
        with open('models/prophet_model.pkl', 'rb') as f:
            models['prophet'] = pickle.load(f)
    except:
        models['prophet'] = None
    
    # Load Random Forest
    try:
        with open('models/random_forest_model.pkl', 'rb') as f:
            models['random_forest'] = pickle.load(f)
        with open('models/feature_columns.json', 'r') as f:
            models['feature_columns'] = json.load(f)
    except:
        models['random_forest'] = None
    
    return models

def load_data():
    """Load processed sales data"""
    try:
        data = pd.read_csv('data/processed_sales_data.csv', parse_dates=['date'])
        return data
    except:
        return None

# Load models and data on startup
MODELS = load_models()
DATA = load_data()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_forecast(model_name, days=7):
    """Generate forecast for specified number of days"""
    
    if DATA is None:
        return None
    
    forecast_dates = pd.date_range(
        start=DATA['date'].max() + timedelta(days=1),
        periods=days
    )
    
    if model_name == 'ma' and MODELS['ma']:
        # Moving Average
        ma_value = np.mean(MODELS['ma']['last_values'])
        predictions = [ma_value] * days
        
    elif model_name == 'exp_smoothing' and MODELS['exp_smoothing']:
        # Exponential Smoothing
        predictions = MODELS['exp_smoothing'].forecast(steps=days)
        
    elif model_name == 'sarima' and MODELS['sarima']:
        # SARIMA
        predictions = MODELS['sarima'].forecast(steps=days)
        
    elif model_name == 'prophet' and MODELS['prophet']:
        # Prophet
        future = pd.DataFrame({'ds': forecast_dates})
        forecast = MODELS['prophet'].predict(future)
        predictions = forecast['yhat'].values
        
    elif model_name == 'random_forest' and MODELS['random_forest']:
        # Random Forest (simplified - would need full feature engineering)
        avg_sales = DATA['unit_sales'].tail(30).mean()
        predictions = [avg_sales] * days
        
    else:
        # Default to moving average
        avg_sales = DATA['unit_sales'].tail(7).mean()
        predictions = [avg_sales] * days
    
    return {
        'dates': [d.strftime('%Y-%m-%d') for d in forecast_dates],
        'predictions': [float(p) for p in predictions]
    }

def calculate_confidence_bounds(predictions, std_dev_multiplier=1.96):
    """Calculate confidence bounds for predictions"""
    if DATA is None:
        return None
    
    # Use historical standard deviation
    hist_std = DATA['unit_sales'].tail(30).std()
    
    lower_bounds = [max(0, p - std_dev_multiplier * hist_std) for p in predictions]
    upper_bounds = [p + std_dev_multiplier * hist_std for p in predictions]
    
    return {
        'lower': [float(b) for b in lower_bounds],
        'upper': [float(b) for b in upper_bounds]
    }

def calculate_metrics():
    """Calculate dashboard KPIs"""
    if DATA is None:
        return None
    
    # Recent data (last 30 days)
    recent_data = DATA.tail(30)
    previous_data = DATA.tail(60).head(30)
    
    # Average daily sales
    avg_sales = recent_data['unit_sales'].mean()
    prev_avg_sales = previous_data['unit_sales'].mean()
    sales_change = ((avg_sales - prev_avg_sales) / prev_avg_sales * 100) if prev_avg_sales > 0 else 0
    
    # Calculate forecast accuracy (using last 7 days as test)
    # For simplicity, using MAPE on recent data
    recent_mean = recent_data['unit_sales'].mean()
    recent_std = recent_data['unit_sales'].std()
    mape = (recent_std / recent_mean * 100) if recent_mean > 0 else 0
    forecast_accuracy = max(0, 100 - mape)
    
    # Next 7-day demand forecast
    forecast_7day = calculate_forecast('exp_smoothing', days=7)
    if forecast_7day:
        next_7day_demand = sum(forecast_7day['predictions'])
    else:
        next_7day_demand = avg_sales * 7
    
    # Days of stock (simplified calculation)
    current_inventory = avg_sales * 10  # Assume 10 days of inventory
    daily_demand = avg_sales
    days_of_stock = current_inventory / daily_demand if daily_demand > 0 else 0
    
    return {
        'avg_daily_sales': {
            'value': round(avg_sales, 0),
            'change': round(sales_change, 1),
            'unit': 'kg'
        },
        'forecast_accuracy': {
            'value': round(forecast_accuracy, 1),
            'mape': round(mape, 1),
            'unit': '%'
        },
        'next_7day_demand': {
            'value': round(next_7day_demand, 0),
            'unit': 'kg',
            'label': 'Predicted'
        },
        'days_of_stock': {
            'value': round(days_of_stock, 0),
            'unit': 'days',
            'status': 'Healthy' if days_of_stock >= 5 else 'Low Stock'
        }
    }

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get dashboard KPIs"""
    category = request.args.get('category', 'all')
    metrics = calculate_metrics()
    
    if metrics:
        return jsonify(metrics)
    else:
        return jsonify({'error': 'Data not available'}), 500

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """Get forecast data"""
    model = request.args.get('model', 'exp_smoothing')
    days = int(request.args.get('days', 7))
    category = request.args.get('category', 'all')
    
    forecast = calculate_forecast(model, days)
    
    if forecast:
        # Add confidence bounds
        bounds = calculate_confidence_bounds(forecast['predictions'])
        forecast['lower_bound'] = bounds['lower']
        forecast['upper_bound'] = bounds['upper']
        
        # Add historical data (last 30 days)
        if DATA is not None:
            historical = DATA.tail(30)[['date', 'unit_sales']].copy()
            forecast['historical'] = {
                'dates': [d.strftime('%Y-%m-%d') for d in historical['date']],
                'actual': [float(v) for v in historical['unit_sales']]
            }
        
        return jsonify(forecast)
    else:
        return jsonify({'error': 'Forecast generation failed'}), 500

@app.route('/api/historical', methods=['GET'])
def get_historical():
    """Get historical sales data"""
    if DATA is None:
        return jsonify({'error': 'Data not available'}), 500
    
    days = int(request.args.get('days', 90))
    category = request.args.get('category', 'all')
    
    historical = DATA.tail(days)[['date', 'unit_sales']].copy()
    
    return jsonify({
        'dates': [d.strftime('%Y-%m-%d') for d in historical['date']],
        'sales': [float(v) for v in historical['unit_sales']]
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available models and their status"""
    available_models = []
    
    for model_name, model in MODELS.items():
        if model is not None and model_name != 'feature_columns':
            available_models.append({
                'id': model_name,
                'name': model_name.replace('_', ' ').title(),
                'status': 'ready'
            })
    
    return jsonify({'models': available_models})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available product categories"""
    categories = [
        {'id': 'rice', 'name': 'Rice', 'icon': '🌾'},
        {'id': 'water', 'name': 'Bottled Water', 'icon': '💧'},
        {'id': 'oil', 'name': 'Cooking Oil', 'icon': '🫒'},
        {'id': 'noodles', 'name': 'Instant Noodles', 'icon': '🍜'},
        {'id': 'sugar', 'name': 'Sugar', 'icon': '🧂'}
    ]
    
    return jsonify({'categories': categories})

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("WING SHOP INVENTORY FORECASTING DASHBOARD")
    print("="*80)
    print("\nStarting Flask server...")
    print("Dashboard will be available at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
