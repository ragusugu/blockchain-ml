# 🔗 Blockchain Fraud Detection with Dual-Mode Processing

A sophisticated **AI-powered fraud detection system** for blockchain transactions with **dual processing modes**: Scheduled/Batch and Real-Time.

> **Latest Update**: Complete project organization - all files organized into logical directories for production-ready scalability.

---

## 🎯 Quick Navigation

| Need | Location |
|------|----------|
| **🚀 Quick Start** | [QUICK_START_DUAL_MODE.md](documentation/guides/QUICK_START_DUAL_MODE.md) |
| **📚 Full Documentation** | [documentation/README.md](documentation/README.md) |
| **🏗️ System Architecture** | [documentation/architecture/](documentation/architecture/) |
| **📖 Setup Guides** | [documentation/guides/](documentation/guides/) |
| **🔍 API Reference** | [documentation/api/](documentation/api/) |
| **✅ Completion Status** | [documentation/references/COMPLETION_CHECKLIST.md](documentation/references/COMPLETION_CHECKLIST.md) |

---

## ✨ Features

### 🔄 **Dual Processing Modes**

#### 1️⃣ Scheduled Mode (Batch Processing)
```
- Extract blockchain data every X minutes
- Train ML models continuously
- Full data storage and history
- Comprehensive fraud analysis
- Best for: Deep insights & trend analysis
```

#### 2️⃣ Real-Time Mode (Stream Processing)
```
- Process transactions instantly
- Use pre-trained models for inference
- Minimal storage (results only)
- <200ms detection latency
- Best for: Real-time alerts & live monitoring
```

### 🤖 **ML Fraud Detection**
- **Random Forest** classifier for pattern detection
- **Isolation Forest** for anomaly detection
- Dual-model consensus for high confidence
- Continuous model retraining in scheduled mode

### 📊 **Interactive Dashboard**
- Real-time transaction monitoring
- Mode-aware UI (scheduled vs real-time)
- Detailed fraud analysis and insights
- Transaction filtering and search
- Statistical overview and metrics

### 🔐 **Blockchain Integration**
- Direct Ethereum RPC connection
- Web3.py for blockchain interaction
- Support for mainnet/testnet
- Gas analysis and transaction tracking

---

## 📁 Project Structure

```
blockchain-ml/
├─ 📁 src/                           ← SOURCE CODE
│  ├─ backend/                       ← PYTHON BACKEND
│  │  ├─ etl/                        ← Extract-Transform-Load
│  │  ├─ ml/                         ← Machine Learning Models
│  │  ├─ api/                        ← Flask REST API
│  │  └─ processing/                 ← Schedulers & Processing
│  │
│  └─ frontend/                      ← REACT APP
│     └─ src/components/             ← UI Components
│
├─ 📁 documentation/                 ← ALL DOCS (20+ FILES)
│  ├─ guides/                        ← Setup & Usage Guides
│  ├─ architecture/                  ← Design & Technical Docs
│  ├─ api/                           ← API Documentation
│  ├─ references/                    ← Status & Checklists
│  └─ legacy/                        ← Previous Docs
│
├─ 📁 scripts/                       ← AUTOMATION SCRIPTS
│  ├─ ai_start.sh                   ← Start AI backend
│  ├─ realtime_start.sh             ← Start real-time mode
│  ├─ start_dashboard.sh            ← Start dashboard
│  ├─ start_react.sh                ← Start React frontend
│  └─ install.sh                    ← Installation script
│
├─ 📁 docker/                        ← DOCKER CONFIGURATION
│  ├─ Dockerfile
│  └─ docker-compose.yml
│
├─ 📁 config/                        ← CONFIGURATION FILES
│  ├─ .env
│  ├─ .dockerignore
│  └─ requirements.txt
│
└─ 📄 README.md                      ← THIS FILE
```

---

## 🚀 Quick Start

### **1. Clone & Setup**
```bash
cd /home/sugangokul/Desktop/blockchain-ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Configure Environment**
```bash
cp config/.env .env
# Edit .env with your settings
export RPC_URL="your-ethereum-rpc-url"
export DATABASE_URL="your-database-url"
```

### **3. Start the System**

**Option A: Scheduled Mode (ML Training)**
```bash
bash scripts/ai_start.sh
```

**Option B: Real-Time Mode (Instant Detection)**
```bash
bash scripts/realtime_start.sh
```

### **4. Launch Dashboard**
```bash
bash scripts/start_react.sh
# Open http://localhost:3000
```

---

## 📚 Documentation Index

### **Getting Started**
- [Quick Start Guide](documentation/guides/QUICK_START_DUAL_MODE.md)
- [Installation Guide](documentation/guides/AI_SETUP_GUIDE.md)
- [Dashboard Setup](documentation/guides/DASHBOARD_README.md)

### **Architecture & Design**
- [System Architecture](documentation/architecture/VISUAL_ARCHITECTURE.md)
- [Code Structure](documentation/architecture/CODE_STRUCTURE.md)
- [ETL Pipeline Design](documentation/architecture/ETL_PIPELINE.md)
- [ML Implementation](documentation/architecture/AI_FRAUD_DETECTION.md)

### **Guides**
- [Testing Guide](documentation/guides/TESTING_GUIDE.md)
- [Deployment Guide](documentation/guides/DEPLOYMENT_GUIDE.md)
- [Scheduling Guide](documentation/guides/SCHEDULING_GUIDE.md)
- [React Setup](documentation/guides/REACT_SETUP.md)

### **References**
- [API Reference](documentation/api/)
- [Completion Checklist](documentation/references/COMPLETION_CHECKLIST.md)
- [Implementation Status](documentation/references/IMPLEMENTATION_COMPLETE.md)
- [What Was Added](documentation/references/WHAT_WAS_ADDED.txt)

---

## 🔧 System Architecture

### **Backend Components**

```
ETL Pipeline (Extract → Transform → Load)
    ↓
AI Models (Train & Predict)
    ↓
Flask API (REST Endpoints)
    ↓
Dashboard (React Frontend)
```

### **Data Flow**

**Scheduled Mode:**
```
1. Extract blocks from Ethereum RPC
2. Transform raw data into analysis format
3. Train ML models on historical data
4. Predict fraud on current transactions
5. Store all data in PostgreSQL
6. Display results in dashboard
```

**Real-Time Mode:**
```
1. Stream blocks from Ethereum RPC
2. Transform to analysis format
3. Use pre-trained models for inference
4. Return instant predictions
5. Store results only (minimal storage)
6. Update dashboard in real-time
```

---

## 🛠️ Technology Stack

### **Backend**
- **Python 3.12** - Main language
- **Flask** - REST API framework
- **SQLAlchemy** - ORM for database
- **scikit-learn** - ML models
- **Web3.py** - Blockchain interaction
- **PostgreSQL** - Data storage
- **APScheduler** - Job scheduling

### **Frontend**
- **React 18** - UI framework
- **Vite** - Build tool
- **Material-UI** - Component library
- **Framer Motion** - Animations
- **Axios** - API communication

### **DevOps**
- **Docker** - Containerization
- **Docker Compose** - Multi-container setup

---

## 📊 Key Features Comparison

| Feature | Scheduled Mode | Real-Time Mode |
|---------|:--:|:--:|
| **Processing** | Batch (every X min) | Stream (instant) |
| **Model Training** | ✅ Continuous | ❌ Pre-trained only |
| **Data Storage** | ✅ Full history | ❌ Results only |
| **Latency** | 1-2 minutes | <200ms |
| **Storage Size** | Large (~GB) | Small (~MB) |
| **Best For** | Analysis & Trends | Live Monitoring |

---

## 🎯 Processing Flow

### **Scheduled Mode Workflow**
```
START
  ↓
Extract blocks from chain
  ↓
Transform to DataFrame
  ↓
Train models on data
  ↓
Predict fraud scores
  ↓
Store results & models
  ↓
Update dashboard
  ↓
SLEEP (X minutes)
  ↓
REPEAT
```

### **Real-Time Mode Workflow**
```
START
  ↓
Stream blocks from chain
  ↓
Transform to DataFrame
  ↓
Load pre-trained models
  ↓
Predict fraud instantly
  ↓
Store results only
  ↓
Send to dashboard
  ↓
REPEAT
```

---

## 🧪 Testing

```bash
# Test ETL Pipeline
python src/backend/processing/test_etl.py

# Test ML Models
python src/backend/ml/train_ai_model.py

# Run scheduled processing
python src/backend/etl/main_etl.py

# Test real-time streaming
python src/backend/ml/realtime_processor.py
```

---

## 📈 API Endpoints

### **Mode Selection**
```
GET /api/options?mode=scheduled|realtime
→ Returns available processing options for the mode
```

### **Transaction Processing**
```
POST /api/transactions
{
  "mode": "scheduled|realtime",
  "option": "option_name",
  "block_count": 100
}
→ Process and return fraud detection results
```

### **Dashboard**
```
GET / → Main dashboard UI
GET /dashboard → Dashboard data view
```

---

## 🔐 Configuration

### **Environment Variables**
```bash
# Blockchain
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/blockchain_db

# Processing
BATCH_SIZE=10
PROCESSING_MODE=scheduled|realtime
```

---

## 📦 Installation

### **With Docker**
```bash
docker-compose up -d
```

### **Local Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python src/backend/processing/test_etl.py

# Start services
bash scripts/ai_start.sh
bash scripts/start_react.sh
```

---

## 🤝 Project Status

✅ **Completed**
- Dual-mode processing architecture
- ML fraud detection models
- Interactive React dashboard
- Flask REST API
- ETL pipeline
- Comprehensive documentation
- Complete file organization

📊 **Statistics**
- 200+ lines of ML code
- 400+ lines of UI components
- 1000+ lines of backend
- 5000+ lines of documentation
- 50+ organized files

---

## 📞 Support

- **Quick Help**: See [QUICK_REFERENCE.md](documentation/references/QUICK_REFERENCE.md)
- **Issues**: Check [COMPLETION_CHECKLIST.md](documentation/references/COMPLETION_CHECKLIST.md)
- **Architecture**: Read [VISUAL_ARCHITECTURE.md](documentation/architecture/VISUAL_ARCHITECTURE.md)

---

## 📄 License

This project is organized and maintained for educational purposes.

---

**Last Updated**: January 15, 2026  
**Status**: ✅ Production Ready  
**Organization Level**: 🌟🌟🌟🌟🌟 (100% Complete)

