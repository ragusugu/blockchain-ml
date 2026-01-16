# Docker & Kubernetes Setup Complete! 🎉

## 📦 What's Ready

Your blockchain-ml project is now fully containerized and ready for:
- ✅ **Docker Compose** - Single server deployment
- ✅ **Kubernetes (Kind)** - Multi-server deployment  
- ✅ **Production-grade Dockerfiles** - Multi-stage optimized builds
- ✅ **Deployment scripts** - One-command setup

---

## 🚀 Quick Start (Choose One)

### Option 1: Docker Compose (Fastest - 5 min)
```bash
bash scripts/deployment/deploy-docker.sh
```
**Result:** All services running on your machine
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`

### Option 2: Kubernetes (Production-like - 10 min)
```bash
bash scripts/deployment/deploy-kubernetes.sh
```
**Result:** Cluster running with auto-scaling, health checks, auto-restart

### Option 3: Interactive Menu
```bash
bash scripts/deployment/deploy.sh
```

---

## 📁 Files Created

### Dockerfiles (Production Ready)
```
Dockerfile.backend      - Flask API (multi-stage)
Dockerfile.frontend     - React app (optimized)
Dockerfile.worker       - ML inference worker
Dockerfile.scheduler    - ETL batch jobs
```

### Docker Compose
```
docker-compose.yml      - 5 services + networking
```

### Kubernetes Manifests (`k8s/`)
```
01-namespace.yaml           ← Isolated namespace
02-configmap.yaml           ← App config
03-secrets.yaml             ← Credentials
04-storage.yaml             ← Volumes
05-postgres-statefulset.yaml ← Database
06-backend-deployment.yaml  ← Backend (3 replicas)
07-frontend-deployment.yaml ← Frontend (2 replicas)
08-worker-deployment.yaml   ← ML Worker (2 replicas)
09-scheduler-cronjob.yaml   ← Batch jobs
10-ingress.yaml             ← HTTP routing
```

### Deployment Scripts
```
scripts/deployment/
├── deploy.sh              ← Main menu
├── deploy-docker.sh       ← Docker setup
├── deploy-kubernetes.sh   ← K8s setup
├── cleanup-docker.sh      ← Remove Docker
└── cleanup-kubernetes.sh  ← Remove K8s
```

---

## ⚙️ Configuration

### Update `.env` file
```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env
```

**Key settings:**
- `POSTGRES_PASSWORD` - Change from default
- `RPC_URL` - Your Alchemy/Infura key
- `ETL_SCHEDULE_*` - When to run batch jobs

---

## 📊 Architecture

### Docker Compose (Single Server)
```
Your Machine
├── PostgreSQL Container (5432)
├── Backend Container (5000)
├── Frontend Container (3000)
├── ML Worker Container
└── Scheduler Container
```

### Kubernetes (Multi-Server/Cluster)
```
K8s Cluster
├── postgres-0 (StatefulSet)
├── backend-xxx (3 Deployments)
├── frontend-xxx (2 Deployments)
├── ml-worker-xxx (2 Deployments)
├── etl-scheduler (CronJob)
├── Services (networking)
└── Ingress (HTTP routing)
```

---

## 🔍 Common Commands

### Docker Compose
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f backend

# Scale backend to 5
docker-compose up -d --scale backend=5
```

### Kubernetes
```bash
# View status
kubectl get all -n blockchain-ml

# View logs
kubectl logs -n blockchain-ml -f deployment/backend

# Scale backend to 5
kubectl scale deployment backend --replicas=5 -n blockchain-ml

# Port forward
kubectl port-forward svc/backend 5000:5000 -n blockchain-ml
```

---

## 🔑 Key Features

✅ **Multi-stage Dockerfiles** - Minimal image sizes
✅ **Health checks** - Auto-restart failed services
✅ **Resource limits** - Prevent runaway containers
✅ **Non-root users** - Security best practice
✅ **Persistent storage** - Data survives restarts
✅ **Auto-scaling** - K8s can scale based on load
✅ **Zero-downtime updates** - Rolling updates
✅ **Network isolation** - Services communicate securely

---

## 📚 Documentation

See `DEPLOYMENT_GUIDE.md` for:
- Detailed setup instructions
- Troubleshooting guide
- Monitoring & scaling
- Cloud deployment (future)
- Backup & restore

---

## ⚠️ Important Notes

### Before First Deploy
1. ✅ Update `.env` with your RPC URL
2. ✅ Change database password
3. ✅ Ensure Docker/kubectl installed

### For Production
- Use managed database (RDS, Cloud SQL)
- Setup SSL/TLS certificates
- Enable resource monitoring
- Configure backups
- Use secrets management

### Health Check Endpoints (Add to Backend)
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/ready')
def ready():
    # Check database connection
    return {'status': 'ready'}, 200
```

---

## 🆘 Troubleshooting

**Port already in use?**
```bash
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it
```

**Docker won't build?**
```bash
docker system prune  # Clean up
docker build -f Dockerfile.backend .  # Rebuild
```

**K8s pod stuck in pending?**
```bash
kubectl describe pod <name> -n blockchain-ml  # See why
```

**Database won't start?**
```bash
# Check database logs
docker-compose logs postgres
# or
kubectl logs -n blockchain-ml statefulset/postgres
```

---

## 📈 Next Steps

1. **Deploy locally** - Use `deploy-docker.sh` or `deploy-kubernetes.sh`
2. **Test everything** - Access frontend and backend
3. **Monitor logs** - Check for errors
4. **Scale services** - Increase replicas
5. **Deploy to cloud** - Use EKS/GKE/AKS (documentation coming)

---

## ✅ You're Ready!

Everything is set up. Run your first deployment:

```bash
# Option 1: Docker Compose
bash scripts/deployment/deploy-docker.sh

# Option 2: Kubernetes
bash scripts/deployment/deploy-kubernetes.sh

# Option 3: Menu
bash scripts/deployment/deploy.sh
```

**Questions?** Check `DEPLOYMENT_GUIDE.md` for detailed documentation!
