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
├── docker/                      # Docker configuration
│   ├── Dockerfile.*            # Container definitions
│   └── docker-compose.yml      # Multi-container orchestration
├── k8s/                         # Kubernetes manifests
│   ├── 01-namespace.yaml
│   ├── 02-configmap.yaml      # RPC & app config
│   └── ...
├── scripts/deployment/          # Deployment automation
│   ├── deploy.sh              # Interactive deployment
│   ├── deploy-docker.sh       # Docker setup
│   └── deploy-kubernetes.sh   # Kubernetes setup
├── src/
│   ├── backend/               # Flask API
│   ├── frontend/              # React Dashboard
│   └── ml/                    # ML models & inference
├── config/                     # Configuration files
├── docs/                       # Documentation
│   ├── README.md             # Full documentation
│   ├── QUICK_START.md        # Quick start guide
│   └── RPC guides            # RPC configuration
└── requirements.txt           # Python dependencies
```

---

## 🔧 Configuration

Edit `.env` for settings:
```bash
# RPC Endpoint (default: eth.public-rpc.com - free, no auth)
RPC_URL=https://eth.public-rpc.com

# Database
DB_USER=postgres
DB_PASSWORD=fraud_detection

# ML Settings
FRAUD_THRESHOLD=0.7
BATCH_SIZE=100
```

See `docs/OPEN_SOURCE_RPC_GUIDE.md` for RPC options.

---

## 📚 Documentation

- [Main README](docs/README.md) - Full project documentation
- [Quick Start](docs/QUICK_START.md) - Getting started guide
- [Docker Setup](docker/DOCKER_KUBERNETES_README.md) - Docker details
- [RPC Guide](docs/OPEN_SOURCE_RPC_GUIDE.md) - RPC configuration
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
./cleanup.sh --status

# Force cleanup now
./cleanup.sh --cleanup-now
```

**Automatic monitoring** runs in background - no manual intervention needed!

📖 See [CLEANUP_QUICK_REFERENCE.md](CLEANUP_QUICK_REFERENCE.md) for details.

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
bash docs/RPC_QUICK_START.sh

# Check deployment status
docker-compose ps                    # Docker
kubectl get pods -n blockchain-ml   # Kubernetes

# View logs
docker-compose logs -f backend
kubectl logs -f deployment/backend -n blockchain-ml
```

---

**Ready to deploy?** See [Quick Start Guide](docs/QUICK_START.md)
