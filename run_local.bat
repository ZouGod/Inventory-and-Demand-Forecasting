@echo off
REM Quick startup script for Wing Shop Random Forest Dashboard
REM This script starts the Flask server for local testing

echo ==========================================
echo Wing Shop Random Forest Dashboard
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo ✓ Dependencies installed
)

echo.
echo [2/3] Checking model files...
if exist "models\random_forest_model.pkl" (
    echo ✓ Random Forest model found
) else (
    echo WARNING: Model file not found. Train it with: python train_random_forest.py
)

echo.
echo [3/3] Starting Flask server...
echo.
echo ==========================================
echo Dashboard: http://localhost:5000
echo Health Check: http://localhost:5000/api/health
echo API Docs: See VERCEL_DEPLOYMENT.md
echo ==========================================
echo.

python -c "from api import app; app.run(debug=True, port=5000)"
