#!/bin/bash
set -e

echo "🔨 Building backend image..."
cd /home/sugangokul/Desktop/blockchain-ml
docker build -f docker/Dockerfile.backend -t blockchain-ml-backend:latest . > /tmp/build.log 2>&1
if [ $? -eq 0 ]; then
  echo "✅ Backend built successfully"
else
  echo "❌ Build failed"
  tail -20 /tmp/build.log
  exit 1
fi

echo "📦 Loading into Kind cluster..."
kind load docker-image blockchain-ml-backend:latest --name blockchain-ml
echo "✅ Image loaded"

echo "🔄 Restarting backend pods..."
kubectl delete pods -n blockchain-ml -l app=backend
sleep 5

echo "⏳ Waiting for pods to be ready..."
kubectl rollout status deployment/backend -n blockchain-ml --timeout=60s

echo "✅ Deployment complete! Backend fix is now live."
echo ""
echo "Testing API..."
sleep 3
curl -s http://localhost:5000/api/health | jq .
