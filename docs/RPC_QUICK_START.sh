#!/bin/bash

# Open-Source RPC Quick Reference

cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║         🌐 OPEN-SOURCE RPC ENDPOINTS (NO KEYS REQUIRED)            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

🚀 QUICK START (Already Configured!)

   Your .env is already set to use:
   RPC_URL=https://eth.public-rpc.com
   
   ✅ No API key needed
   ✅ No signup required
   ✅ Ready to deploy now!

   bash scripts/deployment/deploy.sh

───────────────────────────────────────────────────────────────────────

🌐 FREE RPC OPTIONS (No Authentication)

   1. eth.public-rpc.com
      ✅ RECOMMENDED - Most reliable
      URL: https://eth.public-rpc.com

   2. ethereum.publicnode.com
      ✅ Good uptime
      URL: https://ethereum.publicnode.com

   3. rpc.ankr.com/eth
      ✅ Good performance
      URL: https://rpc.ankr.com/eth

───────────────────────────────────────────────────────────────────────

💳 FREEMIUM OPTIONS (Sign-up Required)

   4. Infura
      URL: https://mainnet.infura.io/v3/YOUR_INFURA_KEY
      Free tier: 100K requests/day
      Setup: https://infura.io/

   5. Alchemy
      URL: https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
      Free tier: 300M compute units/month
      Setup: https://www.alchemy.com/

   6. QuickNode
      URL: https://mainnet.quicknode.pro/YOUR_KEY/
      Free tier: 50 req/second
      Setup: https://www.quicknode.com/

───────────────────────────────────────────────────────────────────────

🔧 SWITCH RPC ENDPOINT

   Option 1: Edit .env
   ─────────────────
   nano .env
   # Change: RPC_URL=https://ethereum.publicnode.com

   Option 2: Edit Docker Compose
   ────────────────────────────
   nano docker-compose.yml
   # Change backend environment RPC_URL

   Option 3: Edit Kubernetes ConfigMap
   ───────────────────────────────────
   nano k8s/02-configmap.yaml
   # Change RPC_URL in data section
   kubectl apply -f k8s/02-configmap.yaml

───────────────────────────────────────────────────────────────────────

✅ TEST RPC CONNECTION

   # Test with curl
   curl -X POST https://eth.public-rpc.com \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

   # Test with Python
   python3 << 'PYTHON'
   from web3 import Web3
   w3 = Web3(Web3.HTTPProvider('https://eth.public-rpc.com'))
   if w3.is_connected():
       print(f'✅ Connected! Block: {w3.eth.block_number}')
   else:
       print('❌ Not connected')
   PYTHON

───────────────────────────────────────────────────────────────────────

📊 COMPARISON

   No Setup Required:
   ├─ eth.public-rpc.com (Recommended)
   ├─ ethereum.publicnode.com
   └─ rpc.ankr.com/eth

   Requires Signup (Free Tier):
   ├─ Infura (100K req/day)
   ├─ Alchemy (300M compute units/month)
   └─ QuickNode (50 req/second)

   Self-Hosted (Maximum Control):
   └─ geth --http

───────────────────────────────────────────────────────────────────────

🎯 DEPLOYMENT WITH RPC

   Docker Compose:
   bash scripts/deployment/deploy-docker.sh

   Kubernetes:
   bash scripts/deployment/deploy-kubernetes.sh

   Uses RPC from .env or docker-compose.yml automatically

───────────────────────────────────────────────────────────────────────

📖 FULL GUIDE: See OPEN_SOURCE_RPC_GUIDE.md

════════════════════════════════════════════════════════════════════════

EOF
