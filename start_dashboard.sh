#!/bin/bash
# 🚀 Quick Start Script for Blockchain Fraud Detection Dashboard

echo "=================================================="
echo "  🔗 Blockchain Fraud Detection Dashboard"
echo "  Starting Setup..."
echo "=================================================="
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python $(python3 --version) found"
echo ""

# Navigate to project directory
PROJECT_DIR="/home/sugangokul/Desktop/blockchain-ml"
cd "$PROJECT_DIR"
echo "✓ Working directory: $PROJECT_DIR"
echo ""

# Check if requirements installed
echo "✓ Checking dependencies..."
python3 -c "import flask; import web3; import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Installing..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ All dependencies installed"
fi
echo ""

# Verify file structure
echo "✓ Verifying files..."
FILES=(
    "src/ai_dashboard.py"
    "src/templates/index.html"
    "src/static/style.css"
    "src/static/script.js"
    "src/ai_fraud_detector.py"
    "src/ai_integration.py"
    "src/transform.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ❌ $file (MISSING)"
    fi
done
echo ""

# Check if model exists
if [ -f "ai_model.pkl" ]; then
    echo "✓ AI model found (ai_model.pkl)"
else
    echo "⚠️  AI model not found. Training model..."
    python3 src/train_ai_model.py
    echo "✓ Model trained"
fi
echo ""

# Check port availability
echo "✓ Checking if port 5000 is available..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "❌ Port 5000 is already in use"
    echo "   Please close the application using port 5000 or use a different port"
    exit 1
else
    echo "✓ Port 5000 is available"
fi
echo ""

# Start the dashboard
echo "=================================================="
echo "  🚀 Starting Dashboard..."
echo "=================================================="
echo ""
echo "📱 Dashboard URL: http://localhost:5000"
echo ""
echo "✨ Instructions:"
echo "  1. Open browser to http://localhost:5000"
echo "  2. Select an AI option (1, 2, or 3)"
echo "  3. Enter number of blocks (1-100)"
echo "  4. Click 'Fetch & Analyze'"
echo "  5. Click any transaction to see details"
echo "  6. Switch options anytime to compare"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo ""
echo "=================================================="
echo ""

# Start Flask
python3 src/ai_dashboard.py
