# Wing Shop Dashboard - Quick Start Guide

## 🚀 Get Your Dashboard Running in 5 Steps

### Step 1: Install Dependencies (2 minutes)
```bash
pip install -r requirements_flask.txt
```

### Step 2: Update Data Paths (1 minute)
Open `train_and_save_models.py` and change lines 33-38:

```python
# REPLACE THESE WITH YOUR ACTUAL PATHS
items = pd.read_csv(r"D:\YOUR_PATH\items.csv")
holiday_events = pd.read_csv(r"D:\YOUR_PATH\holidays_events.csv", parse_dates=['date'])
stores = pd.read_csv(r"D:\YOUR_PATH\stores.csv")
oil = pd.read_csv(r"D:\YOUR_PATH\oil.csv", parse_dates=['date'])
transactions = pd.read_csv(r"D:\YOUR_PATH\transactions.csv", parse_dates=['date'])
train = pd.read_csv(r'D:\YOUR_PATH\train.csv', parse_dates=['date'])
```

### Step 3: Train Models (3-5 minutes)
```bash
python train_and_save_models.py
```

**Expected Result:**
- ✓ Creates `models/` folder with 5 trained models
- ✓ Creates `data/` folder with processed sales data
- ✓ Prints success messages for each model

### Step 4: Launch Dashboard (1 second)
```bash
python app.py
```

**You'll See:**
```
================================================================================
WING SHOP INVENTORY FORECASTING DASHBOARD
================================================================================

Starting Flask server...
Dashboard will be available at: http://localhost:5000

Press Ctrl+C to stop the server
================================================================================

 * Running on http://0.0.0.0:5000
```

### Step 5: Open Browser
Go to: **http://localhost:5000**

---

## ✅ Verification Checklist

Before running, ensure you have:
- [ ] Python 3.8+ installed
- [ ] All dataset CSV files (train.csv, items.csv, stores.csv, etc.)
- [ ] Updated file paths in training script
- [ ] At least 2GB free RAM
- [ ] Port 5000 available

After running, verify:
- [ ] `models/` directory exists with 5 .pkl files
- [ ] `data/processed_sales_data.csv` exists
- [ ] Dashboard loads at localhost:5000
- [ ] KPI cards show numbers
- [ ] Forecast chart renders

---

## 🎯 Dashboard Features You'll See

### Top Section
- **Product Category Buttons**: Rice, Water, Oil, Noodles, Sugar
- **Forecast Period Selector**: 7, 14, or 30 days

### KPI Cards (4 boxes)
1. **Avg Daily Sales** - with % change indicator
2. **Forecast Accuracy** - MAPE percentage
3. **Next 7-Day Demand** - predicted total
4. **Days of Stock** - inventory runway

### Main Chart Area
- **Forecast Tab**: Shows historical sales (black line) + predictions (blue dotted) + confidence bounds (gray shaded)
- **Inventory Tab**: 90-day historical trend
- **Alerts Tab**: Stock warnings and recommendations

---

## 🔥 Quick Tips

### Test the Dashboard
1. Click different product categories → KPIs update
2. Change forecast period → Chart updates
3. Switch tabs → Different visualizations

### Customize KPIs
Edit `app.py` → `calculate_metrics()` function

### Change Colors
Edit `static/css/style.css` → `:root` variables

### Add New Products
Edit `app.py` → `get_categories()` function

---

## ⚠️ Common Issues

**Issue**: Models folder not created  
**Fix**: Run `python train_and_save_models.py` first

**Issue**: Dashboard shows no data  
**Fix**: Check that `data/processed_sales_data.csv` exists

**Issue**: Charts not rendering  
**Fix**: Check browser console (F12) for errors. Ensure internet connection for Plotly CDN.

**Issue**: Port 5000 already in use  
**Fix**: Change port in `app.py` last line to 5001 or 8000

**Issue**: Slow loading  
**Fix**: Reduce forecast days or historical data range

---

## 📱 Quick Commands Reference

```bash
# Install packages
pip install -r requirements_flask.txt

# Train models (run once)
python train_and_save_models.py

# Start dashboard
python app.py

# Stop dashboard
Press Ctrl+C in terminal

# Check if models exist
ls models/  # Linux/Mac
dir models\  # Windows

# View processed data
head data/processed_sales_data.csv  # Linux/Mac
type data\processed_sales_data.csv  # Windows (first few lines)
```

---

## 🎓 Next Steps After Setup

1. **Explore the Dashboard**
   - Try different product categories
   - Experiment with forecast periods
   - Check the alerts tab

2. **Understand the Data**
   - Look at `data/processed_sales_data.csv`
   - Check model files in `models/` folder
   - Review `models/metadata.json`

3. **Customize**
   - Add your company logo to `templates/index.html`
   - Adjust colors in `static/css/style.css`
   - Modify KPI calculations in `app.py`

4. **Enhance**
   - Add more product categories
   - Implement user authentication
   - Create export functionality
   - Add email alerts

---

## 📞 Troubleshooting Help

If you're stuck:
1. Check the terminal for error messages
2. Open browser console (F12) for JavaScript errors
3. Verify all file paths are correct
4. Ensure data files are not corrupted
5. Try with a smaller dataset first

---

**Dashboard Setup Time: ~10 minutes**  
**Worth it? Absolutely! 🎉**

Now you have a professional forecasting dashboard that:
- Updates in real-time
- Provides accurate predictions
- Helps optimize inventory
- Reduces waste and costs

**Happy Forecasting! 📈**
