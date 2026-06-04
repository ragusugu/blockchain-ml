#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
K8S_DIR="$PROJECT_ROOT/k8s"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Kubernetes (Kind) Deployment        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

# Check if Kind is installed
if ! command -v kind &> /dev/null; then
    echo -e "${RED}❌ Kind is not installed${NC}"
    echo "Install from: https://kind.sigs.k8s.io/docs/user/quick-start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed${NC}"
    echo "Install from: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites found${NC}\n"

# Create Kind cluster if it doesn't exist
CLUSTER_NAME="blockchain-ml"

echo -e "${BLUE}📦 Checking Kind cluster...${NC}"
if kind get clusters | grep -q $CLUSTER_NAME; then
    echo -e "${GREEN}✅ Cluster '$CLUSTER_NAME' already exists${NC}\n"
else
    echo -e "${YELLOW}🔨 Creating Kind cluster '$CLUSTER_NAME'...${NC}\n"
    
    # Create Kind cluster with port mapping
    kind create cluster --name $CLUSTER_NAME --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  ports:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  - containerPort: 5000
    hostPort: 5000
    protocol: TCP
  - containerPort: 3000
    hostPort: 3000
    protocol: TCP
  - containerPort: 5432
    hostPort: 5432
    protocol: TCP
EOF
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to create cluster${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Cluster created${NC}\n"
fi

# Build Docker images
echo -e "${BLUE}🔨 Building Docker images for Kubernetes...${NC}\n"

docker build -f "$PROJECT_ROOT/docker/Dockerfile.backend" -t blockchain-ml-backend:latest "$PROJECT_ROOT"
docker build -f "$PROJECT_ROOT/docker/Dockerfile.frontend" -t blockchain-ml-frontend:latest "$PROJECT_ROOT"
docker build -f "$PROJECT_ROOT/docker/Dockerfile.worker" -t blockchain-ml-worker:latest "$PROJECT_ROOT"
docker build -f "$PROJECT_ROOT/docker/Dockerfile.scheduler" -t blockchain-ml-scheduler:latest "$PROJECT_ROOT"

echo -e "${GREEN}✅ Images built${NC}\n"

# Load images into Kind cluster
echo -e "${BLUE}📥 Loading images into Kind cluster...${NC}\n"

kind load docker-image blockchain-ml-backend:latest --name $CLUSTER_NAME
kind load docker-image blockchain-ml-frontend:latest --name $CLUSTER_NAME
kind load docker-image blockchain-ml-worker:latest --name $CLUSTER_NAME
kind load docker-image blockchain-ml-scheduler:latest --name $CLUSTER_NAME

echo -e "${GREEN}✅ Images loaded${NC}\n"

# Create .env file if needed (for secrets)
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cat > "$PROJECT_ROOT/.env" << 'EOF'
POSTGRES_PASSWORD=change_me_to_secure_password
POSTGRES_DB=blockchain_db
POSTGRES_USER=blockchain_user
RPC_URL=https://ethereum.publicnode.com
BATCH_SIZE=10
ETL_SCHEDULE_HOUR=0
ETL_SCHEDULE_MINUTE=0
EOF
    echo -e "${GREEN}✅ .env created - please update with your values${NC}\n"
fi

# Source .env without mutating tracked Kubernetes manifests
if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$PROJECT_ROOT/.env"
    set +a
fi

# Deploy to Kubernetes
echo -e "${BLUE}🚀 Deploying to Kubernetes...${NC}\n"

POSTGRES_DB="${POSTGRES_DB:-blockchain_db}"
POSTGRES_USER="${POSTGRES_USER:-blockchain_user}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-change_me_to_secure_password}"
RPC_URL="${RPC_URL:-https://ethereum.publicnode.com}"
BATCH_SIZE="${BATCH_SIZE:-10}"
ETL_SCHEDULE_HOUR="${ETL_SCHEDULE_HOUR:-0}"
ETL_SCHEDULE_MINUTE="${ETL_SCHEDULE_MINUTE:-0}"
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}"

kubectl apply -f "$K8S_DIR/01-namespace.yaml"

echo -e "${BLUE}🔐 Applying generated ConfigMap and Secret...${NC}"
kubectl -n blockchain-ml create configmap blockchain-config \
    --from-literal=RPC_URL="$RPC_URL" \
    --from-literal=BATCH_SIZE="$BATCH_SIZE" \
    --from-literal=ETL_SCHEDULE_HOUR="$ETL_SCHEDULE_HOUR" \
    --from-literal=ETL_SCHEDULE_MINUTE="$ETL_SCHEDULE_MINUTE" \
    --from-literal=FLASK_ENV=production \
    --from-literal=NODE_ENV=production \
    --from-literal=REACT_APP_API_URL=http://backend:5000 \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl -n blockchain-ml create secret generic db-credentials \
    --from-literal=POSTGRES_USER="$POSTGRES_USER" \
    --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    --from-literal=DATABASE_URL="$DATABASE_URL" \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl apply -f "$K8S_DIR/04-storage.yaml"
kubectl apply -f "$K8S_DIR/05-postgres-statefulset.yaml"
kubectl apply -f "$K8S_DIR/06-backend-deployment.yaml"
kubectl apply -f "$K8S_DIR/07-frontend-deployment.yaml"
kubectl apply -f "$K8S_DIR/08-worker-deployment.yaml"
kubectl apply -f "$K8S_DIR/09-scheduler-cronjob.yaml"
kubectl apply -f "$K8S_DIR/10-ingress.yaml"

kubectl -n blockchain-ml patch cronjob etl-scheduler --type merge \
    -p "{\"spec\":{\"schedule\":\"${ETL_SCHEDULE_MINUTE} ${ETL_SCHEDULE_HOUR} * * *\"}}"

echo -e "${GREEN}✅ Kubernetes manifests applied${NC}\n"

# Wait for deployments
echo -e "${YELLOW}⏳ Waiting for deployments to be ready...${NC}"
sleep 15

echo -e "${BLUE}📋 Deployment Status:${NC}\n"
kubectl get all -n blockchain-ml

echo -e "\n${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Kubernetes Deployment Complete!     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}\n"

echo -e "${BLUE}🌐 Access the application:${NC}"
echo -e "   Frontend: ${BLUE}http://localhost:3000${NC}"
echo -e "   Backend:  ${BLUE}http://localhost:5000${NC}\n"

echo -e "${BLUE}📊 View logs:${NC}"
echo -e "   Backend:  ${YELLOW}kubectl logs -n blockchain-ml -f deployment/backend${NC}"
echo -e "   Frontend: ${YELLOW}kubectl logs -n blockchain-ml -f deployment/frontend${NC}"
echo -e "   Worker:   ${YELLOW}kubectl logs -n blockchain-ml -f deployment/ml-worker${NC}\n"

echo -e "${BLUE}🔄 Watch pods:${NC}"
echo -e "   ${YELLOW}kubectl get pods -n blockchain-ml -w${NC}\n"

echo -e "${BLUE}🛑 To delete cluster:${NC}"
echo -e "   ${YELLOW}kind delete cluster --name blockchain-ml${NC}\n"
