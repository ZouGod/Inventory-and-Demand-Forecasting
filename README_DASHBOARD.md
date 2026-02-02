# Wing Shop Inventory Forecasting Dashboard

A professional Flask-based web dashboard for real-time demand forecasting and inventory optimization at Wing Shop (Store 44).

![Dashboard Preview](dashboard_preview.png)

## 📋 Project Overview

This dashboard provides:
- **Real-time KPI Monitoring**: Track average daily sales, forecast accuracy, predicted demand, and stock levels
- **Interactive Forecasting**: 7, 14, or 30-day demand predictions with confidence intervals
- **Product Category Filtering**: Analyze specific products (Rice, Water, Oil, Noodles, Sugar)
- **Multiple Time Series Models**: Exponential Smoothing, SARIMA, Prophet, and Random Forest
- **Stock Alerts**: Automated warnings for low inventory and restock recommendations

## 🏗️ Project Structure

```
wing_shop_dashboard/
├── app.py                          # Flask backend application
├── train_and_save_models.py        # Model training script
├── requirements_flask.txt          # Python dependencies
├── models/                         # Saved ML models
│   ├── ma_model.pkl
│   ├── exp_smoothing_model.pkl
│   ├── sarima_model.pkl
│   ├── prophet_model.pkl
│   ├── random_forest_model.pkl
│   ├── feature_columns.json
│   └── metadata.json
├── data/                           # Processed data
│   └── processed_sales_data.csv
├── templates/                      # HTML templates
│   └── index.html
└── static/                         # CSS and JavaScript
    ├── css/
    │   └── style.css
    └── js/
        └── dashboard.js
```

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements_flask.txt
```

### Step 2: Update Data Paths

Edit `train_and_save_models.py` and update the file paths (around lines 33-38):

```python
# Change these paths to your data location
items = pd.read_csv(r"YOUR_PATH\items.csv")
holiday_events = pd.read_csv(r"YOUR_PATH\holidays_events.csv", parse_dates=['date'])
stores = pd.read_csv(r"YOUR_PATH\stores.csv")
oil = pd.read_csv(r"YOUR_PATH\oil.csv", parse_dates=['date'])
transactions = pd.read_csv(r"YOUR_PATH\transactions.csv", parse_dates=['date'])
train = pd.read_csv(r'YOUR_PATH\train.csv', parse_dates=['date'])
```

### Step 3: Train and Save Models

```bash
python train_and_save_models.py
```

This will:
- Load and process data for Store 44
- Train 5 forecasting models
- Save models to `./models/` directory
- Save processed data to `./data/` directory

**Expected Output:**
```
================================================================================
WING SHOP - MODEL TRAINING & SAVING
================================================================================

[1/4] Loading Data...
✓ Store 44 data loaded: (125497, 6)

[2/4] Processing Product Categories...

[3/4] Training Models...

Training Moving Average...
✓ Saved Moving Average model

Training Exponential Smoothing...
✓ Saved Exponential Smoothing model

Training SARIMA...
✓ Saved SARIMA model

Training Prophet...
✓ Saved Prophet model

Training Random Forest...
✓ Saved Random Forest model

[4/4] Saving Metadata...
✓ Saved metadata

================================================================================
MODEL TRAINING COMPLETE!
================================================================================
```

### Step 4: Run the Dashboard

```bash
python app.py
```

### Step 5: Access the Dashboard

Open your browser and navigate to:
```
http://localhost:5000
```

## 🎯 Features

### 1. **KPI Cards**
- **Avg Daily Sales**: Shows current average with % change
- **Forecast Accuracy**: MAPE-based accuracy metric
- **Next 7-Day Demand**: Predicted demand for the coming week
- **Days of Stock**: Current inventory runway

### 2. **Product Category Filters**
Filter forecasts by product type:
- 🌾 Rice
- 💧 Bottled Water
- 🫒 Cooking Oil
- 🍜 Instant Noodles
- 🧂 Sugar

### 3. **Forecast Period Selector**
Choose prediction horizon:
- 7 Days (default)
- 14 Days
- 30 Days

### 4. **Interactive Charts**
- **Forecast Tab**: Shows historical sales + predicted demand with confidence intervals
- **Inventory Tab**: Historical sales trends over 90 days
- **Alerts Tab**: Stock warnings and restock recommendations

### 5. **Real-time Updates**
- Auto-refresh every 5 minutes
- Loading indicators during data fetch
- Smooth transitions and animations

## 🔌 API Endpoints

The Flask backend provides RESTful API endpoints:

### GET `/api/metrics`
Returns KPI metrics for dashboard cards.

**Query Parameters:**
- `category` (optional): Product category filter

**Response:**
```json
{
  "avg_daily_sales": {
    "value": 424,
    "change": 8.2,
    "unit": "kg"
  },
  "forecast_accuracy": {
    "value": 92.3,
    "mape": 7.7,
    "unit": "%"
  },
  "next_7day_demand": {
    "value": 3256,
    "unit": "kg",
    "label": "Predicted"
  },
  "days_of_stock": {
    "value": 7,
    "unit": "days",
    "status": "Healthy"
  }
}
```

### GET `/api/forecast`
Returns forecast predictions with confidence bounds.

**Query Parameters:**
- `model` (optional): Model name (default: 'exp_smoothing')
- `days` (optional): Forecast horizon (default: 7)
- `category` (optional): Product category filter

**Response:**
```json
{
  "dates": ["2026-01-31", "2026-02-01", ...],
  "predictions": [420, 435, 440, ...],
  "lower_bound": [380, 395, 400, ...],
  "upper_bound": [460, 475, 480, ...],
  "historical": {
    "dates": ["2026-01-01", "2026-01-02", ...],
    "actual": [410, 425, 438, ...]
  }
}
```

### GET `/api/historical`
Returns historical sales data.

**Query Parameters:**
- `days` (optional): Number of days to retrieve (default: 90)
- `category` (optional): Product category filter

**Response:**
```json
{
  "dates": ["2025-11-01", "2025-11-02", ...],
  "sales": [405, 420, 415, ...]
}
```

### GET `/api/models`
Returns list of available forecasting models.

**Response:**
```json
{
  "models": [
    {"id": "ma", "name": "Moving Average", "status": "ready"},
    {"id": "exp_smoothing", "name": "Exponential Smoothing", "status": "ready"},
    {"id": "sarima", "name": "Sarima", "status": "ready"},
    {"id": "prophet", "name": "Prophet", "status": "ready"},
    {"id": "random_forest", "name": "Random Forest", "status": "ready"}
  ]
}
```

### GET `/api/categories`
Returns available product categories.

**Response:**
```json
{
  "categories": [
    {"id": "rice", "name": "Rice", "icon": "🌾"},
    {"id": "water", "name": "Bottled Water", "icon": "💧"},
    {"id": "oil", "name": "Cooking Oil", "icon": "🫒"},
    {"id": "noodles", "name": "Instant Noodles", "icon": "🍜"},
    {"id": "sugar", "name": "Sugar", "icon": "🧂"}
  ]
}
```

## 🎨 Customization

### Change Color Scheme
Edit `static/css/style.css` and modify CSS variables:

```css
:root {
    --primary-blue: #2D5BFF;      /* Main brand color */
    --success-green: #10B981;     /* Positive indicators */
    --warning-orange: #F59E0B;    /* Warning indicators */
    --danger-red: #EF4444;        /* Danger indicators */
    /* ... more colors ... */
}
```

### Add New Models
1. Train your model in `train_and_save_models.py`
2. Save it with pickle
3. Add loading logic in `app.py` → `load_models()`
4. Add forecasting logic in `app.py` → `calculate_forecast()`

### Modify KPIs
Edit the calculation logic in `app.py` → `calculate_metrics()`

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Models Not Loading
- Ensure you ran `train_and_save_models.py` successfully
- Check that `./models/` directory exists with .pkl files
- Verify file paths in training script

### Charts Not Displaying
- Check browser console for JavaScript errors
- Ensure Plotly.js CDN is accessible
- Verify API endpoints return data (test in browser: `http://localhost:5000/api/metrics`)

### Data Not Available
- Confirm `data/processed_sales_data.csv` exists
- Check file paths in training script match your data location
- Verify Store 44 has data in your dataset

## 📊 Performance Optimization

### For Large Datasets
- Implement data caching with Redis
- Use pagination for historical data
- Aggregate data at different granularities

### For Production
```python
# Use production WSGI server instead of Flask's development server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔒 Security Considerations

For production deployment:
1. Set `app.run(debug=False)`
2. Use environment variables for sensitive data
3. Add authentication (Flask-Login)
4. Enable HTTPS
5. Implement rate limiting (Flask-Limiter)
6. Add CORS protection

## 📈 Future Enhancements

- [ ] User authentication and role-based access
- [ ] Export reports to PDF/Excel
- [ ] Email alerts for low stock
- [ ] Multi-store comparison
- [ ] Custom date range selection
- [ ] Model performance comparison dashboard
- [ ] Integration with Wing Bank's ERP system
- [ ] Mobile-responsive design improvements

## 👤 Author

**Sang Haksou**  
Data Scientist Apprentice  
Wing Bank (Cambodia) Plc  
Internship Period: January 12 - May 12, 2026

## 📄 License

This project is part of an internship at Wing Bank (Cambodia) Plc.

---

**Built with ❤️ for Wing Shop Inventory Optimization**
