# 🔧 RPC Connection Fix Guide

## ❌ Problem
Web3 connection failed: RPC not connected

## ✅ Solution

Your system requires a working Ethereum RPC endpoint. Here are your options:

### **Option 1: Use Free Public RPC (Recommended)**

Add this to `/home/sugangokul/Desktop/blockchain-ml/docker/.env`:
```
RPC_URL=https://eth.drpc.org
```

Then restart:
```bash
cd /home/sugangokul/Desktop/blockchain-ml/docker
docker-compose restart backend
```

### **Option 2: Get Free Alchemy Key (Recommended - More Reliable)**

1. Go to: https://www.alchemy.com/
2. Sign up for free account
3. Create an Ethereum Mainnet app
4. Copy your API key
5. Update `.env`:
```
RPC_URL=https://eth-mainnet.alchemy.com/v2/YOUR_API_KEY
```

### **Option 3: Get Free Infura Key**

1. Go to: https://www.infura.io/
2. Sign up for free account
3. Create new project
4. Copy your project ID
5. Update `.env`:
```
RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

### **Option 4: Use Ankr with API Key (Free Tier)**

1. Go to: https://www.ankr.com/rpc/
2. Sign up for free
3. Create your API key
4. Update `.env`:
```
ANKR_RPC_URL=https://rpc.ankr.com/eth/YOUR_API_KEY
```

## 🚀 Apply Your Choice

**Step 1:** Edit the .env file:
```bash
nano /home/sugangokul/Desktop/blockchain-ml/docker/.env
```

**Step 2:** Update RPC_URL with your choice

**Step 3:** Save and restart:
```bash
cd /home/sugangokul/Desktop/blockchain-ml/docker
docker-compose restart backend
```

**Step 4:** Test the connection:
```bash
curl http://localhost:5000/api/stats
```

## ✅ Success Indicator

When working, you should see:
```json
{"transactions": [...], "stats": {...}}
```

Instead of:
```json
{"error":"Web3 not connected"}
```

---

**Recommended:** Use **Alchemy** for best reliability + free tier is generous.
