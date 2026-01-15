# 🧪 Testing Guide - Blockchain Fraud Detection Dashboard

## Quick Test Checklist

Before running the full dashboard, verify each component works independently.

---

## ✅ Pre-Test Setup

### 1. Install Dependencies
```bash
cd /home/sugangokul/Desktop/blockchain-ml
pip install flask flask-cors
```

### 2. Verify File Structure
```bash
# Check all files exist
ls -la src/ai_dashboard.py
ls -la src/templates/index.html
ls -la src/static/style.css
ls -la src/static/script.js
```

### 3. Check Model
```bash
# Verify AI model exists
ls -la ai_model.pkl

# Or train if missing:
python src/train_ai_model.py
```

---

## 🔬 Component Tests

### Test 1: Backend Initialization

**File**: `src/ai_dashboard.py`  
**Duration**: ~5 seconds

```bash
cd /home/sugangokul/Desktop/blockchain-ml
python3 -c "
from src.ai_dashboard import initialize
import logging
logging.basicConfig(level=logging.INFO)
success = initialize()
if success:
    print('✅ Backend initialized successfully')
else:
    print('❌ Backend initialization failed')
"
```

**Expected Output:**
```
✅ Dashboard initialized
✅ Backend initialized successfully
```

---

### Test 2: Web3 Connection

**File**: `src/ai_dashboard.py`  
**Duration**: ~3 seconds

```bash
python3 -c "
from web3 import Web3
rpc = 'https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu'
w3 = Web3(Web3.HTTPProvider(rpc))
if w3.is_connected():
    print('✅ Web3 connected to Ethereum')
    print(f'  Latest block: {w3.eth.block_number}')
    print(f'  Gas price: {w3.eth.gas_price / 1e9:.2f} Gwei')
else:
    print('❌ Web3 connection failed')
"
```

**Expected Output:**
```
✅ Web3 connected to Ethereum
  Latest block: 18000000
  Gas price: 35.50 Gwei
```

---

### Test 3: AI Model Loading

**File**: `src/ai_fraud_detector.py`  
**Duration**: ~2 seconds

```bash
python3 -c "
import pickle
try:
    with open('ai_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print('✅ AI model loaded successfully')
    print(f'  Model type: {type(model).__name__}')
except Exception as e:
    print(f'❌ Failed to load AI model: {e}')
"
```

**Expected Output:**
```
✅ AI model loaded successfully
  Model type: RandomForestClassifier
```

---

### Test 4: HTML Template

**File**: `src/templates/index.html`  
**Duration**: ~1 second

```bash
python3 -c "
import os
html_file = 'src/templates/index.html'
if os.path.exists(html_file):
    with open(html_file, 'r') as f:
        content = f.read()
    if '<title>' in content and 'blockchain' in content.lower():
        print('✅ HTML template valid')
        print(f'  File size: {len(content)} bytes')
        print(f'  Has CSS link: {\"stylesheet\" in content}')
        print(f'  Has JS script: {\"script.js\" in content}')
    else:
        print('❌ HTML template invalid')
else:
    print('❌ HTML template not found')
"
```

**Expected Output:**
```
✅ HTML template valid
  File size: 8234 bytes
  Has CSS link: True
  Has JS script: True
```

---

### Test 5: CSS Styling

**File**: `src/static/style.css`  
**Duration**: ~1 second

```bash
python3 -c "
import os
css_file = 'src/static/style.css'
if os.path.exists(css_file):
    with open(css_file, 'r') as f:
        content = f.read()
    lines = len(content.split('\n'))
    print('✅ CSS file valid')
    print(f'  File size: {len(content)} bytes')
    print(f'  Lines: {lines}')
    print(f'  Has animations: {\"@keyframes\" in content}')
    print(f'  Has colors: {\"color:\" in content}')
else:
    print('❌ CSS file not found')
"
```

**Expected Output:**
```
✅ CSS file valid
  File size: 18567 bytes
  Lines: 453
  Has animations: True
  Has colors: True
```

---

### Test 6: JavaScript Interactivity

**File**: `src/static/script.js`  
**Duration**: ~1 second

```bash
python3 -c "
import os
js_file = 'src/static/script.js'
if os.path.exists(js_file):
    with open(js_file, 'r') as f:
        content = f.read()
    print('✅ JavaScript file valid')
    print(f'  File size: {len(content)} bytes')
    print(f'  Functions: {content.count(\"function\") + content.count(\"async function\")}')
    print(f'  Event listeners: {content.count(\"addEventListener\")}')
    print(f'  Fetch calls: {content.count(\"fetch(\")}')
else:
    print('❌ JavaScript file not found')
"
```

**Expected Output:**
```
✅ JavaScript file valid
  File size: 12345 bytes
  Functions: 15
  Event listeners: 5
  Fetch calls: 6
```

---

## 🌐 Live Server Tests

### Test 7: Start Flask Server

**Duration**: ~10 seconds

```bash
# Terminal 1: Start the server
cd /home/sugangokul/Desktop/blockchain-ml
python3 src/ai_dashboard.py

# Wait for output:
# ✅ Dashboard initialized
# WARNING: This is a development server...
# Running on http://127.0.0.1:5000
```

**Expected Output:**
```
✅ Dashboard initialized
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Test 8: API Endpoints

**Terminal**: Open a new terminal window

```bash
# Test 1: Get Options
curl http://localhost:5000/api/options

# Test 2: Get Stats
curl http://localhost:5000/api/stats

# Test 3: Post Transaction (with jq for pretty print)
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"option": "1", "block_count": 1}' | jq .
```

**Expected Output (Get Options):**
```json
{
  "options": [
    {
      "id": 1,
      "name": "Real-Time Analysis",
      "description": "Processes after extraction",
      "processing_stage": "After Transform",
      "speed": "Fast",
      ...
    }
  ]
}
```

**Expected Output (Get Stats):**
```json
{
  "latest_block": 18000000,
  "gas_price": 35.5,
  "total_transactions": 0,
  "fraud_count": 0
}
```

---

### Test 9: Web UI Access

**Browser Test**

1. Open browser: `http://localhost:5000`
2. Verify you see:
   - ✅ Header with logo and status
   - ✅ 3 option cards on left
   - ✅ Center panel with option info
   - ✅ Right panel with legends
   - ✅ Animated elements on hover

3. Test interactivity:
   - ✅ Click option cards - they highlight
   - ✅ Click "Fetch & Analyze" - loading spinner appears
   - ✅ Wait ~5 seconds - transaction table populates
   - ✅ Click transaction row - modal appears
   - ✅ Press ESC - modal closes

---

### Test 10: Full User Flow

**Complete E2E Test** (~2 minutes)

```
Step 1: Load Dashboard
├─ ✓ Page loads in < 1 second
├─ ✓ Header displays correctly
├─ ✓ 3 option cards visible
└─ ✓ No console errors

Step 2: Select Option 1
├─ ✓ Card highlights in blue
├─ ✓ Center panel updates
└─ ✓ Option details show

Step 3: Set Parameters
├─ ✓ Enter "5" in block count field
├─ ✓ Click "Fetch & Analyze"
└─ ✓ Loading spinner appears

Step 4: View Results
├─ ✓ Spinner disappears after 3-5 seconds
├─ ✓ Transaction table populates
├─ ✓ Stats cards update
└─ ✓ Rows color-coded by fraud risk

Step 5: View Details
├─ ✓ Click first transaction
├─ ✓ Modal pops up smoothly
├─ ✓ All fields populated correctly
└─ ✓ Press ESC to close

Step 6: Switch Option
├─ ✓ Click Option 2
├─ ✓ Option 1 card no longer highlighted
├─ ✓ Center panel updates
└─ ✓ Click Fetch & Analyze again

Step 7: Compare Results
├─ ✓ New transaction data loads
├─ ✓ Table refreshes with new data
├─ ✓ Fraud scores may differ from Option 1
└─ ✓ Stats update accordingly

Step 8: Test Auto-Refresh
├─ ✓ Click "Auto Refresh" button
├─ ✓ Button text changes to "On"
├─ ✓ Table updates every 5 seconds
├─ ✓ Click again to turn off
└─ ✓ Auto-refresh stops
```

---

## 🐛 Debugging Checklist

### If Dashboard Won't Start

```bash
# 1. Check Python version
python3 --version  # Should be 3.8+

# 2. Check dependencies
pip list | grep -E "flask|web3|pandas|cors"

# 3. Check port
lsof -i :5000

# 4. Check file permissions
ls -la src/ai_dashboard.py
```

### If Web3 Won't Connect

```bash
# Test RPC endpoint directly
curl https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### If Frontend Won't Load

```bash
# Check for 404 errors in network tab (F12 → Network)
# Verify static files served:

curl http://localhost:5000/static/style.css
curl http://localhost:5000/static/script.js

# Check browser console (F12 → Console) for JS errors
```

### If Transactions Don't Show

```bash
# Check API response
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"option": "1", "block_count": 1}' | jq .

# Check Flask logs for errors
# (visible in terminal running Flask)
```

---

## 📊 Performance Benchmarks

Expected performance metrics:

| Component | Target | Acceptable | Warning |
|-----------|--------|-----------|---------|
| Page Load | < 1s | < 2s | > 3s |
| Option Click | Instant | < 100ms | > 500ms |
| Fetch 5 Blocks | 3-5s | 2-8s | > 10s |
| Modal Open | Instant | < 200ms | > 500ms |
| Auto-Refresh | 5s | 4-6s | > 8s |
| CSS Load | < 500ms | < 1s | > 2s |
| JS Load | < 500ms | < 1s | > 2s |

---

## ✨ Visual Regression Tests

Manually verify visual appearance:

- [ ] Header gradient displays correctly
- [ ] Option cards have shadow/glow effects
- [ ] Hover effects work smoothly
- [ ] Color scheme is consistent
- [ ] Loading spinner rotates smoothly
- [ ] Modal appears centered
- [ ] Fraud risk colors are distinct:
  - [ ] Green (LOW)
  - [ ] Yellow (MEDIUM)
  - [ ] Orange (HIGH)
  - [ ] Red (CRITICAL)
- [ ] Tables have alternating row colors
- [ ] Scrollbars are styled

---

## 🎯 Test Results Template

```
TEST RUN: [Date/Time]
Tester: [Name]

PRE-TESTS:
[ ] Dependencies installed
[ ] Files verified
[ ] Model present
[ ] Port available

COMPONENT TESTS:
[ ] Backend initialization
[ ] Web3 connection
[ ] AI model loading
[ ] HTML template
[ ] CSS styling
[ ] JavaScript

LIVE SERVER TESTS:
[ ] Flask starts
[ ] API /options
[ ] API /stats
[ ] API /transactions (POST)
[ ] API /transaction/<hash> (GET)
[ ] Web UI loads

INTEGRATION TESTS:
[ ] Option selection
[ ] Fetch & Analyze
[ ] Results display
[ ] Modal details
[ ] Auto-refresh
[ ] Switch options
[ ] Multiple fetches

VISUAL TESTS:
[ ] Styling correct
[ ] Animations smooth
[ ] Colors distinct
[ ] Layout responsive

PERFORMANCE:
Page load time: _____ ms
Fetch time: _____ ms
Modal open time: _____ ms

ISSUES FOUND:
1. ______________________
2. ______________________
3. ______________________

STATUS: [ ] PASS [ ] FAIL
```

---

## 🚀 Final Verification

Before considering dashboard complete, verify:

```bash
✅ All tests pass
✅ No console errors (F12)
✅ No terminal errors
✅ Dashboard responsive on desktop/mobile
✅ API endpoints return valid JSON
✅ Transactions display correctly
✅ Fraud detection working
✅ Modal shows accurate data
✅ Auto-refresh functional
✅ Option switching works
```

---

**Ready to test? Start with:**

```bash
bash start_dashboard.sh
```

Then run tests from second terminal window.
