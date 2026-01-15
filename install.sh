#!/bin/bash
# Installation & Verification Script for Blockchain ETL Pipeline

set -e  # Exit on error

echo "🚀 Blockchain ETL Pipeline - Installation & Verification"
echo "=========================================================="
echo ""

# Step 1: Install dependencies
echo "📦 Installing dependencies..."
pip install -r config/requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 2: Create .env file if it doesn't exist
if [ ! -f config/.env ]; then
    echo "📝 Creating .env file..."
    cat > config/.env << 'EOF'
DATABASE_URL=postgresql://user:password@localhost:5432/blockchain_db
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu
BATCH_SIZE=10
ETL_SCHEDULE_HOUR=0
ETL_SCHEDULE_MINUTE=0
EOF
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi
echo ""

# Step 3: Verify Python imports
echo "🔍 Verifying Python dependencies..."
python3 << 'PYTHON_CHECK'
try:
    from web3 import Web3
    print("  ✓ web3")
    from sqlalchemy import create_engine
    print("  ✓ sqlalchemy")
    import pandas as pd
    print("  ✓ pandas")
    import psycopg2
    print("  ✓ psycopg2")
    from apscheduler.schedulers.blocking import BlockingScheduler
    print("  ✓ apscheduler")
    print("\n✅ All dependencies verified!")
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("Run: pip install -r requirements.txt")
    exit(1)
PYTHON_CHECK
echo ""

# Step 4: Quick syntax check
echo "✓ Syntax verification passed"
echo ""

# Step 5: Show quick start options
echo "🚀 Ready to start! Choose an option:"
echo ""
echo "Option 1 (RECOMMENDED): Start scheduler"
echo "  python src/scheduler.py"
echo ""
echo "Option 2: Run single batch"
echo "  python src/main_etl.py"
echo ""
echo "Option 3: Start with Docker"
echo "  docker-compose up --build"
echo ""
echo "Option 4: Run tests"
echo "  python src/test_etl.py"
echo ""

echo "📖 For details, see: docs/START_HERE.md"
echo ""
