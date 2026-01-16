#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

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

docker build -f Dockerfile.backend -t blockchain-ml-backend:latest .
docker build -f Dockerfile.frontend -t blockchain-ml-frontend:latest ./src/frontend
docker build -f Dockerfile.worker -t blockchain-ml-worker:latest .
docker build -f Dockerfile.scheduler -t blockchain-ml-scheduler:latest .

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Images built${NC}\n"

# Load images into Kind cluster
echo -e "${BLUE}📥 Loading images into Kind cluster...${NC}\n"

kind load docker-image blockchain-ml-backend:latest --name $CLUSTER_NAME
kind load docker-image blockchain-ml-frontend:latest --name $CLUSTER_NAME
kind load docker-image blockchain-ml-worker:latest --name $CLUSTER_NAME
kind load docker-image blockchain-ml-scheduler:latest --name $CLUSTER_NAME

echo -e "${GREEN}✅ Images loaded${NC}\n"

# Create .env file if needed (for secrets)
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cat > .env << 'EOF'
POSTGRES_PASSWORD=change_me_to_secure_password
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
EOF
    echo -e "${GREEN}✅ .env created - please update with your values${NC}\n"
fi

# Update secrets with values from .env
echo -e "${BLUE}🔐 Updating Kubernetes secrets...${NC}"

# Source .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Update secrets YAML
sed -i "s|change-me-to-secure-password|${POSTGRES_PASSWORD:-change_me_to_secure_password}|g" k8s/03-secrets.yaml
sed -i "s|YOUR_KEY|${RPC_URL:-https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY}|g" k8s/02-configmap.yaml

echo -e "${GREEN}✅ Secrets updated${NC}\n"

# Deploy to Kubernetes
echo -e "${BLUE}🚀 Deploying to Kubernetes...${NC}\n"

kubectl apply -f k8s/01-namespace.yaml
kubectl apply -f k8s/02-configmap.yaml
kubectl apply -f k8s/03-secrets.yaml
kubectl apply -f k8s/04-storage.yaml
kubectl apply -f k8s/05-postgres-statefulset.yaml
kubectl apply -f k8s/06-backend-deployment.yaml
kubectl apply -f k8s/07-frontend-deployment.yaml
kubectl apply -f k8s/08-worker-deployment.yaml
kubectl apply -f k8s/09-scheduler-cronjob.yaml

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
