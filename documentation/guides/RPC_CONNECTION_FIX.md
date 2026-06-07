# RPC Connection Troubleshooting

## Problem

The backend reports `Web3 connection failed` or `RPC not connected`.

## Recommended Fix

Your system requires a working Ethereum RPC endpoint. Here are your options:

### Option 1: Use a Free Public RPC

Add this to `.env` or `docker/.env`:

```bash
RPC_URL=https://eth.drpc.org
```

Then restart:

```bash
cd docker
docker-compose restart backend
```

### Option 2: Use Alchemy

1. Go to: https://www.alchemy.com/
2. Sign up for a free account
3. Create an Ethereum Mainnet app
4. Copy your API key
5. Update `.env`:

```bash
RPC_URL=https://eth-mainnet.alchemy.com/v2/YOUR_API_KEY
```

### Option 3: Use Infura

1. Go to: https://www.infura.io/
2. Sign up for a free account
3. Create a new project
4. Copy your project ID
5. Update `.env`:

```bash
RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

### Option 4: Use Ankr

1. Go to: https://www.ankr.com/rpc/
2. Sign up for free
3. Create your API key
4. Update `.env`:

```bash
ANKR_RPC_URL=https://rpc.ankr.com/eth/YOUR_API_KEY
```

## Apply Your Choice

Edit the environment file:

```bash
nano docker/.env
```

Update `RPC_URL` or `ANKR_RPC_URL`, save, and restart:

```bash
cd docker
docker-compose restart backend
```

Test the connection:

```bash
curl http://localhost:5000/api/stats
```

## Success Indicator

When working, you should see:

```json
{"transactions": [...], "stats": {...}}
```

Instead of:

```json
{"error":"Web3 not connected"}
```

---

Do not commit private provider keys. Keep real RPC URLs in local environment files or deployment secrets.
