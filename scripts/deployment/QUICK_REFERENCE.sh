#!/bin/bash
# Quick Reference: Docker + Kubernetes Commands

echo "═══════════════════════════════════════════════════════════"
echo "  DOCKER + KUBERNETES QUICK REFERENCE"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Color codes
B='\033[1;34m'  # Blue
G='\033[1;32m'  # Green  
Y='\033[1;33m'  # Yellow
R='\033[1;31m'  # Red
N='\033[0m'     # Normal

echo -e "${B}DEPLOYMENT${N}"
echo "  docker-compose up -d                    # Start Docker Compose"
echo "  bash scripts/deployment/deploy.sh       # Interactive menu"
echo "  bash scripts/deployment/deploy-docker.sh # Docker setup"
echo "  bash scripts/deployment/deploy-kubernetes.sh # K8s setup"
echo ""

echo -e "${B}DOCKER COMPOSE STATUS${N}"
echo "  docker-compose ps                       # List containers"
echo "  docker-compose logs -f                  # View all logs"
echo "  docker-compose logs -f backend          # View backend logs"
echo "  docker-compose stats                    # Resource usage"
echo ""

echo -e "${B}DOCKER COMPOSE CONTROL${N}"
echo "  docker-compose up -d                    # Start all services"
echo "  docker-compose down                     # Stop services"
echo "  docker-compose down -v                  # Stop + remove volumes"
echo "  docker-compose restart                  # Restart all services"
echo "  docker-compose restart backend          # Restart one service"
echo ""

echo -e "${B}DOCKER COMPOSE SCALING${N}"
echo "  docker-compose up -d --scale backend=5 # Scale backend to 5"
echo "  docker-compose up -d --scale ml_worker=3 # Scale worker to 3"
echo ""

echo -e "${B}KUBERNETES STATUS${N}"
echo "  kubectl get pods -n blockchain-ml       # List pods"
echo "  kubectl get all -n blockchain-ml        # List all resources"
echo "  kubectl get events -n blockchain-ml     # View events"
echo "  kubectl describe pod <name> -n blockchain-ml # Pod details"
echo ""

echo -e "${B}KUBERNETES LOGS${N}"
echo "  kubectl logs -f deployment/backend -n blockchain-ml"
echo "  kubectl logs -f deployment/frontend -n blockchain-ml"
echo "  kubectl logs -f statefulset/postgres -n blockchain-ml"
echo ""

echo -e "${B}KUBERNETES CONTROL${N}"
echo "  kind create cluster --name blockchain-ml # Create cluster"
echo "  kind delete cluster --name blockchain-ml # Delete cluster"
echo "  kubectl apply -f k8s/                   # Deploy manifests"
echo "  kubectl delete -f k8s/                  # Delete all resources"
echo ""

echo -e "${B}KUBERNETES SCALING${N}"
echo "  kubectl scale deployment backend --replicas=5 -n blockchain-ml"
echo "  kubectl scale deployment frontend --replicas=3 -n blockchain-ml"
echo ""

echo -e "${B}KUBERNETES PORT FORWARD${N}"
echo "  kubectl port-forward svc/backend 5000:5000 -n blockchain-ml"
echo "  kubectl port-forward svc/frontend 3000:3000 -n blockchain-ml"
echo "  kubectl port-forward svc/postgres 5432:5432 -n blockchain-ml"
echo ""

echo -e "${B}KUBERNETES UPDATES${N}"
echo "  kubectl rollout restart deployment/backend -n blockchain-ml"
echo "  kubectl set image deployment/backend backend=blockchain-ml-backend:latest -n blockchain-ml"
echo "  kubectl rollout history deployment/backend -n blockchain-ml"
echo "  kubectl rollout undo deployment/backend -n blockchain-ml"
echo ""

echo -e "${B}DATABASE OPERATIONS${N}"
echo "  # Docker Compose"
echo "  docker exec blockchain-postgres psql -U blockchain_user blockchain_db"
echo "  docker exec -i blockchain-postgres psql -U blockchain_user blockchain_db < backup.sql"
echo ""
echo "  # Kubernetes"
echo "  kubectl exec -it postgres-0 -n blockchain-ml -- psql -U blockchain_user blockchain_db"
echo "  kubectl exec -i postgres-0 -n blockchain-ml -- psql -U blockchain_user blockchain_db < backup.sql"
echo ""

echo -e "${B}ACCESS APPLICATION${N}"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:5000"
echo "  Database:  localhost:5432"
echo ""

echo -e "${B}CONFIGURATION${N}"
echo "  cp .env.example .env                    # Create .env"
echo "  nano .env                               # Edit configuration"
echo "  kubectl apply -f k8s/03-secrets.yaml    # Update K8s secrets"
echo "  kubectl apply -f k8s/02-configmap.yaml  # Update K8s config"
echo ""

echo -e "${B}TROUBLESHOOTING${N}"
echo "  docker ps                               # Running containers"
echo "  docker logs <container>                 # Container logs"
echo "  docker inspect <container>              # Container details"
echo "  kubectl describe pod <pod> -n blockchain-ml"
echo "  kubectl events -n blockchain-ml         # K8s events"
echo "  lsof -i :5000                          # Find process on port"
echo ""

echo -e "${B}CLEANUP${N}"
echo "  docker-compose down -v                  # Remove all Docker"
echo "  kind delete cluster --name blockchain-ml # Remove K8s"
echo "  bash scripts/deployment/cleanup-docker.sh"
echo "  bash scripts/deployment/cleanup-kubernetes.sh"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "Documentation: See DEPLOYMENT_GUIDE.md for details"
echo "═══════════════════════════════════════════════════════════"
