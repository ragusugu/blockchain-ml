# Project Structure Summary

## 📁 Complete Directory Layout

```
blockchain-ml/
│
├── 📘 Documentation
│   ├── README.md                    # Main project overview
│   ├── SETUP.md                     # Quick start guide (THIS FILE)
│   └── documentation/
│       ├── README.md                # Full documentation index
│       ├── guides/                  # Step-by-step guides
│       └── architecture/            # Technical architecture docs
│
├── 🐳 Docker & Kubernetes
│   ├── docker/
│   │   ├── Dockerfile.backend       # Python Flask backend image
│   │   ├── Dockerfile.frontend      # React frontend image  
│   │   ├── Dockerfile.worker        # ML worker image
│   │   ├── Dockerfile.scheduler     # Scheduler image
│   │   ├── nginx.conf               # Frontend web server config
│   │   └── docker-compose.yml       # Local development compose
│   │
│   └── k8s/
│       ├── backend-deployment.yaml
│       ├── frontend-deployment.yaml
│       ├── ml-worker-deployment.yaml
│       ├── postgres-statefulset.yaml
│       ├── configmap.yaml           # Environment variables
│       ├── secret.yaml              # Database credentials
│       └── ingress.yaml             # Network ingress
│
├── 💻 Source Code
│   └── src/
│       ├── backend/
│       │   ├── api/
│       │   │   └── ai_dashboard.py  # Main Flask API (endpoints)
│       │   ├── etl/
│       │   │   ├── extract.py       # Block extraction
│       │   │   ├── transform.py     # Data transformation
│       │   │   └── main_etl.py      # ETL orchestration
│       │   ├── ml/
│       │   │   ├── ai_fraud_detector.py
│       │   │   ├── ai_integration.py
│       │   │   └── train_ai_model.py
│       │   └── processing/
│       │       ├── scheduler.py
│       │       └── test_etl.py
│       │
│       └── frontend/
│           ├── src/
│           │   ├── App.jsx           # Main application (MODE SWITCHING)
│           │   ├── components/       # React components
│           │   │   ├── Header.jsx    # Header with mode switcher
│           │   │   ├── ModeSelector.jsx
│           │   │   ├── OptionCard.jsx
│           │   │   ├── StatCard.jsx
│           │   │   ├── TransactionTable.jsx
│           │   │   └── ...
│           │   └── main.jsx
│           ├── package.json
│           ├── vite.config.js
│           └── index.html
│
├── 🛠️ Scripts & Config
│   ├── start.sh                     # Main startup script
│   ├── scripts/
│   │   └── keep_ports_alive.sh      # Auto-restart port-forwards
│   ├── config/                      # Application configs
│   ├── setup/                       # Setup utilities
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment variables
│
├── 📚 Configuration
│   ├── .gitignore
│   ├── .env.example
│   └── .vscode/
│       ├── settings.json            # VS Code workspace settings
│       ├── launch.json              # Debug configuration
│       └── tasks.json               # Build tasks
│
└── 🐍 Virtual Environment
    └── venv/                        # Python virtual environment

```

## 🎯 Key Features

| Feature | Location | Status |
|---------|----------|--------|
| Mode Switcher (Batch/Real-Time) | Header.jsx, App.jsx | ✅ Working |
| Refresh Counter | App.jsx line 91+ | ✅ Working |
| Etherscan Integration | TransactionTable.jsx | ✅ Working |
| Async Job API | ai_dashboard.py:257 | ✅ Working |
| Port-Forward Auto-Restart | scripts/keep_ports_alive.sh | ✅ Working |
| State Management | App.jsx (optimized) | ✅ Working |
| Error Handling | App.jsx (fallback API) | ✅ Working |

## 🚀 Deployment Flow

```
User Action
    ↓
React Frontend (App.jsx)
    ↓
Flask API (ai_dashboard.py)
    ↓
ETL Pipeline (extract → transform)
    ↓
ML Models (fraud detection)
    ↓
PostgreSQL (storage)
    ↓
Display Results (React Dashboard)
```

## 📊 API Endpoints

### Transaction Processing
- `POST /api/transactions/async` - Start async job
- `GET /api/transactions/job/<job_id>` - Poll job status
- `POST /api/transactions` - Direct synchronous call (fallback)

### System Status
- `GET /api/health` - System health check
- `GET /api/stats` - Blockchain statistics
- `GET /api/options?mode=<scheduled|realtime>` - Processing options
- `POST /api/model-toggle` - Enable/disable AI model

### Data Access
- `GET /api/transaction/<hash>` - Get transaction details

## 🧹 Cleanup Performed

✅ Removed temporary files (nohup.out, fraud_model.pkl)
✅ Removed old scripts (cleanup.sh, deploy-fix.sh, etc.)
✅ Removed duplicate documentation (docs/ folder)
✅ Removed corrupted filenames
✅ Removed empty deploy folder
✅ Organized scripts into proper folders
✅ Consolidated documentation

## 📝 Code Quality

- **Frontend:** React 18 with Material-UI components
- **Backend:** Flask with async job support
- **State Management:** Optimized sessionStorage + React state
- **Error Handling:** Comprehensive with fallback mechanisms
- **Logging:** Console debugging for all major actions
- **Testing:** Tested for mode switching, API calls, UI interactions

---

**Total Size:** ~2GB (including venv and node_modules)
**Docker Images:** 4 (backend, frontend, worker, scheduler)
**Database:** PostgreSQL
**Status:** ✅ Production Ready
