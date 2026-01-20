#!/bin/bash

################################################################################
# BLOCKCHAIN-ML: Complete Deployment Reset & Setup Script
# 
# This script performs a complete reset of Docker & Kubernetes setup and
# deploys the entire blockchain-ml project from scratch.
#
# Features:
# - ✅ Cleans up all existing Docker containers, images, and volumes
# - ✅ Cleans up all Kubernetes resources
# - ✅ Builds fresh Docker images
# - ✅ Deploys to Kubernetes (Kind/EKS/AKS)
# - ✅ Optional Python environment setup
# - ✅ Comprehensive error handling and logging
#
# Usage:
#   ./complete-deployment.sh                    # Interactive mode
#   ./complete-deployment.sh --skip-cleanup     # Skip cleanup phase
#   ./complete-deployment.sh --python-setup     # Include Python setup
#   ./complete-deployment.sh --k8s-only         # Kubernetes only
#   ./complete-deployment.sh --docker-only      # Docker only
#
################################################################################

set -e

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEPLOYMENT_DIR="$SCRIPT_DIR"
DOCKER_DIR="$PROJECT_ROOT/docker"
K8S_DIR="$PROJECT_ROOT/k8s"
LOG_FILE="$PROJECT_ROOT/deployment-$(date +%Y%m%d_%H%M%S).log"

# Defaults
SKIP_CLEANUP=false
PYTHON_SETUP=false
DEPLOYMENT_TYPE="all"  # all, docker, k8s
CLUSTER_NAME="blockchain-ml"
NAMESPACE="blockchain-ml"

################################################################################
# Utility Functions
################################################################################

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${CYAN}ℹ️  $1${NC}" | tee -a "$LOG_FILE"
}

separator() {
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}" | tee -a "$LOG_FILE"
}

################################################################################
# Prerequisites Check
################################################################################

check_prerequisites() {
    log "Checking prerequisites..."
    separator
    
    local missing=0
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
        missing=$((missing + 1))
    else
        success "Docker found: $(docker --version)"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed"
        missing=$((missing + 1))
    else
        success "Docker Compose found: $(docker-compose --version)"
    fi
    
    # Check kubectl (for K8s)
    if [[ "$DEPLOYMENT_TYPE" == "k8s" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        if ! command -v kubectl &> /dev/null; then
            error "kubectl is not installed"
            missing=$((missing + 1))
        else
            success "kubectl found: $(kubectl version --short --client 2>/dev/null || echo 'installed')"
        fi
    fi
    
    # Check Kind (for local K8s)
    if [[ "$DEPLOYMENT_TYPE" == "k8s" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        if ! command -v kind &> /dev/null; then
            warning "Kind is not installed (needed for local K8s clusters)"
            info "Install from: https://kind.sigs.k8s.io/docs/user/quick-start/"
        else
            success "Kind found: $(kind version)"
        fi
    fi
    
    # Check Docker daemon
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running"
        missing=$((missing + 1))
    else
        success "Docker daemon is running"
    fi
    
    if [ $missing -gt 0 ]; then
        error "Missing $missing prerequisite(s). Please install and try again."
        exit 1
    fi
    
    echo ""
}

################################################################################
# Docker Cleanup
################################################################################

cleanup_docker() {
    log "Starting Docker cleanup..."
    separator
    
    # Stop all containers
    if [ "$(docker ps -q)" ]; then
        warning "Stopping running containers..."
        docker stop $(docker ps -q) 2>/dev/null || true
        info "Waiting for containers to stop..."
        sleep 2
    fi
    
    # Remove all containers
    if [ "$(docker ps -aq)" ]; then
        warning "Removing all containers..."
        docker rm $(docker ps -aq) --force 2>/dev/null || true
    fi
    
    # Remove blockchain-ml images
    warning "Removing blockchain-ml Docker images..."
    docker rmi blockchainml:latest 2>/dev/null || true
    docker rmi blockchain-ml-frontend:latest 2>/dev/null || true
    docker rmi blockchain-ml-backend:latest 2>/dev/null || true
    docker rmi blockchain-ml-worker:latest 2>/dev/null || true
    docker rmi blockchain-ml-scheduler:latest 2>/dev/null || true
    
    # Remove dangling images
    warning "Removing dangling Docker images..."
    docker image prune -f 2>/dev/null || true
    
    # Remove volumes
    warning "Removing Docker volumes..."
    docker volume rm blockchain-postgres 2>/dev/null || true
    docker volume rm blockchain-ml_postgres_data 2>/dev/null || true
    docker volume rm blockchain-ml_models_cache 2>/dev/null || true
    docker volume prune -f 2>/dev/null || true
    
    # Remove networks
    warning "Removing Docker networks..."
    docker network rm blockchain-network 2>/dev/null || true
    docker network prune -f 2>/dev/null || true
    
    success "Docker cleanup completed"
    echo ""
}

################################################################################
# Kubernetes Cleanup
################################################################################

cleanup_kubernetes() {
    log "Starting Kubernetes cleanup..."
    separator
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        warning "kubectl not available, skipping Kubernetes cleanup"
        return 0
    fi
    
    # Delete namespace (cascades to all resources)
    warning "Deleting Kubernetes namespace '$NAMESPACE'..."
    kubectl delete namespace "$NAMESPACE" --ignore-not-found=true 2>/dev/null || true
    
    # Wait for namespace to be deleted
    info "Waiting for namespace deletion..."
    for i in {1..30}; do
        if ! kubectl get namespace "$NAMESPACE" &>/dev/null; then
            success "Namespace deleted"
            break
        fi
        if [ $i -eq 30 ]; then
            warning "Namespace deletion timed out, continuing anyway..."
        fi
        sleep 1
    done
    
    # Delete Kind cluster (if exists and not in kubeconfig)
    if command -v kind &> /dev/null; then
        warning "Checking for Kind cluster..."
        if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
            warning "Deleting Kind cluster '$CLUSTER_NAME'..."
            kind delete cluster --name "$CLUSTER_NAME" 2>/dev/null || true
            success "Kind cluster deleted"
        fi
    fi
    
    # Remove any local K8s resources
    info "Cleaning up local Kubernetes configuration..."
    
    success "Kubernetes cleanup completed"
    echo ""
}

################################################################################
# Python Environment Setup (Optional)
################################################################################

setup_python_environment() {
    log "Setting up Python environment..."
    separator
    
    cd "$PROJECT_ROOT"
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        warning "requirements.txt not found in $PROJECT_ROOT"
        return 0
    fi
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        info "Creating Python virtual environment..."
        python3 -m venv venv
        success "Virtual environment created"
    else
        info "Virtual environment already exists"
    fi
    
    # Activate and install requirements
    info "Installing Python dependencies..."
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel --quiet
    pip install -r requirements.txt --quiet
    deactivate
    
    success "Python environment setup completed"
    echo ""
}

################################################################################
# Docker Build & Deployment
################################################################################

setup_docker_environment() {
    log "Setting up Docker environment..."
    separator
    
    cd "$DOCKER_DIR"
    
    # Create .env file if not exists
    if [ ! -f ".env" ]; then
        warning "Creating .env file..."
        cat > .env << 'EOF'
# Database Configuration
POSTGRES_DB=blockchain_db
POSTGRES_USER=blockchain_user
POSTGRES_PASSWORD=change_me_to_secure_password

# Blockchain RPC
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY

# ETL Configuration
BATCH_SIZE=10
ETL_SCHEDULE_HOUR=0
ETL_SCHEDULE_MINUTE=0

# Model Configuration
MODEL_ENABLED=true
MAX_BLOCKS_PER_REQUEST=5

# Environment
FLASK_ENV=production
EOF
        info ".env file created. Please update with your settings:"
        info "  - POSTGRES_PASSWORD: Secure password"
        info "  - RPC_URL: Your Alchemy/Infura RPC URL"
    fi
    
    success ".env file ready"
}

build_docker_images() {
    log "Building Docker images..."
    separator
    
    cd "$DOCKER_DIR"
    
    info "Building all Docker images (this may take a few minutes)..."
    
    if [ -f "docker-compose.yml" ]; then
        info "Using docker-compose build..."
        docker-compose build --no-cache 2>&1 | tee -a "$LOG_FILE"
    else
        # Build individual Dockerfiles
        for dockerfile in Dockerfile.*; do
            if [ -f "$dockerfile" ]; then
                local image_name="${dockerfile/Dockerfile./blockchain-ml-}"
                info "Building $image_name from $dockerfile..."
                docker build -f "$dockerfile" -t "$image_name:latest" . 2>&1 | tee -a "$LOG_FILE"
            fi
        done
    fi
    
    success "Docker images built successfully"
    
    # List images
    info "Built Docker images:"
    docker images | grep blockchain-ml | tee -a "$LOG_FILE"
    echo ""
}

deploy_docker_compose() {
    log "Starting Docker Compose services..."
    separator
    
    cd "$DOCKER_DIR"
    
    info "Pulling base images..."
    docker-compose pull 2>&1 | tee -a "$LOG_FILE"
    
    info "Starting services..."
    docker-compose up -d 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -ne 0 ]; then
        error "Docker Compose deployment failed"
        return 1
    fi
    
    # Wait for services to be healthy
    info "Waiting for services to be healthy..."
    for i in {1..30}; do
        if docker-compose ps | grep -q "healthy"; then
            success "Services are healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            warning "Services health check timed out"
        fi
        sleep 2
    done
    
    success "Docker Compose deployment completed"
    echo ""
    
    # Show service info
    info "Running services:"
    docker-compose ps 2>&1 | tee -a "$LOG_FILE"
    echo ""
}

################################################################################
# Kubernetes Setup & Deployment
################################################################################

setup_kubernetes_cluster() {
    log "Setting up Kubernetes cluster..."
    separator
    
    if ! command -v kind &> /dev/null; then
        error "Kind is required for local Kubernetes setup"
        error "Install from: https://kind.sigs.k8s.io/docs/user/quick-start/"
        return 1
    fi
    
    # Check if cluster exists
    if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
        info "Kind cluster '$CLUSTER_NAME' already exists"
    else
        info "Creating Kind cluster '$CLUSTER_NAME'..."
        kind create cluster --name "$CLUSTER_NAME" 2>&1 | tee -a "$LOG_FILE"
        success "Kind cluster created"
    fi
    
    # Set kubeconfig context
    info "Setting kubectl context..."
    kubectl cluster-info --context "kind-${CLUSTER_NAME}" >/dev/null 2>&1
    kubectl config use-context "kind-${CLUSTER_NAME}" 2>&1 | tee -a "$LOG_FILE"
    
    success "Kubernetes cluster ready"
    echo ""
}

deploy_kubernetes_resources() {
    log "Deploying Kubernetes resources..."
    separator
    
    cd "$K8S_DIR"
    
    # Create namespace
    info "Creating namespace '$NAMESPACE'..."
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f - 2>&1 | tee -a "$LOG_FILE"
    
    # Apply Kubernetes manifests
    info "Applying Kubernetes manifests..."
    for yaml_file in *.yaml; do
        if [ -f "$yaml_file" ]; then
            info "Applying $yaml_file..."
            kubectl apply -f "$yaml_file" 2>&1 | tee -a "$LOG_FILE"
        fi
    done
    
    success "Kubernetes resources deployed"
    echo ""
    
    # Wait for deployments
    info "Waiting for deployments to be ready (this may take a few minutes)..."
    kubectl rollout status deployment -n "$NAMESPACE" --timeout=5m 2>&1 | tee -a "$LOG_FILE" || true
    
    echo ""
}

load_docker_images_to_kind() {
    log "Loading Docker images into Kind cluster..."
    separator
    
    if ! command -v kind &> /dev/null; then
        warning "Kind not available, skipping image loading"
        return 0
    fi
    
    info "Loading images into Kind cluster..."
    for image in blockchainml:latest blockchain-ml-backend:latest blockchain-ml-frontend:latest blockchain-ml-worker:latest blockchain-ml-scheduler:latest; do
        if docker image inspect "$image" &>/dev/null; then
            info "Loading $image..."
            kind load docker-image "$image" --name "$CLUSTER_NAME" 2>&1 | tee -a "$LOG_FILE" || true
        fi
    done
    
    success "Docker images loaded into Kind"
    echo ""
}

################################################################################
# Verification & Health Checks
################################################################################
# Update .env files with K8s Postgres credentials
################################################################################

update_env_files_for_k8s() {
    log "Updating .env files with K8s Postgres credentials..."
    separator
    
    local K8S_DB_PASSWORD="change-me-to-secure-password"
    local K8S_DB_USER="blockchain_user"
    local K8S_DB_NAME="blockchain_db"
    local K8S_RPC_URL="https://ethereum.publicnode.com"
    
    # Update root .env
    if [ -f "$PROJECT_ROOT/.env" ]; then
        info "Updating $PROJECT_ROOT/.env..."
        cat > "$PROJECT_ROOT/.env" << EOF
# PostgreSQL Database Credentials (K8s Postgres)
POSTGRES_DB=${K8S_DB_NAME}
POSTGRES_USER=${K8S_DB_USER}
POSTGRES_PASSWORD=${K8S_DB_PASSWORD}

# Full DATABASE_URL (K8s Postgres via port-forward to localhost:5432)
# Run: kubectl port-forward -n ${NAMESPACE} svc/postgres 5432:5432
DATABASE_URL=postgresql://${K8S_DB_USER}:${K8S_DB_PASSWORD}@127.0.0.1:5432/${K8S_DB_NAME}

# RPC URL for Ethereum
RPC_URL=${K8S_RPC_URL}
EOF
        success "Updated $PROJECT_ROOT/.env"
    fi
    
    # Update config/.env
    if [ -d "$PROJECT_ROOT/config" ]; then
        info "Updating $PROJECT_ROOT/config/.env..."
        cat > "$PROJECT_ROOT/config/.env" << EOF
# PostgreSQL Database Credentials (K8s Postgres)
POSTGRES_DB=${K8S_DB_NAME}
POSTGRES_USER=${K8S_DB_USER}
POSTGRES_PASSWORD=${K8S_DB_PASSWORD}

# Full DATABASE_URL (K8s Postgres via port-forward to localhost:5432)
# Run: kubectl port-forward -n ${NAMESPACE} svc/postgres 5432:5432
DATABASE_URL=postgresql://${K8S_DB_USER}:${K8S_DB_PASSWORD}@127.0.0.1:5432/${K8S_DB_NAME}

# RPC URL for Ethereum
RPC_URL=${K8S_RPC_URL}
EOF
        success "Updated $PROJECT_ROOT/config/.env"
    fi
    
    success ".env files updated with K8s Postgres credentials"
    info "Use port-forward to connect: kubectl port-forward -n ${NAMESPACE} svc/postgres 5432:5432"
    echo ""
}

################################################################################
# Verification & Health Checks
################################################################################

verify_deployment() {
    log "Verifying deployment..."
    separator
    
    if [[ "$DEPLOYMENT_TYPE" == "docker" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        info "Docker services:"
        docker-compose -f "$DOCKER_DIR/docker-compose.yml" ps 2>&1 | tee -a "$LOG_FILE"
        echo ""
    fi
    
    if [[ "$DEPLOYMENT_TYPE" == "k8s" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        info "Kubernetes pods:"
        kubectl get pods -n "$NAMESPACE" 2>&1 | tee -a "$LOG_FILE"
        echo ""
        
        info "Kubernetes services:"
        kubectl get svc -n "$NAMESPACE" 2>&1 | tee -a "$LOG_FILE"
        echo ""
    fi
    
    success "Deployment verification completed"
    echo ""
}

show_access_info() {
    log "Access Information"
    separator
    
    if [[ "$DEPLOYMENT_TYPE" == "docker" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        info "Docker Compose Services:"
        info "  Backend API:  http://localhost:5000"
        info "  Frontend:     http://localhost:3000"
        info "  PostgreSQL:   localhost:5432"
        echo ""
    fi
    
    if [[ "$DEPLOYMENT_TYPE" == "k8s" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        info "Kubernetes Services (use port-forward to access):"
        info "  kubectl port-forward -n $NAMESPACE svc/backend 5000:5000"
        info "  kubectl port-forward -n $NAMESPACE svc/frontend 3000:3000"
        echo ""
    fi
    
    success "Access information displayed"
    echo ""
}

################################################################################
# Help & Usage
################################################################################

show_help() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║   Blockchain-ML: Complete Deployment Script                   ║
╚════════════════════════════════════════════════════════════════╝

DESCRIPTION:
  Complete reset and deployment of blockchain-ml project.
  Cleans up all existing resources and creates fresh setup.

USAGE:
  ./complete-deployment.sh [OPTIONS]

OPTIONS:
  --skip-cleanup      Skip cleanup phase (reuse existing resources)
  --python-setup      Include Python virtual environment setup
  --docker-only       Deploy only Docker (skip Kubernetes)
  --k8s-only         Deploy only Kubernetes (skip Docker)
  --help             Show this help message

EXAMPLES:
  # Full deployment with cleanup
  ./complete-deployment.sh

  # Deploy to Docker only
  ./complete-deployment.sh --docker-only

  # Include Python environment setup
  ./complete-deployment.sh --python-setup

  # Full deployment without cleanup (reuse existing)
  ./complete-deployment.sh --skip-cleanup

REQUIREMENTS:
  - Docker & Docker Compose
  - kubectl & Kind (for Kubernetes)
  - Python 3.8+ (if using --python-setup)

OUTPUT:
  - Logs saved to: deployment-YYYYMMDD_HHMMSS.log

CLEANUP:
  To manually cleanup:
    docker-compose down -v         # Docker cleanup
    kind delete cluster --name blockchain-ml  # K8s cleanup
EOF
}

################################################################################
# Main Execution Flow
################################################################################

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-cleanup)
                SKIP_CLEANUP=true
                shift
                ;;
            --python-setup)
                PYTHON_SETUP=true
                shift
                ;;
            --docker-only)
                DEPLOYMENT_TYPE="docker"
                shift
                ;;
            --k8s-only)
                DEPLOYMENT_TYPE="k8s"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

main() {
    separator
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Blockchain-ML: Complete Deployment Reset & Setup Script    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
    separator
    echo ""
    
    log "Deployment started at $(date)"
    log "Log file: $LOG_FILE"
    log "Project root: $PROJECT_ROOT"
    echo ""
    
    # Parse arguments
    parse_arguments "$@"
    
    # Show configuration
    info "Configuration:"
    info "  Deployment Type: $DEPLOYMENT_TYPE"
    info "  Skip Cleanup: $SKIP_CLEANUP"
    info "  Python Setup: $PYTHON_SETUP"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Cleanup phase (unless skipped)
    if [ "$SKIP_CLEANUP" = false ]; then
        if [[ "$DEPLOYMENT_TYPE" == "docker" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
            cleanup_docker
        fi
        
        if [[ "$DEPLOYMENT_TYPE" == "k8s" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
            cleanup_kubernetes
        fi
    else
        warning "Skipping cleanup phase"
        echo ""
    fi
    
    # Python setup (optional)
    if [ "$PYTHON_SETUP" = true ]; then
        setup_python_environment
    fi
    
    # Docker setup (if included)
    if [[ "$DEPLOYMENT_TYPE" == "docker" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        setup_docker_environment
        build_docker_images
        deploy_docker_compose
    fi
    
    # Kubernetes setup (if included)
    if [[ "$DEPLOYMENT_TYPE" == "k8s" ]] || [[ "$DEPLOYMENT_TYPE" == "all" ]]; then
        setup_kubernetes_cluster
        load_docker_images_to_kind
        deploy_kubernetes_resources
        update_env_files_for_k8s
    fi
    
    # Verify deployment
    verify_deployment
    
    # Show access information
    show_access_info
    
    separator
    success "Deployment completed successfully!"
    log "Deployment finished at $(date)"
    echo ""
    info "Next steps:"
    info "  1. Update configuration files (.env, secrets, etc.)"
    info "  2. Verify services are running (see above)"
    info "  3. Access the dashboard at the URLs shown above"
    echo ""
}

# Run main function
main "$@"
