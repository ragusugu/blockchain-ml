#!/bin/bash

# 🚀 Real-Time Blockchain Processor - Quick Start
# NO DATABASE NEEDED!

echo "================================================"
echo "🚀 Real-Time Blockchain Data Processor"
echo "================================================"
echo ""
echo "Choose an option:"
echo ""
echo "1) CONSOLE MODE (Watch live transactions)"
echo "2) JSON MODE (Save to file)"
echo "3) CSV MODE (Save to spreadsheet)"
echo "4) WEBHOOK MODE (Send to Discord/Slack/API)"
echo ""
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running: bash install.sh"
    bash install.sh
fi

# Activate venv
source venv/bin/activate

cd src

# Read user choice
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "🎬 Starting CONSOLE mode..."
        export OUTPUT_MODE=console
        python realtime_processor.py
        ;;
    2)
        echo "💾 Starting JSON mode..."
        export OUTPUT_MODE=json
        python realtime_processor.py
        ;;
    3)
        echo "📊 Starting CSV mode..."
        export OUTPUT_MODE=csv
        python realtime_processor.py
        ;;
    4)
        echo "🔗 Starting WEBHOOK mode..."
        read -p "Enter webhook URL (Discord/Slack/API): " webhook_url
        if [ -z "$webhook_url" ]; then
            echo "❌ No webhook URL provided"
            exit 1
        fi
        export OUTPUT_MODE=webhook
        export WEBHOOK_URL="$webhook_url"
        python realtime_processor.py
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
