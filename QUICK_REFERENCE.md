# ⚡ Quick Reference Card

## 🚀 Launch Dashboard

```bash
cd /home/sugangokul/Desktop/blockchain-ml
bash start_dashboard.sh
# Open: http://localhost:5000
```

---

## 📍 File Locations

| File | Purpose | Lines |
|------|---------|-------|
| `src/ai_dashboard.py` | Flask backend + APIs | 310 |
| `src/templates/index.html` | Web UI structure | 400 |
| `src/static/style.css` | Animations + styling | 450 |
| `src/static/script.js` | Interactivity | 300 |

---

## 🎯 3 Options Explained

| Option | Stage | Speed | Storage | Use Case |
|--------|-------|-------|---------|----------|
| **1** | After Extract | ⚡ Fast | ❌ None | Live monitoring |
| **2** | Before Load | ⚙️ Medium | ✅ PostgreSQL | Historical analysis |
| **3** | Parallel | 🐢 Slow | ✅ Database | Comprehensive audit |

---

## 🎨 Fraud Risk Colors

```
🟢 GREEN    = LOW       (< 25%)
🟡 YELLOW   = MEDIUM    (25-50%)
🟠 ORANGE   = HIGH      (50-75%)
🔴 RED      = CRITICAL  (> 75%)
```

---

## 🔌 API Endpoints

```bash
# Get all options
GET /api/options

# Fetch transactions
POST /api/transactions
Body: {"option": "1", "block_count": 10}

# Get transaction details
GET /api/transaction/<hash>

# Blockchain stats
GET /api/stats

# AI model info
GET /api/model-info
```

---

## 🖱️ User Interactions

```
CLICK OPTION CARD
  ↓ Selects option, shows details

ENTER BLOCK COUNT
  ↓ Set 1-100 blocks to analyze

CLICK "FETCH & ANALYZE"
  ↓ Shows loading spinner, fetches data

TRANSACTION TABLE LOADS
  ↓ Shows results with fraud colors

CLICK TRANSACTION ROW
  ↓ Opens detailed modal

CLICK "AUTO REFRESH" (Optional)
  ↓ Refreshes every 5 seconds
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| ESC | Close modal |
| Ctrl+C | Stop Flask server |

---

## 📊 Stats Cards Display

- **Total Transactions** - Sum of all TXs analyzed
- **Fraud Detected** - Count of fraudulent TXs
- **Average Value** - Mean ETH per transaction
- **Success Rate** - % of successful TXs

---

## 🧪 Quick Tests

```bash
# Test backend
python3 src/ai_dashboard.py &

# Test API
curl http://localhost:5000/api/options

# Test in browser
Open http://localhost:5000
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | `lsof -i :5000` then kill process |
| Missing dependencies | `pip install -r requirements.txt` |
| Web3 connection failed | Check RPC URL, internet connection |
| No transactions showing | Try fewer blocks (1-5 first) |
| API returns 404 | Verify Flask is running |
| CSS/JS not loading | Clear browser cache (Ctrl+Shift+Del) |

---

## 📱 Responsive Breakpoints

- **Desktop**: Full 3-panel layout
- **Tablet** (768-1200px): Center panel only
- **Mobile** (< 768px): Single column

---

## 🔑 Configuration

Environment variables (optional):

```bash
export RPC_URL="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
export DATABASE_URL="postgresql://user:pass@localhost/db"
```

---

## 📈 Expected Performance

| Metric | Target |
|--------|--------|
| Page load | < 1 second |
| Fetch (5 blocks) | 3-5 seconds |
| Modal open | Instant |
| Option switch | < 100ms |

---

## 💾 Requirements

```
Python 3.8+
Flask >= 2.0
Web3.py >= 6.0
pandas >= 1.0
scikit-learn >= 0.24
flask-cors
```

Install all:
```bash
pip install -r requirements.txt
```

---

## 🎓 Learning Path

1. **Start**: Read `DASHBOARD_README.md`
2. **Install**: Run `start_dashboard.sh`
3. **Test**: Follow `TESTING_GUIDE.md`
4. **Explore**: Try all 3 options
5. **Analyze**: View transaction details
6. **Monitor**: Enable auto-refresh

---

## 📁 Project Structure

```
blockchain-ml/
├── src/
│   ├── ai_dashboard.py          ← Main backend
│   ├── templates/
│   │   └── index.html           ← Frontend
│   └── static/
│       ├── style.css            ← Styling
│       └── script.js            ← Interactivity
├── DASHBOARD_README.md          ← Full guide
├── TESTING_GUIDE.md             ← Tests
├── COMPLETION_SUMMARY.md        ← Summary
└── start_dashboard.sh           ← Launcher
```

---

## 🎯 Common Tasks

### Change number of blocks
```
In UI: Enter value in "Blocks" field (1-100)
```

### View transaction details
```
Click any row in transactions table
→ Modal appears with 12+ fields
```

### Switch processing option
```
Click different option card (1, 2, or 3)
→ Center panel updates instantly
→ Click Fetch & Analyze again
```

### Enable continuous monitoring
```
Click "Auto Refresh" button
→ Updates every 5 seconds
→ Click again to disable
```

### Export transaction data
```
Right-click transactions table
→ Inspect (F12) → Copy HTML
→ Paste to Excel/Google Sheets
```

---

## 🔒 Security Notes

- ✅ CORS enabled for development
- ✅ Input validation on block count
- ✅ Error handling implemented
- ⚠️ No authentication (add in production)
- ⚠️ RPC key exposed (use env var in production)

---

## 📞 Getting Help

1. **Check Logs** - Terminal output when Flask runs
2. **Browser Console** - F12 → Console tab
3. **Network Tab** - F12 → Network to see API calls
4. **Testing Guide** - Complete debugging steps
5. **Documentation** - See README files

---

## ✅ Pre-Launch Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Port 5000 available
- [ ] Internet connection active
- [ ] AI model (ai_model.pkl) exists
- [ ] All 4 files created (dashboard.py, index.html, style.css, script.js)
- [ ] No terminal errors

---

## 🚀 Ready to Go!

```bash
cd /home/sugangokul/Desktop/blockchain-ml
bash start_dashboard.sh
# → http://localhost:5000
```

**Enjoy detecting blockchain fraud! 🔍**

---

*Reference Card v1.0 - Blockchain Fraud Detection Dashboard*
