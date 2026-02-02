# Wing Shop Inventory Forecasting - Complete Project Guide

**Student:** Sang Haksou  
**Company:** Wing Bank (Cambodia) Plc  
**Project:** Wing Shop Inventory Optimization Dashboard  
**Internship Period:** January 12 - May 12, 2026

---

## 📚 Project Overview

This project delivers an end-to-end demand forecasting solution consisting of:

1. **Data Analysis & Model Training** (Python Scripts)
2. **Web Dashboard** (Flask Application)
3. **Real-time Forecasting API** (REST Endpoints)

---

## 🗂️ Complete File Structure

```
wing_shop_project/
│
├── 📊 DATA ANALYSIS & TRAINING
│   ├── wing_shop_forecasting.py                 # Full analysis (7 models)
│   ├── wing_shop_forecasting_no_arima_lgbm.py   # Reduced models (5 models)
│   ├── train_and_save_models.py                 # Train & save for dashboard
│   ├── plotting_section.py                      # Standalone plotting code
│   ├── requirements.txt                         # Analysis dependencies
│   └── README.md                                # Analysis documentation
│
├── 🌐 FLASK DASHBOARD
│   ├── app.py                                   # Flask backend
│   ├── requirements_flask.txt                   # Dashboard dependencies
│   ├── README_DASHBOARD.md                      # Dashboard documentation
│   ├── QUICKSTART_DASHBOARD.md                  # Quick setup guide
│   │
│   ├── templates/                               # HTML templates
│   │   └── index.html                           # Main dashboard page
│   │
│   ├── static/                                  # Frontend assets
│   │   ├── css/
│   │   │   └── style.css                        # Dashboard styles
│   │   └── js/
│   │       └── dashboard.js                     # Dashboard logic
│   │
│   ├── models/                                  # Saved ML models (generated)
│   │   ├── ma_model.pkl
│   │   ├── exp_smoothing_model.pkl
│   │   ├── sarima_model.pkl
│   │   ├── prophet_model.pkl
│   │   ├── random_forest_model.pkl
│   │   ├── feature_columns.json
│   │   └── metadata.json
│   │
│   └── data/                                    # Processed data (generated)
│       └── processed_sales_data.csv
│
└── 📈 OUTPUT (from analysis scripts)
    └── output_plots/                            # Generated visualizations
        ├── 01_time_series_overview.png
        ├── 02_seasonal_decomposition.png
        ├── 03_acf_pacf.png
        ├── 04_model_comparison_metrics.png
        ├── 05_forecast_comparison.png
        ├── 06_residual_analysis.png
        ├── predictions_comparison.csv
        └── model_evaluation_results.csv
```

---

## 🎯 Two Ways to Use This Project

### Option 1: Data Analysis Only
**Purpose:** Research, model comparison, academic report  
**Files Needed:** `wing_shop_forecasting.py` or `wing_shop_forecasting_no_arima_lgbm.py`  
**Output:** Charts, CSV files with predictions and metrics

### Option 2: Production Dashboard
**Purpose:** Real-time forecasting, business operations  
**Files Needed:** Flask dashboard files + `train_and_save_models.py`  
**Output:** Interactive web dashboard

---

## 📋 Complete Workflow

### Phase 1: Data Analysis & Model Evaluation

**Step 1.1 - Initial Analysis**
```bash
# Install dependencies
pip install -r requirements.txt

# Run full analysis (7 models)
python wing_shop_forecasting.py

# OR run reduced analysis (5 models, faster)
python wing_shop_forecasting_no_arima_lgbm.py
```

**What You Get:**
- 6 PNG charts showing:
  - Time series overview
  - Seasonal patterns
  - ACF/PACF analysis
  - Model comparison
  - Forecast predictions
  - Residual analysis
- 2 CSV files:
  - predictions_comparison.csv
  - model_evaluation_results.csv

**Time Required:** 10-20 minutes  
**Use Cases:**
- Understanding data patterns
- Model selection
- Report generation
- Academic presentation

---

### Phase 2: Dashboard Development

**Step 2.1 - Train Models for Dashboard**
```bash
# Install Flask dependencies
pip install -r requirements_flask.txt

# Update data paths in train_and_save_models.py
# Then run:
python train_and_save_models.py
```

**What It Does:**
- Loads Store 44 data
- Trains 5 models
- Saves models as .pkl files in `models/`
- Saves processed data to `data/`

**Step 2.2 - Launch Dashboard**
```bash
python app.py
```

**Step 2.3 - Access Dashboard**
Open browser: `http://localhost:5000`

**Time Required:** 5-10 minutes  
**Use Cases:**
- Daily operations
- Real-time monitoring
- Business presentations
- Inventory management

---

## 🔄 Typical Project Timeline

### Week 1-2: Data Exploration
- Run analysis scripts
- Generate visualizations
- Understand patterns
- Select best model

### Week 3-4: Model Development
- Train multiple models
- Compare performance
- Fine-tune parameters
- Document findings

### Week 5-6: Dashboard Development
- Setup Flask application
- Create HTML/CSS interface
- Implement API endpoints
- Test functionality

### Week 7-8: Testing & Refinement
- User acceptance testing
- Performance optimization
- Bug fixes
- Documentation

---

## 🎓 Learning Outcomes

### Technical Skills Gained
✅ Time series analysis (ARIMA, SARIMA, Prophet)  
✅ Machine learning (Random Forest, LightGBM)  
✅ Web development (Flask, HTML, CSS, JavaScript)  
✅ Data visualization (Matplotlib, Seaborn, Plotly)  
✅ API development (RESTful endpoints)  
✅ Model deployment and serving  

### Business Skills Gained
✅ Inventory optimization  
✅ Demand forecasting  
✅ KPI development  
✅ Dashboard design  
✅ Stakeholder communication  

---

## 📊 Model Comparison Summary

| Model | Pros | Cons | Best For |
|-------|------|------|----------|
| **Moving Average** | Simple, fast | Not adaptive | Baseline comparison |
| **Exp Smoothing** | Good for trends | Needs parameters | Short-term forecasts |
| **ARIMA** | Statistical rigor | Complex setup | Academic analysis |
| **SARIMA** | Handles seasonality | Slow training | Weekly patterns |
| **Prophet** | Easy to use | Black box | Holiday effects |
| **Random Forest** | Feature flexibility | Not pure time series | Multi-feature data |
| **LightGBM** | Fast, accurate | Complex tuning | Large datasets |

---

## 🚀 Deployment Options

### Development (Current Setup)
```bash
python app.py  # Flask development server
```
- Good for: Testing, development
- Not for: Production use

### Production (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
- Good for: Real deployment
- Handles: Multiple requests

### Cloud Deployment
**Options:**
- Heroku (easiest)
- AWS EC2/Elastic Beanstalk
- Google Cloud Run
- Azure App Service

---

## 🔧 Customization Guide

### Add New Product Category

**1. Update `train_and_save_models.py`:**
```python
category_mapping = {
    'GROCERY I': 'Rice',
    'BEVERAGES': 'Bottled Water',
    'NEW_FAMILY': 'New Product',  # Add this
    # ...
}
```

**2. Update `app.py`:**
```python
@app.route('/api/categories')
def get_categories():
    categories = [
        # existing categories...
        {'id': 'new', 'name': 'New Product', 'icon': '🎁'}  # Add this
    ]
    return jsonify({'categories': categories})
```

**3. Update `templates/index.html`:**
```html
<button class="category-btn" data-category="new">
    <span class="category-icon">🎁</span>
    <span>New Product</span>
</button>
```

### Change Forecast Horizon

**In Dashboard:** Use dropdown (already implemented)

**In Analysis Script:**
```python
# Change this line
test_days = 30  # Change to 7, 14, 60, etc.
```

### Modify KPI Calculations

Edit `app.py` → `calculate_metrics()`:
```python
def calculate_metrics():
    # Your custom logic here
    avg_sales = recent_data['unit_sales'].mean()
    # Add more calculations...
```

---

## 📖 Documentation Links

1. **Analysis Scripts**: See `README.md`
2. **Dashboard**: See `README_DASHBOARD.md`
3. **Quick Start**: See `QUICKSTART.md` or `QUICKSTART_DASHBOARD.md`

---

## 🐛 Troubleshooting Hub

### Analysis Script Issues

**Problem:** ModuleNotFoundError  
**Solution:** `pip install -r requirements.txt`

**Problem:** FileNotFoundError  
**Solution:** Update file paths in script

**Problem:** Model training too slow  
**Solution:** Reduce data size or skip ARIMA/Prophet

### Dashboard Issues

**Problem:** Models not found  
**Solution:** Run `train_and_save_models.py` first

**Problem:** Dashboard won't start  
**Solution:** Check port 5000 is available

**Problem:** Charts not rendering  
**Solution:** Check internet connection (Plotly CDN)

---

## ✅ Pre-Submission Checklist

### For Analysis Report
- [ ] All charts generated in `output_plots/`
- [ ] CSV files contain predictions
- [ ] Model comparison table included
- [ ] Code is documented
- [ ] README is complete

### For Dashboard Demo
- [ ] Models trained and saved
- [ ] Dashboard loads at localhost:5000
- [ ] All KPIs display correctly
- [ ] Charts render properly
- [ ] Product filters work
- [ ] No console errors

---

## 🎯 Project Deliverables

### Phase 1 Deliverables (Analysis)
1. ✅ Python forecasting scripts
2. ✅ 6 visualization charts
3. ✅ Model comparison report (CSV)
4. ✅ Predictions dataset (CSV)
5. ✅ Technical documentation

### Phase 2 Deliverables (Dashboard)
1. ✅ Flask web application
2. ✅ Interactive dashboard UI
3. ✅ REST API endpoints
4. ✅ Trained ML models
5. ✅ User documentation

### Final Report Should Include
- Executive summary
- Problem statement
- Methodology
- Data analysis results
- Model comparison
- Dashboard screenshots
- Conclusions & recommendations
- Future enhancements

---

## 📞 Support & Resources

### Python Libraries Documentation
- Pandas: https://pandas.pydata.org/docs/
- Statsmodels: https://www.statsmodels.org/
- Prophet: https://facebook.github.io/prophet/
- Flask: https://flask.palletsprojects.com/

### Learning Resources
- Time Series: https://otexts.com/fpp2/
- Flask Tutorial: https://flask.palletsprojects.com/tutorial/
- Plotly Charts: https://plotly.com/python/

---

## 🏆 Success Metrics

### Technical Success
- ✅ Forecast accuracy (MAPE) < 15%
- ✅ Dashboard loads in < 3 seconds
- ✅ API response time < 1 second
- ✅ Zero critical bugs

### Business Success
- ✅ Reduced waste by 15-20%
- ✅ Improved stock availability
- ✅ Order calculation time: 4 hours → 3 minutes
- ✅ Manager satisfaction score: 8+/10

---

## 🎓 Presentation Tips

### For Technical Audience
- Focus on model architecture
- Show code snippets
- Explain hyperparameters
- Discuss performance metrics

### For Business Audience
- Start with problem statement
- Show dashboard demo
- Highlight cost savings
- Present KPI improvements

### Demo Flow
1. Show problem (old manual process)
2. Explain solution (automated forecasting)
3. Live dashboard demo
4. Show results (charts, metrics)
5. Discuss impact (time/cost savings)

---

**Project Duration:** 16 weeks (January - May 2026)  
**Estimated Hours:** 320 hours (20 hours/week)  
**Technologies Used:** Python, Flask, JavaScript, HTML/CSS, ML Models  
**Business Impact:** High (inventory optimization, cost reduction)

---

**Good luck with your internship! 🚀**

This comprehensive solution demonstrates:
- Strong technical skills
- Business understanding
- Problem-solving ability
- Professional development practices

**You've got this! 💪**
