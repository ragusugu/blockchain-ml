# Blockchain ML - Fraud Detection System

A production-ready blockchain fraud detection system using machine learning with Docker & Kubernetes deployment.

## 🚀 Quick Start

### Option 1: Docker Compose (5 minutes)
```bash
cp .env.example .env
bash scripts/deployment/deploy-docker.sh
```

### Option 2: Kubernetes (15 minutes)
```bash
cp .env.example .env
bash scripts/deployment/deploy-kubernetes.sh
```

**Access Dashboard:** http://localhost:3000

---

## 📁 Project Structure

```
blockchain-ml/
├── src/
│   ├── backend/                 # Flask API, ETL, ML, MCP, processing utilities
│   │   ├── api/                 # Dashboard API entrypoint
│   │   ├── etl/                 # Extract/transform/load and streaming
│   │   ├── ml/                  # Fraud model training and inference
│   │   ├── processing/          # Scheduler/manual ETL helpers
│   │   └── utils/               # Operational utilities
│   └── frontend/                # Vite React dashboard
├── tests/                       # Backend unit tests
├── docker/                      # Dockerfiles, Compose, nginx
├── k8s/                         # Kubernetes manifests
├── scripts/                     # Local, streaming, and deployment helpers
├── documentation/               # Guides, architecture notes, archive
├── memory-bank/                 # Maintainer context for future sessions
└── requirements.txt             # Python dependencies
```

---

## 🔧 Configuration

Edit `.env` for settings:
```bash
# RPC Endpoint (default: public node, no auth)
RPC_URL=https://ethereum.publicnode.com

# Database
POSTGRES_USER=blockchain_user
POSTGRES_PASSWORD=change_me_to_secure_password

# ML Settings
FRAUD_THRESHOLD=0.7
BATCH_SIZE=10
```

See `.env.example` for RPC options.

---

## 📚 Documentation

- [Documentation Index](documentation/README.md) - Full project documentation
- [Quick Start](documentation/guides/QUICKSTART.md) - Getting started guide
- [Docker Setup](docker/DOCKER_KUBERNETES_README.md) - Docker details
- [Deployment Guide](documentation/guides/DEPLOYMENT_GUIDE.md) - Deployment details
- [RPC Troubleshooting](documentation/guides/RPC_CONNECTION_FIX.md) - Fix RPC connection issues
- [Kubernetes Manifests](k8s/) - K8s deployment files

---

## 🎯 Key Features

✅ Real-time fraud detection using ML
✅ Docker containerization
✅ Kubernetes orchestration with auto-scaling
✅ Open-source RPC endpoints (no API keys needed)
✅ PostgreSQL database
✅ React dashboard
✅ REST API backend
✅ **Automatic disk space management** - Cleans up when space runs low

---

## 🧹 Disk Management

Automatic cleanup keeps your system healthy:

```bash
# Check disk status
PYTHONPATH=src/backend ./venv/bin/python src/backend/utils/disk_cleanup.py

# Remove Docker Compose resources and volumes
bash scripts/deployment/cleanup-docker.sh

# Remove the local Kind Kubernetes cluster
bash scripts/deployment/cleanup-kubernetes.sh
```

---

## 🚀 Deploy Now

```bash
cp .env.example .env
bash scripts/deployment/deploy.sh
```

Then choose Docker or Kubernetes from the menu.

---

## 📖 Need Help?

```bash
# View quick reference
bash scripts/deployment/DEPLOYMENT_QUICK_REFERENCE.sh

# Check deployment status
cd docker && docker-compose ps       # Docker
kubectl get pods -n blockchain-ml   # Kubernetes

# View logs
cd docker && docker-compose logs -f backend
kubectl logs -f deployment/backend -n blockchain-ml
```

---

**Ready to deploy?** See [Quick Start Guide](documentation/guides/QUICKSTART.md)
