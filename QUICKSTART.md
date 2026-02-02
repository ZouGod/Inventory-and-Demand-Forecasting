#!/bin/bash
# Quick Reference - Wing Shop Random Forest Deployment

# STEP 1: Install dependencies (do once)
pip install -r requirements.txt

# STEP 2: Train model (done! ✅)
# python train_random_forest.py

# STEP 3: Test locally
python -c "from api import app; app.run(debug=True, port=5000)"
# Then open: http://localhost:5000

# STEP 4: Prepare GitHub
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: Wing Shop Random Forest"
git remote add origin https://github.com/YOUR_USERNAME/wing-shop-forecast.git
git push -u origin main

# STEP 5: Deploy to Vercel (pick ONE)

# Option A: CLI (fastest)
npm install -g vercel
vercel --prod

# Option B: Web (easiest)
# 1. Go to vercel.com/new
# 2. Import GitHub repo
# 3. Click Deploy

# STEP 6: Test deployed app
curl https://wing-shop-forecast-xxxxx.vercel.app/api/health

# That's it! 🎉

# ============================================
# API ENDPOINTS (ready to use)
# ============================================

# 1. Health check
curl https://wing-shop-forecast-xxxxx.vercel.app/api/health

# 2. Get products
curl https://wing-shop-forecast-xxxxx.vercel.app/api/products

# 3. Get forecast (7 days for Rice)
curl -X POST https://wing-shop-forecast-xxxxx.vercel.app/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"days": 7, "product": "Rice", "store": 44}'

# 4. Get historical data (last 30 days)
curl "https://wing-shop-forecast-xxxxx.vercel.app/api/historical?days=30&product=Rice"

# 5. Get model metrics
curl https://wing-shop-forecast-xxxxx.vercel.app/api/metrics

# ============================================
# FILES CREATED
# ============================================

# API Backend:
# - api/__init__.py (Flask app + routes)
# - api/models_handler.py (ML predictions)
# - api/data_processor.py (Data loading)

# Models:
# - models/random_forest_model.pkl (Trained model)
# - models/feature_columns.json (Feature names)
# - models/model_metrics.json (Performance)

# Frontend:
# - index.html (Interactive dashboard)

# Configuration:
# - vercel.json (Deployment config)
# - requirements.txt (Python packages)
# - .gitignore (Git ignore rules)

# Documentation:
# - README.md (Main guide)
# - VERCEL_DEPLOYMENT.md (Technical docs)
# - DEPLOY_TO_VERCEL.md (Step-by-step)
# - DEPLOYMENT_COMPLETE.md (Summary)

# Scripts:
# - train_random_forest.py (Model training)
# - run_local.bat (Local startup - Windows)

# ============================================
# USEFUL COMMANDS
# ============================================

# Check Python version
python --version

# Check pip packages
pip list | grep Flask

# Test local API
curl http://localhost:5000/api/health

# View model metrics
cat models/model_metrics.json | jq .

# View feature columns
cat models/feature_columns.json | jq .

# See recent commits
git log --oneline -5

# Check Vercel deployment status
vercel status

# Open Vercel dashboard
vercel dashboard

# ============================================
# MODEL PERFORMANCE SUMMARY
# ============================================

# R² Score (Accuracy): 84.03%
# MAPE (Error): 8.75%
# RMSE: 19.36
# Training Samples: 1000 days
# Features: 8
# Trees: 100

# ============================================
# DASHBOARD FEATURES
# ============================================

# ✅ Forecast visualization (line chart)
# ✅ Historical data (bar chart)
# ✅ Performance metrics (cards)
# ✅ Product filtering
# ✅ Forecast period selection
# ✅ Confidence intervals
# ✅ Detailed table view
# ✅ Real-time status

# ============================================
# DEPLOYMENT CHECKLIST
# ============================================

# [ ] Model trained (DONE ✅)
# [ ] Dependencies installed
# [ ] Local testing successful
# [ ] GitHub repo created
# [ ] Code pushed to GitHub
# [ ] Vercel account created
# [ ] App deployed to Vercel
# [ ] Dashboard accessible
# [ ] API endpoints working
# [ ] Team notified

# ============================================
# TROUBLESHOOTING QUICK FIXES
# ============================================

# Error: Model not found
# Fix: python train_random_forest.py

# Error: Module not found
# Fix: pip install -r requirements.txt

# Error: Port 5000 in use
# Fix: python -c "from api import app; app.run(port=5001)"

# Error: CORS issues
# Fix: Check dashboard URL matches API URL

# ============================================
# PERFORMANCE STATS
# ============================================

# Cold Start (first request): 5-10 seconds
# Warm Start (subsequent): <200ms
# Model Size: 2.6 MB
# Memory Usage: ~300 MB
# Free Tier Cost: $0/month
# Includes: 100 deploys/month, 50GB bandwidth

# ============================================
# NEXT STEPS
# ============================================

# 1. Deploy to Vercel (now!)
# 2. Collect real Wing Shop data
# 3. Retrain model with real data
# 4. Add more products
# 5. Connect to POS system
# 6. Set up real-time alerts
# 7. Monitor performance

# ============================================
# DOCUMENTATION
# ============================================

# Quick Start:           This file
# Technical Details:     VERCEL_DEPLOYMENT.md
# Step-by-Step Guide:    DEPLOY_TO_VERCEL.md
# Project Overview:      README.md
# Completion Status:     DEPLOYMENT_COMPLETE.md

# ============================================
# CONTACT & SUPPORT
# ============================================

# Vercel Docs: https://vercel.com/docs
# Flask Docs: https://flask.palletsprojects.com
# Scikit-learn: https://scikit-learn.org
# GitHub Docs: https://docs.github.com

# ============================================
# 🚀 READY FOR DEPLOYMENT!
# ============================================
