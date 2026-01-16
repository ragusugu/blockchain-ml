#!/bin/bash

# Delete Kind cluster
CLUSTER_NAME="blockchain-ml"

echo "🛑 Deleting Kubernetes cluster '$CLUSTER_NAME'..."
kind delete cluster --name $CLUSTER_NAME

echo "✅ Cleanup complete"
