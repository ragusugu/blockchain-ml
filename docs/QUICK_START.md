# 🚀 Quick Start Guide

## One-Command Startup

Choose one of these options to start everything automatically:

### **Option 1: Python Script (Recommended)**
```bash
python3 start_all.py
```
**Pros:**
- Cross-platform (Windows, Mac, Linux)
- Better error handling
- Auto-opens browser
- Colored output

### **Option 2: Bash Script**
```bash
bash start.sh
```
**Pros:**
- Lightweight
- Native shell script
- Fast execution

---

## What Gets Started Automatically

✅ **Backend (Flask)**
- Runs on `http://localhost:5000`
- REST API endpoints
- Fraud detection models
- Database connections

✅ **Frontend (React)**
- Runs on `http://localhost:3000`
- Interactive dashboard
- Real-time monitoring

✅ **Auto-Configuration**
- Installs npm dependencies (if needed)
- Sets environment variables
- Checks system requirements
- Opens browser automatically

---

## Prerequisites

Make sure you have:
- Python 3.7+
- Node.js 14+
- pip (Python package manager)
- npm (Node package manager)

Install Python dependencies:
```bash
pip install -r requirements.txt
```

---

## What Happens on Startup

1. **Checks Requirements** - Verifies Python, Node.js, npm, and Flask
2. **Sets Environment** - Configures RPC URL, database, polling intervals
3. **Installs Dependencies** - Runs `npm install` if needed
4. **Starts Backend** - Launches Flask on port 5000
5. **Starts Frontend** - Launches React on port 3000
6. **Opens Browser** - Automatically opens http://localhost:3000

---

## Manual Control

If you prefer manual startup:

### Start Backend Only
```bash
cd src/backend
python3 -m flask run --host=0.0.0.0 --port=5000
```

### Start Frontend Only
```bash
cd src/frontend
npm run dev
# or
npm start
```

---

## Troubleshooting

### "Port already in use"
```bash
# Kill process using port 5000 (backend)
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process using port 3000 (frontend)
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
cd src/frontend && npm install --legacy-peer-deps
```

### Backend not connecting to RPC
Check your `RPC_URL` environment variable:
```bash
echo $RPC_URL
# Should be: https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
```

### Frontend not loading
Check if you have node_modules:
```bash
cd src/frontend
npm install --legacy-peer-deps
npm run dev
```

---

## Environment Variables

Create `.env` file in project root:
```env
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
DATABASE_URL=postgresql://user:password@localhost:5432/blockchain_db
POLLING_INTERVAL=10
MAX_WORKERS=5
FLASK_ENV=development
```

---

## Stopping Services

Press `Ctrl+C` in the terminal where the script is running, or:

```bash
# Kill by port
pkill -f "flask run"
pkill -f "npm run dev"
```

---

## Next Steps

1. Navigate to `http://localhost:3000`
2. Select processing mode (Scheduled or Real-Time)
3. Choose an option
4. Click "Fetch & Analyze"
5. Monitor fraud detection live

Enjoy! 🎉
