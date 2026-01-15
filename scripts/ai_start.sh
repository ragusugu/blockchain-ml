#!/bin/bash

# 🧠 AI Fraud Detection - Quick Start Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🧠 BLOCKCHAIN FRAUD DETECTION - AI MODULE           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python -c "import sklearn; import matplotlib; import seaborn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing ML dependencies..."
    pip install scikit-learn matplotlib seaborn requests
fi

echo ""
echo "🧠 AI FRAUD DETECTION OPTIONS:"
echo ""
echo "1) 🚀 TRAIN AI MODEL (Generate + Train)"
echo "2) 📊 REAL-TIME FRAUD DETECTION (Option 1: After Transform)"
echo "3) 🔒 DATABASE FILTERING (Option 2: Before Load)"
echo "4) ⚡ PARALLEL ANALYSIS (Option 3: Production)"
echo "5) 📖 SHOW INTEGRATION GUIDE"
echo "6) 📈 SHOW FLOW DIAGRAM"
echo ""

read -p "Choose option (1-6): " choice

cd src

case $choice in
    1)
        echo ""
        echo "🚀 Training AI Fraud Detection Model..."
        echo "   - Generating 5000 synthetic transactions"
        echo "   - Training RandomForest classifier"
        echo "   - Generating visualizations"
        echo ""
        python train_ai_model.py
        echo ""
        echo "✅ Training complete! Check:"
        echo "   📊 fraud_analysis.png (visualizations)"
        echo "   📋 fraud_report.json (metrics)"
        echo "   🤖 fraud_model.pkl (saved model)"
        ;;
    
    2)
        echo ""
        echo "📊 REAL-TIME FRAUD DETECTION (After Transform)"
        echo "   Input: Raw blockchain data"
        echo "   Process: Extract → Transform → AI Scores → Output"
        echo "   Output: Transactions with fraud probabilities"
        echo ""
        echo "Usage example:"
        cat << 'EOF'

from ai_integration import AIEnrichedETL
from extract import extract_blocks
from transform import transform_data

# Get data from Ethereum
raw_txs = extract_blocks(100, 110, w3)

# Add AI fraud scores
etl_ai = AIEnrichedETL()
enriched = etl_ai.enrich_with_fraud_scores(raw_txs)

# enriched now has fraud_probability, is_fraud, risk_level
for tx in enriched.itertuples():
    if tx.is_fraud == 1:
        print(f"🚨 FRAUD: {tx.transaction_hash}")
        print(f"   Risk: {tx.risk_level}")
        print(f"   Probability: {tx.fraud_probability:.1%}")
EOF
        ;;
    
    3)
        echo ""
        echo "🔒 DATABASE FILTERING (Before Load)"
        echo "   Input: Raw blockchain data"
        echo "   Process: Extract → Transform → AI Filter → Load"
        echo "   Output: Normal to DB, Suspicious to alerts table"
        echo ""
        echo "Usage example:"
        cat << 'EOF'

from ai_integration import AIEnrichedETL

# Get data
raw_txs = extract_blocks(100, 110, w3)

# Filter with AI (only load normal)
etl_ai = AIEnrichedETL()
filtered = etl_ai.filter_before_load(raw_txs, db_insert_normal_only=True)

# filtered['load'] = Normal transactions → Database
# filtered['analyze'] = Suspicious transactions → Alerts table

# Load to PostgreSQL
engine.execute(insert_transactions(filtered['load']))
engine.execute(insert_fraud_alerts(filtered['analyze']))

EOF
        ;;
    
    4)
        echo ""
        echo "⚡ PARALLEL ANALYSIS (Production)"
        echo "   Input: Raw blockchain data"
        echo "   Process: Extract → Transform → Load (main thread)"
        echo "            └─ AI Analysis (background thread)"
        echo "   Output: Fast loading + AI in parallel"
        echo ""
        echo "Usage example:"
        cat << 'EOF'

from ai_integration import AIEnrichedETL
from threading import Thread

raw_txs = extract_blocks(100, 110, w3)
clean_txs = transform_data(raw_txs)

# Load immediately (main thread)
engine.execute(insert_transactions(clean_txs))

# AI analysis runs in background
def ai_analysis():
    etl_ai = AIEnrichedETL()
    results = etl_ai.parallel_ai_analysis(raw_txs)
    # Generate alerts, reports, etc.

thread = Thread(target=ai_analysis, daemon=True)
thread.start()

print("✅ Data loaded! AI running in background...")
EOF
        ;;
    
    5)
        echo ""
        echo "📖 INTEGRATION GUIDE:"
        echo ""
        cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║  CHOOSE INTEGRATION POINT BASED ON YOUR SETUP               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ ❌ NO DATABASE        ✅ Use Option 1 (After Transform)      ║
║    Real-time only        - Stream + detect frauds            ║
║    No storage            - Output to console/JSON/Webhook    ║
║                                                              ║
║ ✅ YES DATABASE       ✅ Use Option 2 (Before Load)          ║
║    Small volume          - Filter before storing             ║
║    Clean DB wanted       - Keep DB free of fraud data        ║
║                                                              ║
║ ✅ YES DATABASE       ✅ Use Option 3 (Parallel)             ║
║    HIGH VOLUME           - Load fast + AI in background      ║
║    Production scale      - Non-blocking analysis             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

QUICK REFERENCE:

Option 1 (After Transform):
├─ Flow: Extract → Transform → AI ✨ → Output
├─ Use: Real-time, streaming, no storage
├─ Speed: ⚡ Fast
└─ Setup: ⚙️ Simple

Option 2 (Before Load):
├─ Flow: Extract → Transform → AI → Load
├─ Use: Database, keep clean, separate fraud
├─ Speed: ⚡ Fast
└─ Setup: ⚙️ Medium

Option 3 (Parallel):
├─ Flow: Extract → Transform → Load
│         └─ AI (background thread)
├─ Use: Production, high volume
├─ Speed: ⚡⚡ Fastest (non-blocking)
└─ Setup: ⚙️ Complex

EOF
        ;;
    
    6)
        echo ""
        echo "📈 FLOW DIAGRAMS:"
        echo ""
        cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║              OPTION 1: AFTER TRANSFORM                       ║
║              (Real-time, No Storage)                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   ┌──────────────┐                                           ║
║   │ Ethereum RPC │                                           ║
║   │  (Alchemy)   │                                           ║
║   └──────┬───────┘                                           ║
║          │ Raw transactions                                   ║
║          ▼                                                    ║
║   ┌──────────────────────┐                                   ║
║   │  Extract Phase       │                                   ║
║   │ (extract_blocks)     │                                   ║
║   └──────┬───────────────┘                                   ║
║          │ Raw data                                           ║
║          ▼                                                    ║
║   ┌──────────────────────┐                                   ║
║   │  Transform Phase     │                                   ║
║   │ (transform_data)     │                                   ║
║   └──────┬───────────────┘                                   ║
║          │ Clean data                                         ║
║          ▼                                                    ║
║   ┌──────────────────────────────┐                           ║
║   │  🧠 AI ENRICHMENT            │                           ║
║   │  (ai_fraud_detector.py)      │                           ║
║   │  ├─ Fraud probability        │                           ║
║   │  ├─ Anomaly detection        │                           ║
║   │  └─ Risk classification      │                           ║
║   └──────┬───────────────────────┘                           ║
║          │ Enriched data                                      ║
║          ▼                                                    ║
║   ┌─────────────────────┐                                    ║
║   │  OUTPUT (Choose):   │                                    ║
║   │  ├─ Console         │                                    ║
║   │  ├─ JSON file       │                                    ║
║   │  ├─ CSV file        │                                    ║
║   │  └─ Webhook (Alert) │                                    ║
║   └─────────────────────┘                                    ║
║                                                               ║
║   ✅ No database, real-time, fast!                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝


╔═══════════════════════════════════════════════════════════════╗
║              OPTION 2: BEFORE LOAD                            ║
║              (Database, Clean Storage)                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   ┌──────────────┐                                           ║
║   │ Ethereum RPC │                                           ║
║   └──────┬───────┘                                           ║
║          ▼                                                    ║
║   ┌──────────────────┐                                       ║
║   │ Extract Phase    │                                       ║
║   └──────┬───────────┘                                       ║
║          ▼                                                    ║
║   ┌──────────────────┐                                       ║
║   │ Transform Phase  │                                       ║
║   └──────┬───────────┘                                       ║
║          │ Clean data                                         ║
║          ▼                                                    ║
║   ┌──────────────────────────────┐                           ║
║   │  🧠 AI FILTER                │                           ║
║   │  (detect fraud)              │                           ║
║   └──────┬───────────┬───────────┘                           ║
║          │           │                                        ║
║      ┌───▼───┐   ┌───▼──────────┐                            ║
║      │NORMAL │   │SUSPICIOUS    │                            ║
║      └───┬───┘   └───┬──────────┘                            ║
║          ▼           ▼                                        ║
║   ┌──────────┐  ┌─────────────┐                              ║
║   │  LOAD    │  │ FRAUD ALERT │                              ║
║   │   DB     │  │    TABLE    │                              ║
║   └──────────┘  └─────────────┘                              ║
║                                                               ║
║   ✅ Database stays clean!                                  ║
║   ✅ Fraud data separate!                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝


╔═══════════════════════════════════════════════════════════════╗
║              OPTION 3: PARALLEL ANALYSIS                      ║
║              (Production, High Volume)                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   ┌──────────────┐                                           ║
║   │ Ethereum RPC │                                           ║
║   └──────┬───────┘                                           ║
║          ▼                                                    ║
║   ┌──────────────────────┐                                   ║
║   │  Extract Phase       │                                   ║
║   └──────┬───────────────┘                                   ║
║          ▼                                                    ║
║   ┌──────────────────────┐                                   ║
║   │  Transform Phase     │                                   ║
║   └──────┬───────────────┘                                   ║
║          │                                                    ║
║          ├──────────────────────┐                             ║
║          │                      │                             ║
║     MAIN THREAD           BACKGROUND THREAD                  ║
║          │                      │                             ║
║          ▼                      ▼                             ║
║   ┌──────────────┐      ┌──────────────────┐                ║
║   │ LOAD to DB   │      │ 🧠 AI ANALYSIS   │                ║
║   │ (FAST!)      │      │ (Runs in BG)     │                ║
║   └──────────────┘      │ ├─ Fraud detect  │                ║
║                         │ ├─ Alerts        │                ║
║    ✅ Returns         │ ├─ Reports      │                ║
║    immediately         │ └─ Visuals       │                ║
║                         └──────────────────┘                ║
║                                                               ║
║   ✅ Non-blocking loading!                                  ║
║   ✅ AI runs parallel!                                      ║
║   ✅ Best for production!                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

EOF
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"
