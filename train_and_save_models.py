"""
Wing Shop - Model Training and Saving Script
This script trains models and saves them for use in the Flask dashboard
"""

import pandas as pd
import numpy as np
import pickle
import json
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Time Series Models
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor

print("="*80)
print("WING SHOP - MODEL TRAINING & SAVING")
print("="*80)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================

print("\n[1/4] Loading Data...")

# Load datasets
items = pd.read_csv(r"D:\CADT\InternshipII\wing_shop\data\raw\extracted_all\items.csv")
holiday_events = pd.read_csv(r"D:\CADT\InternshipII\wing_shop\data\raw\extracted_all\holidays_events.csv", parse_dates=['date'])
stores = pd.read_csv(r"D:\CADT\InternshipII\wing_shop\data\raw\extracted_all\stores.csv")
oil = pd.read_csv(r"D:\CADT\InternshipII\wing_shop\data\raw\extracted_all\oil.csv", parse_dates=['date'])
transactions = pd.read_csv(r"D:\CADT\InternshipII\wing_shop\data\raw\extracted_all\transactions.csv", parse_dates=['date'])
train = pd.read_csv(r'D:\CADT\InternshipII\wing_shop\data\raw\extracted_all\train.csv', parse_dates=['date'])

# Filter for Store 44
store_44_data = train[train['store_nbr'] == 44].copy()

print(f"✓ Store 44 data loaded: {store_44_data.shape}")

# ============================================================================
# 2. CREATE PRODUCT CATEGORIES MAPPING
# ============================================================================

# Map actual families to dashboard categories
category_mapping = {
    'GROCERY I': 'Rice',
    'BEVERAGES': 'Bottled Water',
    'GROCERY II': 'Cooking Oil',
    'BREAD/BAKERY': 'Instant Noodles',
    'PRODUCE': 'Sugar'
}

# For this example, we'll create aggregated data by product family
# In production, you'd map specific items to categories

print("\n[2/4] Processing Product Categories...")

# ============================================================================
# 3. PREPARE DATA FOR EACH CATEGORY
# ============================================================================

def prepare_category_data(category_filter=None):
    """Prepare data for a specific category or all categories"""
    
    if category_filter:
        # Filter by specific item families
        relevant_families = [k for k, v in category_mapping.items() if v == category_filter]
        if relevant_families:
            category_items = items[items['family'].isin(relevant_families)]['item_nbr'].unique()
            filtered_data = store_44_data[store_44_data['item_nbr'].isin(category_items)].copy()
        else:
            filtered_data = store_44_data.copy()
    else:
        filtered_data = store_44_data.copy()
    
    # Aggregate daily sales
    daily_sales = filtered_data.groupby('date').agg({
        'unit_sales': 'sum',
        'onpromotion': 'sum'
    }).reset_index()
    
    # Merge with transactions
    daily_sales = daily_sales.merge(
        transactions[transactions['store_nbr'] == 44][['date', 'transactions']], 
        on='date', 
        how='left'
    )
    
    # Merge with oil prices
    daily_sales = daily_sales.merge(oil, on='date', how='left')
    
    # Forward fill missing values
    daily_sales['dcoilwtico'] = daily_sales['dcoilwtico'].fillna(method='ffill').fillna(method='bfill')
    daily_sales['transactions'] = daily_sales['transactions'].fillna(0)
    
    # Add holiday features
    holiday_events['is_holiday'] = 1
    daily_sales = daily_sales.merge(
        holiday_events[['date', 'is_holiday']].drop_duplicates('date'),
        on='date',
        how='left'
    )
    daily_sales['is_holiday'] = daily_sales['is_holiday'].fillna(0)
    
    # Handle negative sales
    daily_sales['unit_sales'] = daily_sales['unit_sales'].clip(lower=0)
    
    # Sort by date
    daily_sales = daily_sales.sort_values('date').reset_index(drop=True)
    
    # Create features
    daily_sales['year'] = daily_sales['date'].dt.year
    daily_sales['month'] = daily_sales['date'].dt.month
    daily_sales['day'] = daily_sales['date'].dt.day
    daily_sales['dayofweek'] = daily_sales['date'].dt.dayofweek
    daily_sales['quarter'] = daily_sales['date'].dt.quarter
    daily_sales['is_weekend'] = daily_sales['dayofweek'].isin([5, 6]).astype(int)
    daily_sales['day_of_month'] = daily_sales['date'].dt.day
    daily_sales['is_month_start'] = daily_sales['date'].dt.is_month_start.astype(int)
    daily_sales['is_month_end'] = daily_sales['date'].dt.is_month_end.astype(int)
    daily_sales['is_payday'] = ((daily_sales['day_of_month'] == 15) | 
                                 (daily_sales['is_month_end'] == 1)).astype(int)
    
    # Lag features
    for lag in [1, 7, 14, 30]:
        daily_sales[f'sales_lag_{lag}'] = daily_sales['unit_sales'].shift(lag)
    
    # Rolling statistics
    for window in [7, 14, 30]:
        daily_sales[f'sales_rolling_mean_{window}'] = daily_sales['unit_sales'].rolling(window=window).mean()
        daily_sales[f'sales_rolling_std_{window}'] = daily_sales['unit_sales'].rolling(window=window).std()
    
    return daily_sales

# ============================================================================
# 4. TRAIN AND SAVE MODELS
# ============================================================================

print("\n[3/4] Training Models...")

# Create models directory
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Prepare data for the main category (all products)
daily_sales = prepare_category_data(category_filter=None)

# Save processed data
daily_sales.to_csv('data/processed_sales_data.csv', index=False)
print("✓ Saved processed data")

# Train models on full dataset
sales_series = daily_sales.set_index('date')['unit_sales']

# Model 1: Moving Average
print("\nTraining Moving Average...")
ma_window = 7
ma_model = {'window': ma_window, 'last_values': sales_series.tail(ma_window).values}
with open('models/ma_model.pkl', 'wb') as f:
    pickle.dump(ma_model, f)
print("✓ Saved Moving Average model")

# Model 2: Exponential Smoothing
print("\nTraining Exponential Smoothing...")
try:
    es_model = ExponentialSmoothing(
        sales_series,
        seasonal_periods=7,
        trend='add',
        seasonal='add'
    ).fit()
    with open('models/exp_smoothing_model.pkl', 'wb') as f:
        pickle.dump(es_model, f)
    print("✓ Saved Exponential Smoothing model")
except Exception as e:
    print(f"⚠ Exponential Smoothing failed: {e}")

# Model 3: SARIMA
print("\nTraining SARIMA...")
try:
    sarima_model = SARIMAX(
        sales_series,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 7)
    ).fit(disp=False)
    with open('models/sarima_model.pkl', 'wb') as f:
        pickle.dump(sarima_model, f)
    print("✓ Saved SARIMA model")
except Exception as e:
    print(f"⚠ SARIMA failed: {e}")

# Model 4: Prophet
print("\nTraining Prophet...")
try:
    prophet_train = daily_sales[['date', 'unit_sales']].rename(columns={'date': 'ds', 'unit_sales': 'y'})
    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    prophet_model.add_country_holidays(country_name='EC')
    prophet_model.fit(prophet_train)
    with open('models/prophet_model.pkl', 'wb') as f:
        pickle.dump(prophet_model, f)
    print("✓ Saved Prophet model")
except Exception as e:
    print(f"⚠ Prophet failed: {e}")

# Model 5: Random Forest
print("\nTraining Random Forest...")
try:
    feature_cols = ['dayofweek', 'month', 'quarter', 'is_weekend', 'is_payday',
                    'onpromotion', 'transactions', 'dcoilwtico', 'is_holiday',
                    'sales_lag_1', 'sales_lag_7', 'sales_lag_14', 'sales_lag_30',
                    'sales_rolling_mean_7', 'sales_rolling_mean_14', 'sales_rolling_mean_30']
    
    train_ml = daily_sales.dropna(subset=feature_cols + ['unit_sales'])
    X_train = train_ml[feature_cols]
    y_train = train_ml['unit_sales']
    
    rf_model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    with open('models/random_forest_model.pkl', 'wb') as f:
        pickle.dump(rf_model, f)
    
    # Save feature columns
    with open('models/feature_columns.json', 'w') as f:
        json.dump(feature_cols, f)
    
    print("✓ Saved Random Forest model")
except Exception as e:
    print(f"⚠ Random Forest failed: {e}")

# ============================================================================
# 5. SAVE METADATA
# ============================================================================

print("\n[4/4] Saving Metadata...")

metadata = {
    'last_training_date': datetime.now().isoformat(),
    'data_date_range': {
        'start': daily_sales['date'].min().isoformat(),
        'end': daily_sales['date'].max().isoformat()
    },
    'total_records': len(daily_sales),
    'categories': list(category_mapping.values()),
    'models_trained': ['Moving Average', 'Exponential Smoothing', 'SARIMA', 'Prophet', 'Random Forest']
}

with open('models/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("✓ Saved metadata")

print("\n" + "="*80)
print("MODEL TRAINING COMPLETE!")
print("="*80)
print(f"\nModels saved in: ./models/")
print(f"Data saved in: ./data/")
print(f"\nYou can now run the Flask dashboard with: python app.py")
print("="*80)
