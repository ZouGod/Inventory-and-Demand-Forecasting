"""
Random Forest Model Training and Saving Script
Trains and saves the Random Forest model with feature columns for Vercel deployment
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from pathlib import Path

def create_synthetic_training_data(n_samples=1000):
    """Create synthetic training data for Random Forest"""
    np.random.seed(42)
    
    # Generate dates
    dates = pd.date_range(start='2022-01-01', periods=n_samples, freq='D')
    
    # Create features
    data = {
        'date': dates,
        'lag_1': np.random.uniform(50, 300, n_samples),
        'lag_7': np.random.uniform(50, 300, n_samples),
        'lag_30': np.random.uniform(50, 300, n_samples),
        'rolling_mean_7': np.random.uniform(80, 250, n_samples),
        'rolling_mean_30': np.random.uniform(80, 250, n_samples),
        'day_of_week': np.tile(np.arange(7), n_samples // 7 + 1)[:n_samples],
        'month': np.repeat(np.arange(1, 13), n_samples // 12 + 1)[:n_samples],
        'is_holiday': np.random.binomial(1, 0.1, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (unit_sales) based on features with some pattern
    df['unit_sales'] = (
        df['lag_1'] * 0.4 +
        df['lag_7'] * 0.3 +
        df['lag_30'] * 0.2 +
        df['rolling_mean_7'] * 0.05 +
        df['rolling_mean_30'] * 0.05 +
        (df['day_of_week'] / 7 * 50) +  # Day of week effect
        (df['is_holiday'] * 30) +  # Holiday boost
        np.random.normal(0, 15, n_samples)  # Noise
    )
    
    # Ensure non-negative sales
    df['unit_sales'] = df['unit_sales'].clip(lower=0)
    
    return df

def train_random_forest(X, y):
    """Train Random Forest model"""
    print("\n[3/4] Training Random Forest Model...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    # Calculate MAPE and RMSE
    y_pred = model.predict(X_test)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    
    print(f"✓ Random Forest trained successfully")
    print(f"  - Training R² Score: {train_score:.4f}")
    print(f"  - Testing R² Score: {test_score:.4f}")
    print(f"  - MAPE: {mape:.2f}%")
    print(f"  - RMSE: {rmse:.2f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n  Top 5 Important Features:")
    for idx, row in feature_importance.head().iterrows():
        print(f"    - {row['feature']}: {row['importance']:.4f}")
    
    return model, {
        'train_r2': float(train_score),
        'test_r2': float(test_score),
        'mape': float(mape),
        'rmse': float(rmse),
        'model_type': 'Random Forest',
        'accuracy': float(test_score)
    }

def main():
    print("="*80)
    print("RANDOM FOREST MODEL TRAINING & SAVING FOR VERCEL DEPLOYMENT")
    print("="*80)
    
    # Create models directory
    root_dir = Path(__file__).parent
    models_dir = root_dir / 'models'
    models_dir.mkdir(exist_ok=True)
    
    print("\n[1/4] Creating Synthetic Training Data...")
    
    # Create synthetic data
    df = create_synthetic_training_data(n_samples=1000)
    print(f"✓ Dataset created: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    
    # Define feature columns
    feature_columns = [
        'lag_1', 'lag_7', 'lag_30',
        'rolling_mean_7', 'rolling_mean_30',
        'day_of_week', 'month', 'is_holiday'
    ]
    
    print(f"✓ Features defined: {feature_columns}")
    
    # Prepare data
    print("\n[2/4] Preparing Data...")
    X = df[feature_columns]
    y = df['unit_sales']
    print(f"✓ X shape: {X.shape}, y shape: {y.shape}")
    
    # Train model
    model, metrics = train_random_forest(X, y)
    
    # Save model
    print("\n[4/4] Saving Model and Configuration...")
    
    # Save Random Forest model
    model_path = models_dir / 'random_forest_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved: {model_path}")
    
    # Save feature columns
    features_path = models_dir / 'feature_columns.json'
    with open(features_path, 'w') as f:
        json.dump(feature_columns, f, indent=2)
    print(f"✓ Feature columns saved: {features_path}")
    
    # Save metrics
    metrics_path = models_dir / 'model_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"✓ Metrics saved: {metrics_path}")
    
    # Save training data sample
    sample_data_path = root_dir / 'data' / 'training_sample.csv'
    sample_data_path.parent.mkdir(exist_ok=True)
    df.head(100).to_csv(sample_data_path, index=False)
    print(f"✓ Training sample saved: {sample_data_path}")
    
    print("\n" + "="*80)
    print("✅ TRAINING COMPLETE - Model ready for deployment!")
    print("="*80)
    print(f"\nModel Location: {model_path}")
    print(f"Features Location: {features_path}")
    print(f"Metrics: MAPE={metrics['mape']:.2f}%, R²={metrics['test_r2']:.4f}")
    print("\nDeployment Ready:")
    print("1. Push to GitHub")
    print("2. Connect to Vercel")
    print("3. Deploy: Dashboard will be live!")

if __name__ == '__main__':
    main()
