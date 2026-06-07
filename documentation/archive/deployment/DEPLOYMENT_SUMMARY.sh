#!/usr/bin/env bash

# Display deployment summary
cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                  ✅ DEPLOYMENT SCRIPTS SUCCESSFULLY CREATED                 ║
║                        Complete Docker & Kubernetes Setup                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

📦 NEW FILES CREATED:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  1. scripts/deployment/complete-deployment.sh                               │
│     └─ 600+ lines of production-ready code                                 │
│     └─ Complete reset and fresh deployment                                 │
│     └─ Docker + Kubernetes management                                      │
│     └─ Optional Python environment setup                                   │
│     └─ Comprehensive error handling & logging                              │
│                                                                              │
│  2. DEPLOYMENT_GUIDE.md                                                    │
│     └─ Complete user documentation (600+ lines)                            │
│     └─ Configuration instructions                                          │
│     └─ Troubleshooting section                                             │
│     └─ CI/CD integration examples                                          │
│     └─ Performance optimization tips                                       │
│                                                                              │
│  3. scripts/deployment/DEPLOYMENT_QUICK_REFERENCE.sh                       │
│     └─ Bash function shortcuts                                             │
│     └─ Quick access to common operations                                   │
│     └─ Pre-built functions for easy use                                    │
│                                                                              │
│  4. DEPLOYMENT_SETUP.md                                                    │
│     └─ Quick start guide                                                   │
│     └─ Feature overview                                                    │
│     └─ Common scenarios                                                    │
│     └─ Security considerations                                             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


🎯 CORE FEATURES:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ✅ DOCKER MANAGEMENT:                                                      │
│     • Clean up all containers (graceful stop)                              │
│     • Delete all blockchain-ml images                                      │
│     • Remove volumes and networks                                          │
│     • Build fresh Docker images                                            │
│     • Deploy with Docker Compose                                           │
│     • Health checks and verification                                       │
│                                                                              │
│  ✅ KUBERNETES MANAGEMENT:                                                  │
│     • Delete namespaces (cascading resources)                              │
│     • Delete Kind clusters                                                 │
│     • Create fresh clusters                                                │
│     • Load Docker images into cluster                                      │
│     • Apply Kubernetes manifests                                           │
│     • Verify pod deployment status                                         │
│                                                                              │
│  ✅ PYTHON ENVIRONMENT (Optional):                                          │
│     • Create virtual environment                                           │
│     • Install from requirements.txt                                        │
│     • Use --python-setup flag                                              │
│                                                                              │
│  ✅ LOGGING & MONITORING:                                                   │
│     • Complete timestamped logs                                            │
│     • Color-coded output                                                   │
│     • Progress tracking                                                    │
│     • Error reporting                                                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


🚀 QUICK START - Choose Your Setup:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Full Deployment (Docker + Kubernetes):                                    │
│  $ cd scripts/deployment                                                   │
│  $ ./complete-deployment.sh                                                │
│                                                                              │
│  Docker Only (Faster):                                                     │
│  $ ./complete-deployment.sh --docker-only                                  │
│                                                                              │
│  Kubernetes Only:                                                          │
│  $ ./complete-deployment.sh --k8s-only                                     │
│                                                                              │
│  With Python Setup:                                                        │
│  $ ./complete-deployment.sh --python-setup                                 │
│                                                                              │
│  Reuse Existing (Skip Cleanup):                                            │
│  $ ./complete-deployment.sh --skip-cleanup                                 │
│                                                                              │
│  Show Help:                                                                │
│  $ ./complete-deployment.sh --help                                         │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


🔧 WHAT GETS CLEANED UP:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  DOCKER:                                                                    │
│  ✅ All running containers (stopped gracefully)                            │
│  ✅ All blockchain-ml Docker images                                        │
│  ✅ Dangling images                                                        │
│  ✅ Volumes (postgres_data, models_cache)                                  │
│  ✅ Networks (blockchain-network)                                          │
│                                                                              │
│  KUBERNETES:                                                               │
│  ✅ Namespace and all resources inside                                     │
│  ✅ Kind cluster                                                           │
│  ✅ PersistentVolumeClaims                                                 │
│  ✅ ConfigMaps and Secrets                                                 │
│  ✅ Kubeconfig entries                                                     │
│                                                                              │
│  NOT DELETED (Safe):                                                       │
│  ✅ Docker daemon itself                                                   │
│  ✅ Kubernetes CLI tools                                                   │
│  ✅ Python system packages                                                 │
│  ✅ Other projects' resources                                              │
│  ✅ Source code files                                                      │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


📊 DEPLOYMENT PHASES:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  1️⃣  Prerequisites Check                                                    │
│      └─ Verify Docker, Docker Compose, kubectl, Kind                      │
│                                                                              │
│  2️⃣  Cleanup Phase (unless --skip-cleanup)                                  │
│      ├─ Docker: Stop → Remove containers → Clean volumes/networks         │
│      └─ K8s: Delete namespace → Delete cluster                            │
│                                                                              │
│  3️⃣  Python Setup (if --python-setup)                                       │
│      ├─ Create virtual environment                                         │
│      └─ Install requirements.txt                                           │
│                                                                              │
│  4️⃣  Docker Setup (unless --k8s-only)                                       │
│      ├─ Create .env configuration                                          │
│      ├─ Build Docker images                                                │
│      └─ Start services                                                     │
│                                                                              │
│  5️⃣  Kubernetes Setup (unless --docker-only)                                │
│      ├─ Create cluster                                                     │
│      ├─ Load Docker images                                                 │
│      ├─ Create namespace                                                   │
│      └─ Deploy manifests                                                   │
│                                                                              │
│  6️⃣  Verification & Access Info                                             │
│      ├─ List containers/pods                                               │
│      └─ Show service URLs                                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


🎛️ COMMAND OPTIONS:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  --docker-only      Deploy only Docker (skip Kubernetes)                   │
│  --k8s-only        Deploy only Kubernetes (skip Docker)                    │
│  --python-setup    Include Python virtual environment setup                │
│  --skip-cleanup    Skip cleanup phase (reuse existing resources)           │
│  --help            Show help message                                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


🔗 SERVICE ACCESS AFTER DEPLOYMENT:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  DOCKER SERVICES:                                                          │
│  • Backend API:    http://localhost:5000                                  │
│  • Frontend:       http://localhost:3000                                  │
│  • PostgreSQL:     localhost:5432                                          │
│                                                                              │
│  KUBERNETES SERVICES (via port-forward):                                   │
│  $ kubectl port-forward -n blockchain-ml svc/backend 5000:5000            │
│  $ kubectl port-forward -n blockchain-ml svc/frontend 3000:3000           │
│  $ kubectl port-forward -n blockchain-ml svc/postgres 5432:5432           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


⚙️  CONFIGURATION BEFORE DEPLOYMENT:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Update docker/.env:                                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ POSTGRES_PASSWORD=change_me_to_secure_password    ⚠️  UPDATE          │ │
│  │ RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY  ⚠️  UPDATE    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  Update k8s/03-secrets.yaml (for Kubernetes):                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ db-password: "your-secure-password"                                    │ │
│  │ rpc-url: "your-rpc-url"                                                │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


🎯 COMMON SCENARIOS:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Development Setup:                                                        │
│  $ ./complete-deployment.sh --docker-only --python-setup                   │
│                                                                              │
│  Testing/CI Pipeline:                                                      │
│  $ ./complete-deployment.sh                                                │
│                                                                              │
│  Production Kubernetes:                                                    │
│  $ ./complete-deployment.sh --k8s-only --skip-cleanup                      │
│                                                                              │
│  Incremental Updates:                                                      │
│  $ ./complete-deployment.sh --skip-cleanup --docker-only                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


📚 DOCUMENTATION:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  📄 DEPLOYMENT_SETUP.md                                                    │
│     └─ Quick start guide and feature overview                             │
│                                                                              │
│  📄 DEPLOYMENT_GUIDE.md                                                    │
│     └─ Complete deployment documentation                                  │
│     └─ Configuration guide                                                │
│     └─ Troubleshooting section                                            │
│     └─ CI/CD integration examples                                         │
│                                                                              │
│  🔧 scripts/deployment/DEPLOYMENT_QUICK_REFERENCE.sh                       │
│     └─ Bash function shortcuts                                            │
│     └─ Pre-built functions for quick operations                           │
│                                                                              │
│  Usage: ./complete-deployment.sh --help                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


💡 QUICK REFERENCE FUNCTIONS:
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Source quick reference:                                                   │
│  $ source scripts/deployment/DEPLOYMENT_QUICK_REFERENCE.sh                 │
│                                                                              │
│  Available functions:                                                      │
│  • deploy_full              Full deployment                                │
│  • deploy_docker            Docker only                                    │
│  • deploy_k8s               Kubernetes only                                │
│  • cleanup_all              Clean everything                               │
│  • status_docker            Docker status                                  │
│  • status_k8s               K8s status                                     │
│  • logs_docker              View Docker logs                               │
│  • logs_k8s                 View K8s logs                                  │
│  • portforward_backend      Backend port forward                           │
│  • health_check             Check service health                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


✅ YOU'RE READY TO DEPLOY!
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  ✓ Script created and tested                                               │
│  ✓ Documentation complete                                                  │
│  ✓ Quick reference functions available                                    │
│  ✓ Error handling implemented                                              │
│  ✓ Logging configured                                                      │
│                                                                              │
│  NEXT STEPS:                                                               │
│  1. Read DEPLOYMENT_SETUP.md for overview                                  │
│  2. Read DEPLOYMENT_GUIDE.md for detailed instructions                     │
│  3. Update configuration (docker/.env and k8s/03-secrets.yaml)            │
│  4. Run: cd scripts/deployment && ./complete-deployment.sh                │
│                                                                              │
│  Questions? Check DEPLOYMENT_GUIDE.md troubleshooting section              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

EOF
