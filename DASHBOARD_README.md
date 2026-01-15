# 🔗 Blockchain Fraud Detection Dashboard

An **interactive web dashboard** for detecting fraudulent Ethereum transactions using AI. Choose between 3 different processing strategies, switch between them in real-time, and analyze transaction details with an animated, intuitive interface.

---

## ✨ Features

### **3 Selectable AI Processing Options**

1. **Real-Time Analysis** (Option 1)
   - Processes transactions immediately after extraction
   - Fastest performance
   - Real-time fraud detection
   - Zero storage overhead

2. **Database-Integrated Analysis** (Option 2)
   - Filters and analyzes before storing in PostgreSQL
   - Balanced approach
   - Persistent data storage
   - Historical transaction tracking

3. **Parallel Processing** (Option 3)
   - Runs multiple AI models simultaneously
   - Most comprehensive analysis
   - Higher complexity
   - Best accuracy for complex patterns

### **Interactive Dashboard**

✅ **3-Panel Layout**
- Left: Option selector with pros/cons
- Center: Live transaction analysis
- Right: Detailed transaction info

✅ **Real-Time Features**
- Switch options anytime
- Instant results display
- Auto-refresh capability
- Live blockchain stats

✅ **Transaction Details**
- Comprehensive modal view
- 8+ data fields per transaction
- Fraud risk assessment
- Detailed AI scoring

✅ **Animated & Intuitive**
- Smooth card transitions
- Loading animations
- Hover effects
- Color-coded fraud levels

---

## 🚀 Quick Start

### **Prerequisites**
```bash
# Python 3.8+
# Flask
# Web3.py
# PostgreSQL (optional, for Option 2/3)
```

### **Installation**

1. **Install Dependencies**
```bash
cd /home/sugangokul/Desktop/blockchain-ml
pip install -r requirements.txt

# Additional if needed:
pip install flask flask-cors
```

2. **Verify Structure**
```
src/
├── ai_dashboard.py           # Flask backend
├── ai_fraud_detector.py      # AI model
├── ai_integration.py         # 3 option implementations
├── transform.py              # Data processing
├── templates/
│   └── index.html           # Web UI
└── static/
    ├── style.css            # Styling (400+ lines)
    └── script.js            # Interactivity (300+ lines)
```

### **Run the Dashboard**

```bash
# Start the Flask server
python src/ai_dashboard.py

# Server starts at:
# http://localhost:5000
```

Open your browser to **http://localhost:5000** and you should see:
- Header with Web3 status
- 3 option cards on the left
- Empty center panel (waiting for selection)
- Right panel with legends

---

## 📊 Usage Guide

### **Step 1: Select an Option**
```
Click any of the 3 option cards on the left panel
- See pros/cons instantly
- Details appear in center panel
```

### **Step 2: Configure & Fetch**
```
1. Enter number of blocks (1-100) in input field
2. Click "Fetch & Analyze" button
3. Wait for transactions to load
```

### **Step 3: View Results**
```
- Transaction table populates with data
- 8 columns: Block, From, To, Value, Gas, Status, Fraud Risk, Action
- Color-coded fraud levels: Green (Low) → Yellow (Medium) → Orange (High) → Red (Critical)
```

### **Step 4: View Details**
```
1. Click any transaction row or "View" button
2. Modal pops up with full details:
   - TX hash, block number, addresses
   - Value, gas usage, status
   - Fraud score and risk level
   - Timestamp and method
3. Click X or press ESC to close
```

### **Step 5: Switch & Compare**
```
1. Click a different option card
2. Center panel updates with new option info
3. Click "Fetch & Analyze" again
4. Compare results from different strategies
```

### **Optional: Auto-Refresh**
```
Click "⏳ Auto Refresh" button
- Refreshes every 5 seconds
- Click again to stop
- Useful for live monitoring
```

---

## 🎨 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│  🔗 Blockchain Fraud Detection    Connected • Block: 18M    │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌────────────────────────────────┐  ┌──────────────┐
│              │  │                                │  │              │
│  Option 1    │  │  Active Option Info            │  │  TX Details  │
│  [✓ selected]│  │                                │  │              │
│              │  │  📊 Stats Cards:               │  │  Hash: 0x... │
│  Option 2    │  │  • Total: 1,234 TXs          │  │  Block: 18M  │
│              │  │  • Fraud: 12 detected         │  │  From: 0x... │
│              │  │  • Avg: 0.5 ETH              │  │              │
│  Option 3    │  │  • Success: 98.5%            │  │  AI Model    │
│              │  │                                │  │  Acc: 94.5%  │
│              │  │  📋 Transactions Table:        │  │              │
│              │  │  [Block|From|To|Value|...]     │  │  Fraud Risk  │
│              │  │                                │  │  Legend:     │
│  ⚙️ Controls │  │  [Results populate here]      │  │  🟢 Low      │
│              │  │                                │  │  🟡 Medium   │
└──────────────┘  └────────────────────────────────┘  └──────────────┘
```

---

## 🔧 API Endpoints

The backend provides these REST API endpoints:

### **GET /api/options**
Returns all 3 options with details
```json
{
  "options": [
    {
      "id": 1,
      "name": "Real-Time Analysis",
      "description": "Processes after extraction",
      "processing_stage": "After Transform",
      "storage_type": "None",
      "speed": "Fast",
      "complexity": "Simple",
      "pros": ["Instant results", "No storage needed"],
      "cons": ["Cannot replay history"]
    },
    ...
  ]
}
```

### **POST /api/transactions**
Fetches and analyzes transactions with selected option
```json
{
  "option": "1",
  "block_count": 10
}
```

Response:
```json
{
  "transactions": [
    {
      "hash": "0x...",
      "block_number": 18000000,
      "from_address": "0x...",
      "to_address": "0x...",
      "value": "1.5",
      "gas_used": "21000",
      "status": "success",
      "fraud_risk": "LOW",
      "fraud_score": 0.05
    },
    ...
  ],
  "stats": {
    "total_transactions": 234,
    "fraud_count": 5,
    "average_value": 0.75,
    "success_rate": 0.985
  }
}
```

### **GET /api/transaction/<hash>**
Gets detailed info for a specific transaction

### **GET /api/stats**
Returns current blockchain statistics

### **GET /api/model-info**
Returns AI model metrics

---

## 🎯 Frontend Technologies

### **HTML5**
- Semantic structure
- 3-column responsive layout
- Modal for details
- Loading overlay
- Accessibility features

### **CSS3** (400+ lines)
- Modern gradient backgrounds
- Smooth animations and transitions
- Color-coded fraud levels
- Responsive grid layout
- Custom scrollbar styling
- Hover effects and interactions

### **JavaScript** (300+ lines)
- Async/await for API calls
- Event delegation
- DOM manipulation
- State management
- Error handling
- Toast notifications

---

## 🎓 How It Works

### **Option Selection Flow**
```
1. User clicks option card
2. selectOption(id) updates selected state
3. updateOptionInfo() fetches details from backend
4. UI highlights selected card
5. Center panel shows option details
```

### **Transaction Fetching Flow**
```
1. User clicks "Fetch & Analyze"
2. fetchTransactions() calls POST /api/transactions
3. Backend processes with selected option
4. Returns transactions + stats
5. populateTransactionsTable() renders results
6. updateStats() shows metrics
```

### **Details Display Flow**
```
1. User clicks transaction row
2. showTransactionDetails(hash) called
3. Fetches from GET /api/transaction/<hash>
4. updateRightPanel() shows summary
5. showModal() opens detailed view
```

---

## 📈 Performance

- **Load Time**: < 1s (initial page load)
- **Fetch & Analyze**: 2-5s (depends on block count)
- **Modal Open**: Instant animation
- **Auto-Refresh**: Every 5 seconds
- **Responsive**: Works on desktop, tablet, mobile

---

## 🐛 Troubleshooting

### **"Failed to load options"**
- Check if Flask server is running: `python src/ai_dashboard.py`
- Verify Web3 connection in terminal output
- Check browser console (F12) for errors

### **"Failed to fetch transactions"**
- Increase block count starting from 1-2 blocks
- Check Ethereum RPC connection
- Verify API endpoint is accessible: `http://localhost:5000/api/stats`

### **Empty transactions table**
- Try fetching fewer blocks
- Check if selected option has data
- Verify AI model is loaded correctly

### **Modal won't open**
- Check browser console for JavaScript errors
- Ensure transaction hash is valid
- Try closing and reopening

### **Auto-refresh not working**
- Check if "Fetch & Analyze" works first
- Verify browser allows auto-refresh
- Check console for timer errors

---

## 📝 Code Structure

### **Backend (ai_dashboard.py)**
```python
initialize()              # Setup Web3 + AI
@app.route('/')          # Serve dashboard
@app.route('/api/options')
@app.route('/api/transactions', methods=['POST'])
@app.route('/api/transaction/<tx_hash>')
@app.route('/api/stats')
@app.route('/api/model-info')
```

### **Frontend (index.html)**
```html
<header>           <!-- Logo, status, stats -->
<main .container>
  <aside .left>    <!-- 3 option cards -->
  <section .center> <!-- Option info, stats, table -->
  <aside .right>   <!-- TX details, legends -->
<modal>            <!-- Detailed TX view -->
<loading>          <!-- Spinner overlay -->
```

### **Styling (style.css)**
```css
:root { --colors }    /* Theme colors */
header {}             /* Sticky header */
.container {}         /* 3-column grid */
.option-card {}       /* Interactive cards */
.stats-grid {}        /* Stats display */
.transactions-table {}/* Data table */
.modal {}            /* Details popup */
@animations {}       /* Smooth transitions */
```

### **JavaScript (script.js)**
```js
loadOptions()         /* Load 3 options */
selectOption()        /* Handle selection */
fetchTransactions()   /* Get TX data */
populateTable()       /* Render results */
showTransactionDetails() /* Show modal */
toggleAutoRefresh()   /* Start/stop loop */
```

---

## 🔄 Data Flow

```
User Input (Option Selection)
    ↓
JavaScript Event Handler
    ↓
selectOption(id) Updates UI
    ↓
Backend: /api/options or /api/transactions
    ↓
Flask Routes Process Request
    ↓
AI Integration Applies Selected Strategy
    ↓
JSON Response
    ↓
JavaScript Updates DOM
    ↓
User Sees Live Results
```

---

## 🚀 Production Deployment

To deploy to production:

1. **Configure Flask**
```python
# ai_dashboard.py
app.run(host='0.0.0.0', port=5000, debug=False)
```

2. **Use Production Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.ai_dashboard:app
```

3. **Enable HTTPS**
```bash
# Use reverse proxy (nginx, Apache) with SSL
```

4. **Environment Variables**
```bash
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
DATABASE_URL=postgresql://...
```

---

## 📦 Requirements

See `requirements.txt`:
```
flask
flask-cors
web3
pandas
scikit-learn
```

---

## 💡 Tips & Tricks

1. **Start with Option 1** - Fastest and simplest
2. **Compare Options** - Use same block count to compare
3. **Monitor Live** - Enable auto-refresh for real-time data
4. **Check Details** - Click transactions to see full analysis
5. **Use Legend** - Refer to color codes in right panel

---

## 📞 Support

For issues or questions:
1. Check browser console (F12)
2. Review terminal output from Flask
3. Verify all files are in place
4. Ensure Port 5000 is available
5. Check network connectivity to Ethereum RPC

---

## ✅ Checklist

Before first run:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Port 5000 is free
- [ ] Internet connection (for Ethereum RPC)
- [ ] All files created:
  - [ ] src/ai_dashboard.py
  - [ ] src/templates/index.html
  - [ ] src/static/style.css
  - [ ] src/static/script.js
- [ ] AI model trained: `python src/train_ai_model.py`
- [ ] Test extraction works: Verify receipts/ folder has data

---

**🎉 Ready to detect fraud? Start the dashboard and explore the AI options!**

```bash
python src/ai_dashboard.py
# → Visit http://localhost:5000
```
