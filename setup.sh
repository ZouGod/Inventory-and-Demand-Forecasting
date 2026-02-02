#!/bin/bash
# Quick setup and deployment script for Vercel

set -e

echo "=========================================="
echo "Wing Shop Random Forest - Setup Script"
echo "=========================================="
echo ""

# Step 1: Create directories
echo "[1/4] Creating necessary directories..."
mkdir -p models
mkdir -p data
mkdir -p static
mkdir -p templates
echo "✓ Directories created"
echo ""

# Step 2: Install dependencies
echo "[2/4] Installing Python dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Step 3: Train model
echo "[3/4] Training Random Forest model..."
python train_random_forest.py
echo ""

# Step 4: Verify deployment files
echo "[4/4] Verifying deployment files..."
files=(
    "api/__init__.py"
    "api/models_handler.py"
    "api/data_processor.py"
    "vercel.json"
    "requirements.txt"
    "index.html"
    "models/random_forest_model.pkl"
    "models/feature_columns.json"
    "models/model_metrics.json"
)

all_exist=true
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (MISSING)"
        all_exist=false
    fi
done
echo ""

if [ "$all_exist" = true ]; then
    echo "=========================================="
    echo "✅ SETUP COMPLETE!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Test locally: python -c \"from api import app; app.run(debug=True, port=5000)\""
    echo "2. Push to GitHub: git push origin main"
    echo "3. Deploy to Vercel: vercel --prod"
    echo ""
    echo "Your dashboard will be live at: https://your-vercel-app.vercel.app"
else
    echo "=========================================="
    echo "❌ SETUP INCOMPLETE"
    echo "=========================================="
    echo "Some files are missing. Check the output above."
    exit 1
fi
