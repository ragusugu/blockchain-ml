# 🌐 Open-Source RPC Setup Guide

> Using **free, public RPC endpoints** for blockchain access (no API keys required)

---

## ⚡ Quick Start (30 seconds)

### The Easiest Option (No Setup Required)

```bash
# Copy .env template
cp .env.example .env

# That's it! It's already configured with eth.public-rpc.com
# No API keys needed, no signup required
```

**Default RPC**: `https://eth.public-rpc.com` ✅ Ready to use!

---

## 🔓 Free & Open-Source RPC Options

### 1. **Public RPC** ⭐ RECOMMENDED (No auth required)
```
URL: https://eth.public-rpc.com
✅ No API key needed
✅ No signup required
✅ Public endpoints maintained by community
✅ Reliable for testing & development
```

### 2. **Ethereum Public Node** (No auth required)
```
URL: https://ethereum.publicnode.com
✅ No API key needed
✅ No signup required
✅ Community-maintained
✅ Good uptime
```

### 3. **Ankr Public RPC** (No auth required)
```
URL: https://rpc.ankr.com/eth
✅ No API key needed
✅ No signup required
✅ Good performance
✅ Multiple blockchain support
```

### 4. **Geth Node (Self-hosted)** (Advanced)
```bash
# Run your own Ethereum node (requires 600GB+ disk)
geth --http --http.addr 0.0.0.0 --http.port 8545
URL: http://localhost:8545
✅ Complete control
✅ No rate limits
❌ High resource requirements
```

---

## 💳 Freemium Options (Sign-up Required)

### 5. **Infura** (Free tier available)
```
URL: https://mainnet.infura.io/v3/YOUR_INFURA_KEY
✅ Free tier: 100K requests/day
✅ High reliability
❌ Requires signup
```

**Setup:**
1. Visit: https://infura.io/
2. Sign up (free)
3. Create project → Get API key
4. Update `.env`: `RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY`

### 6. **Alchemy** (Free tier available)
```
URL: https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
✅ Free tier: 300M compute units/month
✅ Excellent performance
❌ Requires signup
```

**Setup:**
1. Visit: https://www.alchemy.com/
2. Sign up (free)
3. Create app → Get API key
4. Update `.env`: `RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY`

### 7. **QuickNode** (Free tier available)
```
URL: https://mainnet.quicknode.pro/YOUR_ENDPOINT_KEY/
✅ Free tier: 50 requests/second
✅ Good for production
❌ Requires signup
```

**Setup:**
1. Visit: https://www.quicknode.com/
2. Sign up (free)
3. Create endpoint → Get credentials
4. Update `.env`: `RPC_URL=https://mainnet.quicknode.pro/YOUR_KEY/`

### 8. **Moralis Web3 API** (Free tier available)
```
URL: https://mainnet.moralis.io/
✅ Free tier available
✅ Web3 features included
❌ Requires signup
```

---

## 📊 Comparison

| Provider | Auth | Setup | Rate Limit | Reliability | Cost |
|----------|------|-------|-----------|-------------|------|
| **Public RPC** | ❌ No | ⚡ 0 min | Variable | ⭐⭐⭐ | Free |
| **Ethereum Public Node** | ❌ No | ⚡ 0 min | Variable | ⭐⭐⭐ | Free |
| **Ankr** | ❌ No | ⚡ 0 min | Good | ⭐⭐⭐ | Free |
| **Infura** | ✅ Yes | 5 min | 100K/day | ⭐⭐⭐⭐⭐ | Free (tier) |
| **Alchemy** | ✅ Yes | 5 min | High | ⭐⭐⭐⭐⭐ | Free (tier) |
| **QuickNode** | ✅ Yes | 5 min | 50 req/s | ⭐⭐⭐⭐ | Free (tier) |
| **Self-hosted** | ❌ No | ⏱️ Hours | Unlimited | ⭐⭐⭐⭐ | Disk/CPU |

---

## 🚀 Configuration

### Option A: Use Default (Recommended for Quick Start)
```bash
# Already configured in .env.example with eth.public-rpc.com
cp .env.example .env
# No changes needed!
```

### Option B: Switch to Different RPC

**For Docker Compose:**
```bash
cp .env.example .env

# Edit .env
nano .env

# Change RPC_URL to your choice:
RPC_URL=https://ethereum.publicnode.com  # Or any option above
```

**For Kubernetes:**
```bash
# Edit the ConfigMap
nano k8s/02-configmap.yaml

# Update RPC_URL:
RPC_URL: "https://ethereum.publicnode.com"

# Apply changes
kubectl apply -f k8s/02-configmap.yaml
```

---

## 🔧 Testing Your RPC Connection

### Test with curl
```bash
# Test public RPC
curl -X POST https://eth.public-rpc.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

# Should return: {"jsonrpc":"2.0","result":"0x123456...","id":1}
```

### Test in Python
```python
from web3 import Web3

# Test your RPC connection
w3 = Web3(Web3.HTTPProvider('https://eth.public-rpc.com'))

# Check connection
if w3.is_connected():
    print(f"✅ Connected!")
    print(f"   Block: {w3.eth.block_number}")
    print(f"   Balance: {w3.eth.get_balance('0x...')}")
else:
    print("❌ Not connected")
```

### Test in Node.js
```javascript
const Web3 = require('web3');
const web3 = new Web3('https://eth.public-rpc.com');

web3.eth.getBlockNumber().then(blockNumber => {
    console.log('Current block number:', blockNumber);
}).catch(error => {
    console.error('Connection failed:', error);
});
```

---

## 📈 Choosing Based on Your Needs

### For Testing/Development
→ Use **eth.public-rpc.com** (no setup required)
```bash
RPC_URL=https://eth.public-rpc.com
```

### For Production with Low Volume
→ Use **Infura or Alchemy free tier** (reliable)
```bash
RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
```

### For High Volume Production
→ Use **QuickNode** or **self-hosted** (more resources)
```bash
RPC_URL=https://mainnet.quicknode.pro/YOUR_KEY/
```

### For Complete Control
→ **Self-host your node** (requires hardware)
```bash
# Run your own Ethereum node
geth --http
RPC_URL=http://localhost:8545
```

---

## ⚠️ Important Notes

### Rate Limits
- Public RPCs may have rate limits
- For high throughput, use paid/freemium tier
- Monitor your usage

### Reliability
- Public RPCs are community-maintained
- Consider using backup RPC endpoints
- Test before deploying to production

### Performance
- Different RPC providers have different speeds
- Test latency with your application
- Public RPCs may be slower than private ones

---

## 🔄 Fallback RPC Strategy (Advanced)

Update your code to handle RPC failures:

```python
# Fallback RPC endpoints
RPC_URLS = [
    'https://eth.public-rpc.com',
    'https://ethereum.publicnode.com',
    'https://rpc.ankr.com/eth',
]

from web3 import Web3

for rpc_url in RPC_URLS:
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            print(f"✅ Connected to {rpc_url}")
            break
    except:
        print(f"❌ Failed to connect to {rpc_url}")
        continue
```

---

## 🛠️ Troubleshooting

### "Connection Refused"
```bash
# Check if RPC URL is correct
curl https://eth.public-rpc.com

# Should return valid response
```

### "Rate Limited"
```bash
# Too many requests
# Solution: Use paid tier or self-host
```

### "RPC Server Error"
```bash
# RPC endpoint is down
# Solution: Switch to backup RPC
```

---

## 📚 More Resources

- **Chainlist**: https://chainlist.org/ (Find RPC endpoints)
- **Ethereum Nodes**: https://ethereum.org/en/developers/docs/nodes-and-clients/
- **Web3 Docs**: https://web3js.readthedocs.io/
- **Web3.py Docs**: https://web3py.readthedocs.io/

---

## 🚀 Get Started Now

### Quick Setup (30 seconds)
```bash
# Copy config
cp .env.example .env

# Deploy
docker-compose up -d
# or
bash scripts/deployment/deploy.sh
```

That's it! Your app is using the free public RPC endpoint! ✅

---

## 💡 Pro Tips

1. **Use multiple RPC endpoints** for redundancy
2. **Monitor RPC usage** to avoid rate limits
3. **Test RPC connection** before deploying
4. **Consider self-hosting** if you need unlimited access
5. **Use RPC backup strategies** for production

---

## 📝 Summary

| Task | Command |
|------|---------|
| Quick start (no setup) | `cp .env.example .env && docker-compose up -d` |
| Use different RPC | `nano .env && change RPC_URL` |
| Test RPC | `curl -X POST https://eth.public-rpc.com ...` |
| Deploy with K8s | `kubectl apply -f k8s/02-configmap.yaml` |
| Self-host node | `geth --http` |

---

**Default Setup**: Ready to use with `https://eth.public-rpc.com` ✅

No API keys. No signup. No configuration needed. Just works! 🚀
