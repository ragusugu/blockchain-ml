# Dual Processing Mode Implementation

## Overview
The blockchain fraud detection system now supports two distinct processing modes that users can select upfront:
1. **Scheduled (Batch) Processing** - Periodic processing with ML training
2. **Real-Time Processing** - Instant fraud detection with live updates

---

## 🏗️ Architecture Flow

### Initial Mode Selection
```
User Opens App
    ↓
ModeSelector Component
    ├─ ⏰ Scheduled Mode Card
    │   └─ Full details & benefits
    └─ ⚡ Real-Time Mode Card
        └─ Full details & benefits
    ↓
User Selects Mode
    ↓
Fetch Options for Selected Mode
    ↓
Dashboard UI Loads
```

---

## ⏰ SCHEDULED MODE (Batch Processing)

### Workflow
```
Extract Blocks
    ↓
Transform Data
    ↓
Train/Retrain ML Models
    ├─ Random Forest Classifier
    └─ Isolation Forest (Anomalies)
    ↓
Predict Fraud Scores
    ↓
Store Full History in PostgreSQL
    ├─ All transactions
    ├─ Fraud flags
    ├─ Fraud scores
    └─ Model metadata
    ↓
Display in Dashboard
```

### Available Options
1. **Standard Batch Processing**
   - Process blocks in configurable batches
   - Train ML models on accumulated data
   - Store complete history
   - Best for: Compliance, reporting, historical analysis

2. **Enhanced Batch with Anomaly Detection**
   - Dual learning approach
   - Random Forest + Isolation Forest
   - Catches both known and unknown patterns
   - Best for: Enterprise detection, pattern discovery

### Database Storage
- **All transactions** stored for historical analysis
- **Model metadata** saved for reproducibility
- **Fraud scores** for each transaction
- **Anomaly scores** for detected outliers

### Use Cases
- ✅ Compliance reporting
- ✅ Historical pattern analysis
- ✅ Regulatory audits
- ✅ Model retraining cycles
- ✅ Long-term trend analysis

---

## ⚡ REAL-TIME MODE (Stream Processing)

### Workflow
```
Transaction Stream (Web3)
    ↓
Real-Time Transform
    ↓
Load ML Model (Pre-trained)
    ↓
Instant Fraud Inference (<100ms)
    ↓
Store Results Immediately
    ├─ Fraud detection results
    ├─ Risk scores
    └─ Timestamp
    ↓
Display in Live Dashboard
    ↓
Optional: Send Alerts
```

### Available Options
1. **Real-Time Stream Detection**
   - Instant fraud detection as transactions occur
   - ML inference on each transaction
   - Immediate database storage
   - Best for: Active monitoring, threat detection

2. **Real-Time with Risk Scoring**
   - Multi-factor risk assessment
   - Custom alert thresholds
   - Priority scoring
   - Best for: Security operations, incident response

### Database Storage
- **Detection results** (not all historical data)
- **Risk scores** per transaction
- **Timestamp** and status
- **Alert triggers** and thresholds

### Use Cases
- ✅ Live fraud detection
- ✅ Real-time alerts
- ✅ Security monitoring
- ✅ Immediate threat response
- ✅ Dashboard live updates

---

## 🔄 Data Flow Comparison

### Scheduled Mode
```
Period (e.g., hourly)
    ↓
Extract N blocks
    ↓
Batch transform
    ↓
Train/Update models
    ↓
Predict on batch
    ↓
Store all results
    ↓
Report generated
```

**Pros:**
- ✅ Full historical data
- ✅ Model retraining
- ✅ Comprehensive analysis
- ✅ Lower costs
- ✅ Audit ready

**Cons:**
- ❌ Delay between events and detection
- ❌ Higher initial processing cost
- ❌ Database overhead

---

### Real-Time Mode
```
New Transaction
    ↓
Transform (< 10ms)
    ↓
Inference with loaded model (< 50ms)
    ↓
Store result (< 50ms)
    ↓
Display immediately (< 100ms)
```

**Pros:**
- ✅ Instant detection
- ✅ Live dashboard
- ✅ Immediate response
- ✅ No training overhead
- ✅ Lower latency

**Cons:**
- ❌ Uses pre-trained model (no retraining)
- ❌ Higher per-transaction cost
- ❌ Requires model availability

---

## 🎯 Key Implementation Details

### Frontend Changes (`App.jsx`)
```javascript
// New state
const [processingMode, setProcessingMode] = useState(null) // 'scheduled' or 'realtime'

// Initial UI: Mode selection
if (!processingMode) {
  return <ModeSelector onSelectMode={handleSelectMode} />
}

// Then: Dashboard with mode-specific options
```

### Backend Changes (`ai_dashboard.py`)

#### Fetch Options (Mode-aware)
```python
@app.route('/api/options', methods=['GET'])
def get_options():
    mode = request.args.get('mode')  # 'scheduled' or 'realtime'
    
    if mode == 'scheduled':
        return batch_options
    else:
        return realtime_options
```

#### Process Transactions (Mode-aware)
```python
@app.route('/api/transactions', methods=['POST'])
def get_transactions():
    mode = request.json.get('mode')  # 'scheduled' or 'realtime'
    option = request.json.get('option')  # Option within mode
    
    if mode == 'scheduled':
        # Train models, store full history
        enriched = train_and_predict(data)
    else:
        # Instant inference only
        enriched = instant_predict(data)
```

---

## 🔌 Database Considerations

### Scheduled Mode Storage
```sql
-- All transactions
CREATE TABLE transaction_receipts (
    id SERIAL PRIMARY KEY,
    tx_hash VARCHAR(66) UNIQUE,
    block_number BIGINT,
    fraud_score FLOAT,
    is_fraud BOOLEAN,
    created_at TIMESTAMP,
    ...
);

-- Model metadata
CREATE TABLE model_metadata (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(50),
    training_date TIMESTAMP,
    accuracy FLOAT,
    features JSON,
    ...
);
```

### Real-Time Mode Storage
```sql
-- Detection results only
CREATE TABLE fraud_detections (
    id SERIAL PRIMARY KEY,
    tx_hash VARCHAR(66),
    risk_score FLOAT,
    detection_timestamp TIMESTAMP,
    action_taken VARCHAR(50),
    ...
);
```

---

## 🚀 Usage Guide

### For Users

1. **Open Dashboard** → Mode Selection Screen
2. **Select Processing Mode:**
   - Choose ⏰ **Scheduled** for batch processing with training
   - Choose ⚡ **Real-Time** for instant detection
3. **Select Specific Option:**
   - Review option details
   - Choose appropriate approach for use case
4. **Configure & Process:**
   - Set block count
   - Enable auto-refresh if desired
   - Click "Fetch & Analyze"
5. **View Results:**
   - Dashboard shows mode-specific data
   - Statistics match processing approach
   - Option to change mode anytime

### For Developers

**Run in Scheduled Mode:**
```bash
cd src/backend && python3 api/ai_dashboard.py
# Select ⏰ Scheduled → Standard/Enhanced
# Process historical data with model training
```

**Run in Real-Time Mode:**
```bash
cd src/backend && python3 api/ai_dashboard.py
# Select ⚡ Real-Time → Stream/Risk-Scoring
# Stream live transactions with instant detection
```

---

## 📊 Statistics Returned

### Scheduled Mode Stats
- `total_transactions`: All processed
- `fraud_count`: Detected by trained model
- `fraud_percentage`: Percentage detected
- `average_value`: Average ETH value
- `total_eth_value`: Sum of values
- `success_rate`: Non-fraud percentage
- `processing_type`: "Standard ML Training" or "Dual ML Approach"

### Real-Time Mode Stats
- `total_transactions`: Streamed
- `fraud_count`: Real-time detections
- `fraud_percentage`: Detection rate
- `average_value`: Average ETH streamed
- `total_eth_value`: Total ETH streamed
- `success_rate`: Safety rate
- `processing_type`: "Real-Time Inference" or "Real-Time Risk Assessment"

---

## 🔄 Mode Switching

Users can switch modes anytime:
1. Click **"Change Mode"** button
2. Returns to Mode Selector
3. Select different mode
4. Options reload for new mode
5. Dashboard resets for new context

---

## 🎓 When to Use Each Mode

### Choose ⏰ Scheduled When:
- Need historical data retention
- Want regular ML model updates
- Building compliance reports
- Analyzing patterns over time
- Cost is primary concern
- Running periodic batch jobs

### Choose ⚡ Real-Time When:
- Need instant fraud detection
- Monitoring active accounts
- Want live dashboard updates
- Need immediate alerting
- Security is priority
- Can tolerate no historical data

---

## ✅ Validation & Checks

- Mode must be selected before options appear
- Options load based on mode selection
- Transactions sent with correct mode parameter
- Backend validates mode and option combination
- UI shows active mode at all times
- Users can easily switch modes

---

## 🔧 Troubleshooting

| Issue | Scheduled | Real-Time |
|-------|-----------|-----------|
| Model not training | Check logs | Not applicable |
| Database full | Clean old data | Results only |
| Slow processing | Reduce batch size | Increase parallelism |
| Memory usage | Lower batch size | Stream cleanup |
| Alerts not working | Check DB | Implement alerting |

---

## 📝 Future Enhancements

- [ ] Hybrid mode (scheduled training + realtime inference)
- [ ] Mode auto-switching based on load
- [ ] Custom alert rules per mode
- [ ] Data retention policies per mode
- [ ] Performance metrics dashboard per mode
- [ ] Multi-model ensemble per mode
- [ ] Model versioning and rollback
- [ ] Cost analysis per mode

