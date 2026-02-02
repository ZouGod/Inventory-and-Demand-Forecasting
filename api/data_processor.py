"""
Data Processor for Wing Shop Forecasting
Handles data loading and processing from CSV files
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

class DataProcessor:
    """Processes and provides access to sales data"""
    
    def __init__(self):
        self.data = None
        self.products = []
        self.stores = []
        self._load_data()
    
    def _load_data(self):
        """Load sales data from CSV"""
        try:
            root_dir = Path(__file__).parent.parent
            data_dir = root_dir / 'data'
            
            # Try to load processed data
            csv_files = [
                'processed_sales_data.csv',
                'clean_sales.csv',
                'train.csv'
            ]
            
            for csv_file in csv_files:
                csv_path = data_dir / csv_file
                if csv_path.exists():
                    self.data = pd.read_csv(csv_path)
                    if 'date' in self.data.columns:
                        self.data['date'] = pd.to_datetime(self.data['date'])
                    
                    print(f"✓ Data loaded from {csv_path}")
                    self._extract_metadata()
                    return
            
            print("Warning: No sales data found, using synthetic data")
            self._create_synthetic_data()
        
        except Exception as e:
            print(f"Error loading data: {e}")
            self._create_synthetic_data()
    
    def _extract_metadata(self):
        """Extract products and stores from data"""
        try:
            if self.data is None or self.data.empty:
                return
            
            # Extract products
            for col in ['family', 'product', 'category', 'product_name']:
                if col in self.data.columns:
                    self.products = self.data[col].dropna().unique().tolist()[:10]
                    break
            
            # Extract stores
            for col in ['store_nbr', 'store', 'store_id']:
                if col in self.data.columns:
                    self.stores = self.data[col].dropna().unique().tolist()
                    break
            
            if not self.products:
                self.products = ['Rice', 'Water', 'Oil', 'Noodles', 'Sugar']
            
            if not self.stores:
                self.stores = [44]  # Default store
        
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            self.products = ['Rice', 'Water', 'Oil', 'Noodles', 'Sugar']
            self.stores = [44]
    
    def _create_synthetic_data(self):
        """Create synthetic sales data for demo"""
        dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
        
        synthetic_data = {
            'date': dates,
            'unit_sales': np.random.randint(50, 300, len(dates)),
            'family': np.random.choice(['Rice', 'Water', 'Oil', 'Noodles', 'Sugar'], len(dates)),
            'store_nbr': 44,
            'transactions': np.random.randint(100, 500, len(dates))
        }
        
        self.data = pd.DataFrame(synthetic_data)
        self.products = ['Rice', 'Water', 'Oil', 'Noodles', 'Sugar']
        self.stores = [44]
    
    def get_products(self):
        """Get list of available products"""
        if not self.products:
            return ['Rice', 'Water', 'Oil', 'Noodles', 'Sugar']
        return self.products
    
    def get_historical(self, days=30, product='all'):
        """
        Get historical sales data
        
        Args:
            days: Number of days to retrieve
            product: Specific product or 'all'
        
        Returns:
            List of historical data points
        """
        try:
            if self.data is None or self.data.empty:
                return []
            
            # Get last N days
            cutoff_date = datetime.now() - timedelta(days=days)
            
            if 'date' in self.data.columns:
                filtered = self.data[self.data['date'] >= cutoff_date].copy()
            else:
                filtered = self.data.tail(days).copy()
            
            # Filter by product if specified
            if product != 'all':
                for col in ['family', 'product', 'category', 'product_name']:
                    if col in filtered.columns:
                        filtered = filtered[filtered[col] == product]
                        break
            
            # Aggregate by date if multiple entries
            sales_col = 'unit_sales' if 'unit_sales' in filtered.columns else filtered.columns[-1]
            
            if 'date' in filtered.columns:
                daily_sales = filtered.groupby('date')[sales_col].sum().reset_index()
            else:
                daily_sales = filtered[[sales_col]].reset_index()
            
            # Format output
            result = []
            for _, row in daily_sales.iterrows():
                date = row['date'] if 'date' in row else datetime.now()
                value = float(row[sales_col]) if sales_col in row else 0
                
                result.append({
                    'date': pd.to_datetime(date).strftime('%Y-%m-%d'),
                    'value': round(value, 2),
                    'product': product
                })
            
            return result
        
        except Exception as e:
            print(f"Error retrieving historical data: {e}")
            return self._get_synthetic_historical(days, product)
    
    def _get_synthetic_historical(self, days=30, product='all'):
        """Generate synthetic historical data"""
        result = []
        base_value = 150
        
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            # Add trend and noise
            value = base_value + (days - i) * 0.5 + np.random.normal(0, 10)
            
            result.append({
                'date': date.strftime('%Y-%m-%d'),
                'value': round(max(0, value), 2),
                'product': product
            })
        
        return result
    
    def get_statistics(self, product='all'):
        """Get statistical summary of product sales"""
        try:
            if self.data is None or self.data.empty:
                return {}
            
            filtered = self.data.copy()
            
            # Filter by product
            if product != 'all':
                for col in ['family', 'product', 'category']:
                    if col in filtered.columns:
                        filtered = filtered[filtered[col] == product]
                        break
            
            # Get sales column
            sales_col = 'unit_sales' if 'unit_sales' in filtered.columns else filtered.columns[-1]
            
            values = filtered[sales_col].dropna()
            
            return {
                'mean': float(values.mean()),
                'median': float(values.median()),
                'std': float(values.std()),
                'min': float(values.min()),
                'max': float(values.max()),
                'count': len(values)
            }
        
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return {}
