# Blockchain ML Fraud Detection - Setup & Deployment

## Quick Start

### Prerequisites
- Docker & Kubernetes (Kind)
- Python 3.12+
- Node.js 18+

### 1. Start the System

```bash
./start.sh
```

This will:
- Start Kind cluster
- Build & load Docker images
- Deploy to Kubernetes
- Start port-forwards with auto-restart monitoring

### 2. Access the Dashboard

- **Local:** http://localhost:3000
- **Cloudflare Tunnel:** https://drinks-saves-plates-motorola.trycloudflare.com
- **Backend API:** http://localhost:5000

### 3. Monitor Port-Forwards

The system auto-monitors and restarts port-forwards if they crash:

```bash
tail -f /tmp/port_monitor.log
```

## Directory Structure

```
blockchain-ml/
├── src/                      # Source code
│   ├── frontend/            # React dashboard (Vite)
│   └── backend/             # Python Flask API
├── docker/                  # Docker images
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── Dockerfile.worker
│   └── Dockerfile.scheduler
├── k8s/                     # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── postgres-statefulset.yaml
│   └── ...
├── scripts/                 # Utility scripts
│   └── keep_ports_alive.sh  # Auto-restart port-forwards
├── config/                  # Configuration files
├── documentation/           # Project documentation
└── README.md               # This file
```

## Features

### Batch Mode (Scheduled Processing)
- Process blockchain blocks in batches
- Train ML models periodically
- Full PostgreSQL history storage
- Configurable scheduling

**Options:**
1. **Standard Batch Processing** - Full ML model with training
2. **Enhanced Batch** - Dual anomaly detection layer

### Real-Time Mode (Stream Processing)
- Live fraud detection as transactions occur
- Immediate database storage
- Live dashboard updates
- Sub-100ms detection

**Options:**
1. **Real-Time Stream** - Instant detection
2. **Real-Time Advanced** - With anomaly detection

## Usage

1. **Select Mode** (Batch or Real-Time)
2. **Select Processing Option** (1 or 2)
3. **Configure** (Block count, Schedule)
4. **Fetch & Analyze** button
5. **View Results** (Statistics, Transactions, Details)
6. **Enable Auto-Refresh** (Optional) - Schedule automatic updates

## Features Included

✅ Mode switcher in header (instant switching)
✅ Refresh counter (Shows total refreshes in scheduled mode)
✅ Transaction hash integration (Copy to clipboard, Open in Etherscan)
✅ Success rate display (Fixed NaN issue)
✅ Auto-restart port-forwards (No more broken URLs)
✅ Job timeout handling (120s timeout with fallback API)
✅ Complete state management (No contamination between modes)
✅ Error handling (Fallback to direct API if async fails)

## Troubleshooting

### URLs Broken?
The auto-monitor should restart them within 5 seconds. Check:
```bash
pgrep -f "kubectl port-forward"
```

### Timeout Error?
Keep block count at 1 for fastest processing. The system has:
- 120s axios timeout
- 110s async polling
- Fallback to direct API

### Mode Switching Issues?
Browser console shows detailed logs of all actions. Open DevTools (F12) and check Console tab.

## Docker Images

All images are automatically built with `--no-cache` for clean builds:
- `blockchain-ml-backend:latest` - Python Flask + ML models
- `blockchain-ml-frontend:latest` - React dashboard
- `blockchain-ml-ml-worker:latest` - Background processing
- `blockchain-ml-scheduler:latest` - Scheduled jobs

## Database

PostgreSQL stores:
- All transactions analyzed
- Fraud detection results
- ML model training data

Accessible via: `blockchain_user` (configured in Kubernetes secret)

## Support

Check documentation for detailed guides:
- `documentation/guides/` - Step-by-step guides
- `documentation/architecture/` - Technical architecture
- `documentation/references/` - API reference

---

**Last Updated:** January 16, 2026
**Status:** Production Ready ✅
