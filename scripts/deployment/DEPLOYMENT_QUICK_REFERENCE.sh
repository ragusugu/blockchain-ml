#!/bin/bash

################################################################################
# Quick Deployment Reference
# 
# This file contains quick commands for common deployment scenarios
# Source this file or copy commands as needed
################################################################################

# Color codes
export GREEN='\033[0;32m'
export RED='\033[0;31m'
export YELLOW='\033[1;33m'
export CYAN='\033[0;36m'
export NC='\033[0m'

# Script location
DEPLOYMENT_SCRIPT="./scripts/deployment/complete-deployment.sh"

################################################################################
# QUICK COMMANDS
################################################################################

# Display quick reference
show_quick_reference() {
    clear
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                    BLOCKCHAIN-ML DEPLOYMENT QUICK REFERENCE                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 COMMON SCENARIOS:

┌─ 🚀 Full Deployment (Clean Reset)
│
├─ Complete reset + Docker + Kubernetes
│  $ ./scripts/deployment/complete-deployment.sh
│
├─ Docker only (faster for dev)
│  $ ./scripts/deployment/complete-deployment.sh --docker-only
│
├─ Kubernetes only
│  $ ./scripts/deployment/complete-deployment.sh --k8s-only
│
├─ With Python environment setup
│  $ ./scripts/deployment/complete-deployment.sh --python-setup
│
└─ Skip cleanup (reuse existing resources)
   $ ./scripts/deployment/complete-deployment.sh --skip-cleanup

┌─ 🔧 Manual Operations
│
├─ Clean up Docker only
│  $ cd docker && docker-compose down -v
│
├─ Clean up Kubernetes only
│  $ kubectl delete namespace blockchain-ml
│  $ kind delete cluster --name blockchain-ml
│
├─ View Docker logs
│  $ docker-compose -f docker/docker-compose.yml logs -f
│
├─ View Kubernetes logs
│  $ kubectl logs -f pod/<pod-name> -n blockchain-ml
│
└─ Port forward to services
   $ kubectl port-forward -n blockchain-ml svc/backend 5000:5000
   $ kubectl port-forward -n blockchain-ml svc/frontend 3000:3000

┌─ 📊 Status & Information
│
├─ Docker container status
│  $ docker ps
│
├─ Kubernetes pod status
│  $ kubectl get pods -n blockchain-ml
│
├─ View deployment logs
│  $ tail -f deployment-*.log
│
└─ List available contexts
   $ kubectl config get-contexts

┌─ 🔗 Access Services
│
├─ Docker services
│  Backend:  http://localhost:5000
│  Frontend: http://localhost:3000
│  Database: localhost:5432
│
└─ Kubernetes (after port-forward)
   Backend:  http://localhost:5000
   Frontend: http://localhost:3000
   Database: localhost:5432

┌─ ⚙️  Configuration Files
│
├─ Docker environment
│  docker/.env
│
├─ Kubernetes secrets
│  k8s/03-secrets.yaml
│
├─ Database schema
│  k8s/04-storage.yaml
│  k8s/05-postgres-statefulset.yaml
│
└─ Deployment manifests
   k8s/06-backend-deployment.yaml
   k8s/07-frontend-deployment.yaml
   k8s/08-worker-deployment.yaml
   k8s/09-scheduler-cronjob.yaml
   k8s/10-ingress.yaml

┌─ 🐛 Troubleshooting
│
├─ Rebuild Docker images
│  $ docker-compose -f docker/docker-compose.yml build --no-cache
│
├─ Restart Docker services
│  $ docker-compose -f docker/docker-compose.yml restart
│
├─ Reset Kubernetes cluster
│  $ kind delete cluster --name blockchain-ml
│  $ ./scripts/deployment/complete-deployment.sh --k8s-only
│
├─ Check service health
│  $ curl http://localhost:5000/health
│  $ curl http://localhost:5000/ready
│
└─ View all resources
   $ kubectl get all -n blockchain-ml

┌─ 📦 Pre-requisite Installation
│
├─ macOS (brew)
│  $ brew install docker kubectl kind
│
├─ Ubuntu/Debian (apt)
│  $ sudo apt-get install docker.io python3-docker
│  $ sudo snap install kubectl --classic
│  $ go install sigs.k8s.io/kind@latest
│
├─ Or use Docker Desktop
│  https://www.docker.com/products/docker-desktop
│  (includes Docker, Docker Compose, and kubectl)
│
└─ Verify installation
   $ docker --version
   $ docker-compose --version
   $ kubectl version --client
   $ kind version

╔══════════════════════════════════════════════════════════════════════════════╗
║                         📚 For More Information                              ║
║                    Read DEPLOYMENT_GUIDE.md or use --help                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

EOF
}

# Function to run deployment with common scenarios
deploy_full() {
    echo -e "${CYAN}Running full deployment with reset...${NC}"
    "$DEPLOYMENT_SCRIPT"
}

deploy_docker() {
    echo -e "${CYAN}Deploying Docker only...${NC}"
    "$DEPLOYMENT_SCRIPT" --docker-only
}

deploy_k8s() {
    echo -e "${CYAN}Deploying Kubernetes only...${NC}"
    "$DEPLOYMENT_SCRIPT" --k8s-only
}

deploy_with_python() {
    echo -e "${CYAN}Deploying with Python environment setup...${NC}"
    "$DEPLOYMENT_SCRIPT" --python-setup
}

deploy_skip_cleanup() {
    echo -e "${CYAN}Deploying without cleanup (reuse existing)...${NC}"
    "$DEPLOYMENT_SCRIPT" --skip-cleanup
}

# Cleanup functions
cleanup_all() {
    echo -e "${YELLOW}Cleaning up all Docker and Kubernetes resources...${NC}"
    
    # Docker cleanup
    echo "Stopping Docker services..."
    cd docker && docker-compose down -v 2>/dev/null || true
    cd ..
    
    # Kubernetes cleanup
    echo "Deleting Kubernetes namespace..."
    kubectl delete namespace blockchain-ml --ignore-not-found=true 2>/dev/null || true
    
    echo "Deleting Kind cluster..."
    kind delete cluster --name blockchain-ml 2>/dev/null || true
    
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

cleanup_docker() {
    echo -e "${YELLOW}Cleaning up Docker resources...${NC}"
    cd docker && docker-compose down -v 2>/dev/null || true
    cd ..
    echo -e "${GREEN}✅ Docker cleanup completed${NC}"
}

cleanup_k8s() {
    echo -e "${YELLOW}Cleaning up Kubernetes resources...${NC}"
    kubectl delete namespace blockchain-ml --ignore-not-found=true 2>/dev/null || true
    kind delete cluster --name blockchain-ml 2>/dev/null || true
    echo -e "${GREEN}✅ Kubernetes cleanup completed${NC}"
}

# Status functions
status_docker() {
    echo -e "${CYAN}Docker Services:${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

status_k8s() {
    echo -e "${CYAN}Kubernetes Pods:${NC}"
    kubectl get pods -n blockchain-ml 2>/dev/null || echo "Kubernetes not running"
}

# Log functions
logs_docker() {
    local service="${1:-}"
    if [ -z "$service" ]; then
        cd docker && docker-compose logs -f
    else
        cd docker && docker-compose logs -f "$service"
    fi
}

logs_k8s() {
    local pod="${1:-}"
    if [ -z "$pod" ]; then
        kubectl logs -f -n blockchain-ml -l app=backend
    else
        kubectl logs -f -n blockchain-ml "$pod"
    fi
}

logs_deployment() {
    tail -f deployment-*.log
}

# Port forward
portforward_backend() {
    echo "Port forwarding backend: http://localhost:5000"
    kubectl port-forward -n blockchain-ml svc/backend 5000:5000
}

portforward_frontend() {
    echo "Port forwarding frontend: http://localhost:3000"
    kubectl port-forward -n blockchain-ml svc/frontend 3000:3000
}

portforward_postgres() {
    echo "Port forwarding PostgreSQL: localhost:5432"
    kubectl port-forward -n blockchain-ml svc/postgres 5432:5432
}

# Health checks
health_check() {
    echo -e "${CYAN}Checking services health...${NC}"
    echo ""
    
    # Docker services
    if command -v docker &> /dev/null; then
        echo -e "${CYAN}Docker:${NC}"
        curl -s http://localhost:5000/health | jq . 2>/dev/null || echo "Backend not responding"
        echo ""
    fi
    
    # Kubernetes services
    if command -v kubectl &> /dev/null; then
        echo -e "${CYAN}Kubernetes:${NC}"
        kubectl get pods -n blockchain-ml 2>/dev/null | head -5 || echo "Kubernetes not configured"
        echo ""
    fi
}

# Help
show_help() {
    cat << 'EOF'
Blockchain-ML Deployment Functions

USAGE:
  source scripts/deployment/QUICK_REFERENCE.sh
  deploy_full                 # Full deployment with reset
  deploy_docker               # Docker only
  deploy_k8s                  # Kubernetes only
  deploy_with_python          # Include Python setup
  deploy_skip_cleanup         # Skip cleanup phase
  
  cleanup_all                 # Clean Docker and K8s
  cleanup_docker              # Clean Docker only
  cleanup_k8s                 # Clean K8s only
  
  status_docker               # Show Docker status
  status_k8s                  # Show K8s status
  
  logs_docker [service]       # View Docker logs
  logs_k8s [pod]              # View K8s logs
  logs_deployment             # View deployment logs
  
  portforward_backend         # Port forward backend
  portforward_frontend        # Port forward frontend
  portforward_postgres        # Port forward database
  
  health_check                # Check service health
  show_quick_reference        # Show this reference
  show_help                   # Show this help

EXAMPLES:
  deploy_full
  cleanup_docker
  status_docker
  logs_docker backend
  portforward_backend
EOF
}

# Show reference on source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Script was executed directly
    show_quick_reference
else
    # Script was sourced
    show_quick_reference
fi
