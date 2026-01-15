# Quick Start: Dual Mode System

## 🚀 Get Started in 2 Minutes

### What Was Built?

Your app now has a **Mode Selection Screen** where users choose:
- **⏰ Scheduled Mode** - Batch processing with ML training
- **⚡ Real-Time Mode** - Instant fraud detection with live updates

---

## 📋 Steps to Run

### 1. Start the Backend
```bash
cd /home/sugangokul/Desktop/blockchain-ml
python src/ai_dashboard.py
```

Expected output:
```
✅ Dashboard initialized
🚀 Dashboard running on http://localhost:5000
```

### 2. Open in Browser
```
http://localhost:5000
```

### 3. You'll See This:
```
┌─────────────────────────────────────────────────┐
│   Blockchain Fraud Detection                    │
│   Choose your processing mode                   │
│                                                  │
│  [⏰ Scheduled Mode]  [⚡ Real-Time Mode]       │
│                                                  │
│  Select one to continue...                      │
└─────────────────────────────────────────────────┘
```

---

## 🎮 How to Use

### Choice 1: Scheduled Mode (Batch Processing)

**Click:** `⏰ Scheduled Processing`

```
You'll see:
├─ Option 1: Standard Batch Processing
│   └ "ML training on accumulated batches"
├─ Option 2: Enhanced Batch + Anomaly
│   └ "RF + Isolation Forest hybrid learning"
└─ [Configure] → [Fetch & Analyze]

Results:
├─ All historical transactions stored
├─ ML models trained on batch data
├─ Fraud scores calculated
└─ Full statistics generated
```

**Best for:** Compliance, reporting, historical analysis

### Choice 2: Real-Time Mode (Stream Processing)

**Click:** `⚡ Real-Time Processing`

```
You'll see:
├─ Option 1: Real-Time Stream Detection
│   └ "Instant inference as transactions arrive"
├─ Option 2: Real-Time with Risk Scoring
│   └ "Multi-factor analysis with alerts"
└─ [Configure] → [Fetch & Analyze]

Results:
├─ Instant fraud detection (<100ms)
├─ Live dashboard updates
├─ Results stored immediately
└─ Risk-based statistics
```

**Best for:** Live monitoring, threat detection, alerts

---

## 🎨 What Changed?

### Added
1. ✅ **ModeSelector.jsx** - Beautiful mode selection screen
2. ✅ **Updated App.jsx** - Mode state management
3. ✅ **Updated ai_dashboard.py** - Mode-aware API endpoints

### Features
- 🎨 Animated selection cards
- 📊 Mode comparison table
- 🔄 Easy mode switching
- 💡 Feature descriptions
- ✨ Professional UI

---

## 📊 Mode Comparison

| Aspect | Scheduled | Real-Time |
|--------|-----------|-----------|
| Speed | Periodic | Instant |
| Storage | Full history | Results only |
| Training | Yes, regular | No, inference only |
| Database | Large | Small |
| Use Case | Analysis | Monitoring |
| Latency | Minutes | <100ms |

---

## 🔄 User Journey

```
1. User Opens App
   ↓
2. Sees Mode Selector
   ├─ ⏰ Scheduled Mode Card
   └─ ⚡ Real-Time Mode Card
   ↓
3. Selects a Mode
   ↓
4. Dashboard Loads with Mode-Specific Options
   ├─ Option 1
   ├─ Option 2
   └─ Configuration Controls
   ↓
5. Selects Option & Configures
   ├─ Block count
   ├─ Auto-refresh
   └─ Other settings
   ↓
6. Clicks "Fetch & Analyze"
   ↓
7. Results Display
   ├─ Mode-appropriate statistics
   ├─ Transactions table
   └─ Detail modals
   ↓
8. Can Anytime Click "Change Mode"
   └─ Back to step 2
```

---

## 🎯 API Endpoints

### Get Mode-Specific Options
```bash
curl "http://localhost:5000/api/options?mode=scheduled"
curl "http://localhost:5000/api/options?mode=realtime"
```

### Process Transactions
```bash
curl -X POST "http://localhost:5000/api/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "scheduled",
    "option": "1",
    "block_count": 10
  }'
```

---

## 📝 Configuration Options

### Scheduled Mode Options

**Option 1: Standard Batch**
- Process: `Extract → Transform → Train ML → Predict → Store`
- Storage: Full transaction history
- Models: Random Forest only
- Best for: General compliance

**Option 2: Enhanced Batch + Anomaly**
- Process: `Extract → Transform → Train ML + Anomaly → Predict → Store`
- Storage: Full + anomaly scores
- Models: Random Forest + Isolation Forest
- Best for: Unknown fraud patterns

### Real-Time Mode Options

**Option 1: Stream Detection**
- Process: `Stream → Transform → Inference → Store`
- Storage: Detection results only
- Speed: <100ms per transaction
- Best for: Live monitoring

**Option 2: Risk Scoring**
- Process: `Stream → Multi-Factor → Risk Score → Alert → Store`
- Storage: Scored results
- Speed: <200ms per transaction
- Best for: Security operations

---

## ⚙️ Configuration

### Block Count
- **Scheduled**: Recommended 10-100 blocks
- **Real-Time**: 1-10 blocks per stream window
- Min: 1, Max: 100

### Auto-Refresh
- Toggle in dashboard settings
- Interval: 5 seconds
- Useful for: Live monitoring

### Database
- Existing PostgreSQL connection
- No schema changes needed
- Stores all results appropriately

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Mode selector not showing | Clear browser cache, refresh page |
| Options not loading | Check API is running (port 5000) |
| Transactions not fetching | Verify Web3 RPC connection |
| Stats not displaying | Check fraud detector model is loaded |
| Database errors | Verify PostgreSQL connection |
| Mode won't switch | Click "Change Mode" button |

---

## 🔗 Files Reference

**Frontend:**
- `src/frontend/src/components/ModeSelector.jsx` - Mode selection UI
- `src/frontend/src/App.jsx` - Mode state management

**Backend:**
- `src/ai_dashboard.py` - Mode-aware API endpoints

**Documentation:**
- `DUAL_MODE_IMPLEMENTATION.md` - Detailed guide
- `DUAL_MODE_SUMMARY.md` - Overview
- `CODE_STRUCTURE.md` - Technical details
- This file - Quick start

---

## 🎓 Example Workflows

### Compliance Report (Scheduled Mode)
```
1. Select ⏰ Scheduled Processing
2. Select "Standard Batch Processing"
3. Set blocks: 100
4. Click "Fetch & Analyze"
5. Get full transaction history with fraud scores
6. Export for audit/compliance
7. Archive in database
```

### Live Security Monitoring (Real-Time Mode)
```
1. Select ⚡ Real-Time Processing
2. Select "Real-Time with Risk Scoring"
3. Enable Auto-Refresh
4. Monitor dashboard live
5. Get instant alerts for high-risk transactions
6. Take immediate action
7. Review stored alerts later
```

---

## ✨ What Users See

### Mode Selector (First Screen)
```
┌─────────────────────────────────────────────┐
│ 🚀 Blockchain Fraud Detection              │
│                                              │
│ Choose your processing mode to get started  │
│                                              │
│ ┌──────────────────┐  ┌──────────────────┐  │
│ │ ⏰ SCHEDULED      │  │ ⚡ REAL-TIME     │  │
│ │ Batch Mode       │  │ Stream Mode      │  │
│ │                  │  │                  │  │
│ │ • Batch jobs     │  │ • Instant detect │  │
│ │ • ML training    │  │ • Live updates   │  │
│ │ • Full storage   │  │ • Stream process │  │
│ │ • Historic data  │  │ • Immediate act  │  │
│ │                  │  │                  │  │
│ │ [Select →]       │  │ [Select →]       │  │
│ └──────────────────┘  └──────────────────┘  │
│                                              │
│ 📊 Mode Comparison Table                    │
│ [Detailed comparison below]                 │
└─────────────────────────────────────────────┘
```

### Dashboard (After Mode Selection)
```
┌─────────────────────────────────────────────────┐
│ Mode: ⏰ Scheduled | [Change Mode]              │
├─────────────────────────────────────────────────┤
│                                                  │
│ [Option 1] [Option 2]                          │
│ [Block Count: 10] [Auto-refresh: OFF]          │
│ [Fetch & Analyze]                              │
│                                                  │
│ ┌─────────────────────────────────────────────┐ │
│ │ 📊 Statistics                               │ │
│ │ Total TX: 250 | Fraud: 12 | Success: 95.2% │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
│ [Transaction Table]                            │
│ ┌─────────────────────────────────────────────┐ │
│ │ Hash | From | To | Value | Risk | Details  │ │
│ │ 0x... | 0x... | 0x... | 2.5 | LOW | [View] │ │
│ │ 0x... | 0x... | 0x... | 1.2 | HIGH| [View] │ │
│ └─────────────────────────────────────────────┘ │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Next Steps

1. **Run the app** - Follow "Get Started" steps
2. **Select a mode** - Choose your use case
3. **Process data** - Analyze transactions
4. **View results** - Review statistics
5. **Switch modes** - Try the other approach
6. **Customize** - Add alerts, rules, exports

---

## 💡 Tips

- 🎯 Use **Scheduled** for compliance and reporting
- ⚡ Use **Real-Time** for active monitoring
- 🔄 Switch modes anytime with "Change Mode" button
- 📊 Check "Fraud Risk Legend" for color meanings
- 💾 Results automatically stored in database
- 📱 Works on mobile (responsive design)

---

## 🎉 You're All Set!

Your blockchain fraud detection system is now:
- ✅ User-friendly with mode selection
- ✅ Flexible with two processing approaches
- ✅ Professional with beautiful UI
- ✅ Powerful with dual ML strategies
- ✅ Ready for both compliance and monitoring

**Start the app and enjoy!** 🚀

