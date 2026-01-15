#!/bin/bash
# 🚀 React Frontend Setup and Start

echo "=================================================="
echo "  🚀 Blockchain Fraud Detection - React Frontend"
echo "=================================================="
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js"
    exit 1
fi

cd /home/sugangokul/Desktop/blockchain-ml/src/frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "=================================================="
echo "  🎨 Starting React Development Server"
echo "=================================================="
echo ""
echo "📱 Frontend URL: http://localhost:3000"
echo "🔗 Backend API:  http://localhost:5000"
echo ""
echo "✨ The frontend will auto-reload on code changes"
echo "🛑 Press Ctrl+C to stop"
echo ""
echo "=================================================="
echo ""

npm run dev
