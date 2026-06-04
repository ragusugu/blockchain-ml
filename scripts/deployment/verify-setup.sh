#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

# Verification script to check if all Docker + K8s files are created

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   Verifying Docker + Kubernetes Setup                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

missing=0
found=0

# Check Dockerfiles
echo "📦 Checking Dockerfiles..."
for file in docker/Dockerfile.backend docker/Dockerfile.frontend docker/Dockerfile.worker docker/Dockerfile.scheduler; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
        ((found++))
    else
        echo "  ❌ $file"
        ((missing++))
    fi
done
echo ""

# Check docker-compose
echo "🐳 Checking Docker Compose..."
if [ -f "docker/docker-compose.yml" ]; then
    echo "  ✅ docker/docker-compose.yml"
    ((found++))
else
    echo "  ❌ docker-compose.yml"
    ((missing++))
fi
echo ""

# Check Kubernetes manifests
echo "⚙️  Checking Kubernetes Manifests..."
k8s_files=(
    "k8s/01-namespace.yaml"
    "k8s/02-configmap.yaml"
    "k8s/03-secrets.yaml"
    "k8s/04-storage.yaml"
    "k8s/05-postgres-statefulset.yaml"
    "k8s/06-backend-deployment.yaml"
    "k8s/07-frontend-deployment.yaml"
    "k8s/08-worker-deployment.yaml"
    "k8s/09-scheduler-cronjob.yaml"
    "k8s/10-ingress.yaml"
)

for file in "${k8s_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
        ((found++))
    else
        echo "  ❌ $file"
        ((missing++))
    fi
done
echo ""

# Check deployment scripts
echo "🚀 Checking Deployment Scripts..."
scripts=(
    "scripts/deployment/deploy.sh"
    "scripts/deployment/deploy-docker.sh"
    "scripts/deployment/deploy-kubernetes.sh"
    "scripts/deployment/cleanup-docker.sh"
    "scripts/deployment/cleanup-kubernetes.sh"
)

for file in "${scripts[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
        ((found++))
    else
        echo "  ❌ $file"
        ((missing++))
    fi
done
echo ""

# Check documentation
echo "📚 Checking Documentation..."
docs=(
    "documentation/guides/DEPLOYMENT_GUIDE.md"
    "docker/DOCKER_KUBERNETES_SETUP.md"
    "documentation/README.md"
    ".env.example"
)

for file in "${docs[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
        ((found++))
    else
        echo "  ❌ $file"
        ((missing++))
    fi
done
echo ""

# Summary
total=$((found + missing))
echo "╔════════════════════════════════════════════════════════╗"
echo "║            Verification Summary                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo "  ✅ Found:    $found files"
echo "  ❌ Missing:  $missing files"
echo "  📊 Total:    $total files"
echo ""

if [ $missing -eq 0 ]; then
    echo "🎉 All files verified! Setup is complete."
    echo ""
    echo "📖 Next steps:"
    echo "  1. Update .env file:  cp .env.example .env && nano .env"
    echo "  2. Deploy:            bash scripts/deployment/deploy.sh"
    echo "  3. View logs:         cd docker && docker-compose logs -f"
    echo ""
    exit 0
else
    echo "⚠️  Some files are missing! Check the list above."
    exit 1
fi
