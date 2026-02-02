# Vercel Deployment Instructions

## Prerequisites
- GitHub account
- Vercel account (free at vercel.com)
- Git installed
- Python 3.9+ (for local testing)

## Step 1: Prepare Local Repository

```bash
cd d:\CADT\InternshipII\wing_shop_dashboard

# Initialize Git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Wing Shop Random Forest Forecasting Dashboard"
```

## Step 2: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name: `wing-shop-forecast`
3. Description: "Wing Shop Demand Forecasting with Random Forest ML"
4. Make it Public (for Vercel free tier)
5. Click "Create repository"

## Step 3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/wing-shop-forecast.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Vercel

### Option A: Using Web Interface (Easiest)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Paste: `https://github.com/YOUR_USERNAME/wing-shop-forecast`
4. Click "Continue"
5. Vercel will auto-detect Python settings
6. Click "Deploy"

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to staging (test)
vercel

# Deploy to production
vercel --prod
```

## Step 5: Verify Deployment

After deployment, Vercel will show your live URL. Test it:

```bash
# Replace with your actual Vercel URL
curl https://wing-shop-forecast-xxxxx.vercel.app/api/health

# Should return:
# {"status":"healthy","service":"Wing Shop Random Forest Forecaster","models_loaded":true}
```

## Accessing Your Dashboard

- **Dashboard**: `https://wing-shop-forecast-xxxxx.vercel.app`
- **API Health**: `https://wing-shop-forecast-xxxxx.vercel.app/api/health`
- **Forecast**: `POST https://wing-shop-forecast-xxxxx.vercel.app/api/forecast`

## Project Structure for Vercel

```
wing_shop_dashboard/
├── api/                      # Python serverless functions
│   ├── __init__.py          # Main Flask app & routes
│   ├── models_handler.py    # ML model management
│   └── data_processor.py    # Data handling
├── models/                   # Trained ML models
│   ├── random_forest_model.pkl
│   ├── feature_columns.json
│   └── model_metrics.json
├── data/                     # CSV data files
│   ├── processed_sales_data.csv
│   └── training_sample.csv
├── index.html               # Dashboard webpage
├── vercel.json             # Vercel config
├── requirements.txt        # Python dependencies
└── train_random_forest.py  # Model training script
```

## Key Files Explained

### vercel.json
Tells Vercel how to build and deploy your app:
- Specifies Python 3.9 runtime
- Routes API calls to Flask functions
- Serves static HTML files

### requirements.txt
Python packages needed:
- Flask (web framework)
- pandas, numpy (data processing)
- scikit-learn (ML models)
- joblib (model serialization)

### api/__init__.py
Flask application with 5 endpoints:
- `GET /api/health` - System status
- `POST /api/forecast` - Generate predictions
- `GET /api/products` - List products
- `GET /api/historical` - Past sales data
- `GET /api/metrics` - Model performance

## Environment Variables (Optional)

In Vercel dashboard, you can add:

```
DEBUG=false
PYTHONUNBUFFERED=1
MAX_FORECAST_DAYS=90
```

Go to Project Settings → Environment Variables

## Monitoring & Logs

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click your project
3. Click "Deployments"
4. Click latest deployment
5. See build logs and runtime logs

## Updating Your App

After making changes:

```bash
# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push origin main

# Vercel automatically redeploys!
```

## Troubleshooting

### 500 Error - Model Not Found
```
Error: Could not load model
```
**Solution**: Ensure `models/random_forest_model.pkl` exists in repository

### Cold Start Slow
First request takes 5-10s to load model. Subsequent requests are instant.

### CSV Data Not Loading
Make sure `data/processed_sales_data.csv` is in repository (not in .gitignore)

### API Returns 404
Check:
1. Routes match in `api/__init__.py`
2. API URL includes `/api/` prefix
3. No typos in endpoint names

## Performance Stats

- **Deployment time**: 1-2 minutes
- **Cold start**: 5-10 seconds
- **Forecast API**: <200ms
- **Model size**: 2.6 MB
- **Vercel free tier**: Sufficient for this app

## Scaling Up

If you need more features:

1. **Add More Products**: Update data processor
2. **More Accurate Forecasts**: Collect real Wing Shop data
3. **Advanced Features**: Add promotions, seasonality
4. **Multiple Models**: Compare Random Forest with Prophet, ARIMA
5. **Database**: Switch from CSV to PostgreSQL (Vercel Postgres)

## Next Deployment

After successful first deployment:

1. **Collect Real Data**: Replace synthetic data with actual sales
2. **Retrain Model**: Run `python train_random_forest.py`
3. **Push Update**: `git push origin main`
4. **Vercel Auto-Redeploys**: Dashboard instantly updated

## Security Notes

- Model is read-only
- No sensitive data exposed
- API doesn't require authentication (add later if needed)
- HTTPS enabled by default

## Cost

- **Vercel Free Tier**: $0/month
- **Includes**: 
  - Up to 100 deployments/month
  - Unlimited serverless function calls
  - 50GB bandwidth/month
  - Sufficient for this application

## Support Resources

- [Vercel Python Docs](https://vercel.com/docs/functions/python)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Scikit-learn Guide](https://scikit-learn.org)
- [Vercel Community](https://vercel.com/feedback)

---

**Status**: Ready to Deploy ✅  
**Last Updated**: February 2, 2024
