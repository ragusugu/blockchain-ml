# Visual Architecture & Flow Diagrams

## 🎯 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BLOCKCHAIN FRAUD DETECTION                       │
│                      DUAL PROCESSING SYSTEM                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   LANDING PAGE                                                       │
│  ┌────────────────────────────────────────────────────────┐         │
│  │                                                         │         │
│  │  App.jsx → Check processingMode                        │         │
│  │  └─ processingMode === null?                          │         │
│  │     YES: Show ModeSelector                            │         │
│  │     NO:  Show Dashboard                               │         │
│  │                                                         │         │
│  └────────────────────────────────────────────────────────┘         │
│                           ↓                                           │
│  ┌─────────────────────────────────────────────────────┐            │
│  │          MODE SELECTOR COMPONENT                     │            │
│  ├─────────────────────────────────────────────────────┤            │
│  │                                                       │            │
│  │  Header: "Choose Processing Mode"                   │            │
│  │                                                       │            │
│  │  ┌──────────────────┐  ┌──────────────────┐         │            │
│  │  │ ⏰ SCHEDULED      │  │ ⚡ REAL-TIME     │         │            │
│  │  │ Processing       │  │ Processing       │         │            │
│  │  ├──────────────────┤  ├──────────────────┤         │            │
│  │  │ • Batch jobs     │  │ • Stream input   │         │            │
│  │  │ • ML training    │  │ • Instant detect │         │            │
│  │  │ • Full storage   │  │ • Live updates   │         │            │
│  │  │ • Historic data  │  │ • Immediate store│         │            │
│  │  │                  │  │                  │         │            │
│  │  │ [Select Batch]   │  │ [Select Stream]  │         │            │
│  │  └──────────────────┘  └──────────────────┘         │            │
│  │                                                       │            │
│  │  Comparison Table (Below cards)                     │            │
│  │  ┌──────────────────────────────────────────┐       │            │
│  │  │ Aspect      │ Scheduled   │ Real-Time    │       │            │
│  │  │ Speed       │ Periodic    │ <100ms       │       │            │
│  │  │ Training    │ Yes         │ No           │       │            │
│  │  │ Storage     │ Full        │ Results      │       │            │
│  │  │ Use Case    │ Compliance  │ Monitoring   │       │            │
│  │  └──────────────────────────────────────────┘       │            │
│  │                                                       │            │
│  └─────────────────────────────────────────────────────┘            │
│                           ↓                                           │
│                    onSelectMode('scheduled'                          │
│                    or 'realtime')                                    │
│                           ↓                                           │
│  ┌─────────────────────────────────────────────────────┐            │
│  │            DASHBOARD (Mode-Specific)                │            │
│  ├─────────────────────────────────────────────────────┤            │
│  │                                                       │            │
│  │ [Mode Badge: ⏰ Scheduled] [Change Mode]           │            │
│  │                                                       │            │
│  │ LEFT PANEL            │ CENTER PANEL    │ RIGHT      │            │
│  │ ┌──────────────────┐  │ ┌─────────────┐ │ PANEL      │            │
│  │ │ Processing       │  │ │ Option Info │ │ ┌────────┐│            │
│  │ │ Options          │  │ │ ┌─────────┐ │ │ │ Model  ││            │
│  │ ├──────────────────┤  │ │ │ Option 1│ │ │ │ Info   ││            │
│  │ │ ○ Option 1       │  │ │ │ Details │ │ │ │ ┌────┐ ││            │
│  │ │ ○ Option 2       │  │ │ │ & Flow  │ │ │ │ │Acc:││            │
│  │ │                  │  │ │ └─────────┘ │ │ │ │94.5%││            │
│  │ │ Block Count: [10]│  │ │             │ │ │ │ROC:  ││            │
│  │ │ Auto-Refresh: ○  │  │ │ Statistics  │ │ │ │0.982 ││            │
│  │ │                  │  │ │ ┌─────────┐ │ │ │ └────┐ ││            │
│  │ │ [Fetch & Analyze]│  │ │ │Txs: 250 │ │ │ │Risk  ││            │
│  │ │                  │  │ │ │Fraud: 12│ │ │ │Legend││            │
│  │ │ Fraud Risk       │  │ │ │Success%:│ │ │ │┌────┐││            │
│  │ │ Legend           │  │ │ │ 95.2%   │ │ │ ││LOW  │││            │
│  │ │ ┌─────────────┐  │  │ │ └─────────┘ │ │ │└────┘││            │
│  │ │ │LOW   █      │  │  │ │             │ │ │HIGH   ││            │
│  │ │ │MEDIUM█      │  │  │ │ Transaction │ │ │CRITICAL││           │
│  │ │ │HIGH  █      │  │  │ │ Table       │ │ │        ││            │
│  │ │ │CRITICAL█    │  │  │ │ ┌─────────┐ │ │ └────────┘│            │
│  │ │ └─────────────┘  │  │ │ │Hash...  │ │ │          │            │
│  │ └──────────────────┘  │ │ │From...  │ │ │          │            │
│  │                       │ │ │Risk...  │ │ │          │            │
│  │                       │ │ │[View]   │ │ │          │            │
│  │                       │ │ └─────────┘ │ │          │            │
│  │                       │ └─────────────┘ │          │            │
│  │                       └─────────────────┘          │            │
│  └─────────────────────────────────────────────────────┘            │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND (Python + Flask)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  API ENDPOINTS                                                       │
│                                                                      │
│  GET /api/options?mode=scheduled|realtime                          │
│  ├─ Scheduled: [Standard Batch, Enhanced Batch + Anomaly]         │
│  └─ Real-Time: [Stream Detection, Risk Scoring]                   │
│                                                                      │
│  POST /api/transactions                                            │
│  {                                                                  │
│    "mode": "scheduled" | "realtime",                              │
│    "option": "1" | "2",                                           │
│    "block_count": 10                                              │
│  }                                                                  │
│                                                                      │
│  SCHEDULED PROCESSING FLOW:                                        │
│  ─────────────────────────                                         │
│  Request arrives                                                    │
│    ↓                                                                │
│  Extract N blocks via Web3                                         │
│    ↓                                                                │
│  Transform raw data                                                │
│    ↓                                                                │
│  Train ML Models (Random Forest + optionally Isolation Forest)    │
│    ↓                                                                │
│  Predict fraud scores                                              │
│    ↓                                                                │
│  Store in PostgreSQL (Full history + models)                      │
│    ↓                                                                │
│  Return statistics (training info included)                        │
│    ↓                                                                │
│  Response with full data                                           │
│                                                                      │
│  REAL-TIME PROCESSING FLOW:                                        │
│  ───────────────────────────                                       │
│  Request arrives                                                    │
│    ↓                                                                │
│  Stream recent transactions                                        │
│    ↓                                                                │
│  Transform each transaction                                        │
│    ↓                                                                │
│  Instant ML inference (pre-trained model)                         │
│    ↓                                                                │
│  Calculate fraud score (<100ms)                                    │
│    ↓                                                                │
│  Store results immediately to PostgreSQL                           │
│    ↓                                                                │
│  Return streaming statistics                                       │
│    ↓                                                                │
│  Response with real-time data                                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE (PostgreSQL)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SCHEDULED MODE STORAGE:                                           │
│  ┌─────────────────────────────────────────┐                       │
│  │ transaction_receipts                    │                       │
│  │ ├─ id (PK)                             │                       │
│  │ ├─ tx_hash (UNIQUE)                    │                       │
│  │ ├─ from_address                        │                       │
│  │ ├─ to_address                          │                       │
│  │ ├─ value_eth                           │                       │
│  │ ├─ fraud_score (ML result)             │                       │
│  │ ├─ is_fraud (0 or 1)                   │                       │
│  │ ├─ anomaly_score (if enhanced)         │                       │
│  │ └─ created_at                          │                       │
│  └─────────────────────────────────────────┘                       │
│                                                                      │
│  ┌─────────────────────────────────────────┐                       │
│  │ model_metadata                          │                       │
│  │ ├─ id (PK)                             │                       │
│  │ ├─ training_date                       │                       │
│  │ ├─ model_type (Random Forest)          │                       │
│  │ ├─ accuracy                            │                       │
│  │ ├─ features (JSON)                     │                       │
│  │ └─ version                             │                       │
│  └─────────────────────────────────────────┘                       │
│                                                                      │
│  REAL-TIME MODE STORAGE:                                           │
│  ┌─────────────────────────────────────────┐                       │
│  │ fraud_detections (Results only)         │                       │
│  │ ├─ id (PK)                             │                       │
│  │ ├─ tx_hash                             │                       │
│  │ ├─ risk_score                          │                       │
│  │ ├─ detection_timestamp                 │                       │
│  │ ├─ action_taken                        │                       │
│  │ └─ alert_level                         │                       │
│  └─────────────────────────────────────────┘                       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 State Management Flow

```
INITIAL STATE
──────────────
{
  processingMode: null,
  selectedOption: null,
  options: [],
  transactions: [],
  stats: null,
  loading: false,
  error: null
}
          │
          ↓
    User Opens App
          │
          ↓
  Is processingMode null?
    └─ YES → Show ModeSelector
    └─ NO → Show Dashboard
          │
          ↓
USER SELECTS MODE (e.g., 'scheduled')
──────────────────────────────────────
onSelectMode('scheduled')
{
  processingMode: 'scheduled',      ← NEW
  selectedOption: null,
  options: [...],                   ← LOADED
  transactions: [],
  stats: null,
  loading: false,
  error: null
}
          │
          ↓
API CALL: GET /api/options?mode=scheduled
          │
          ↓
OPTIONS LOADED
──────────────
{
  processingMode: 'scheduled',
  selectedOption: null,
  options: [
    {
      id: 1,
      name: 'Standard Batch Processing',
      ...
    },
    {
      id: 2,
      name: 'Enhanced Batch with Anomaly',
      ...
    }
  ],
  transactions: [],
  stats: null,
  loading: false,
  error: null
}
          │
          ↓
Dashboard renders with options
          │
          ↓
USER SELECTS OPTION & CONFIGURES (e.g., option 1, block_count 10)
───────────────────────────────────────────────────────────────────
onSelectOption(1) + onFetch()
{
  processingMode: 'scheduled',
  selectedOption: 1,                ← NEW
  options: [...],
  transactions: [],
  stats: null,
  loading: true,                    ← FETCHING
  error: null
}
          │
          ↓
API CALL: POST /api/transactions
{
  mode: 'scheduled',
  option: '1',
  block_count: 10
}
          │
          ↓
DATA LOADED & PROCESSED
──────────────────────
{
  processingMode: 'scheduled',
  selectedOption: 1,
  options: [...],
  transactions: [                   ← POPULATED
    { hash: '0x...', from: '0x...', fraud_score: 0.12, ... },
    { hash: '0x...', from: '0x...', fraud_score: 0.05, ... },
    ...
  ],
  stats: {                          ← POPULATED
    total_transactions: 250,
    fraud_count: 12,
    fraud_percentage: '4.8%',
    processing_type: 'Standard ML Training',
    ...
  },
  loading: false,                   ← DONE
  error: null
}
          │
          ↓
Dashboard displays results
          │
          ↓
USER CAN:
1. View transactions
2. Click for details
3. Change mode (reset to null)
4. Auto-refresh
5. Download results
```

---

## 🌊 Data Flow Comparison

### SCHEDULED MODE DATA FLOW

```
┌─────────────────────────────────────────────────────────────┐
│                    SCHEDULED PROCESSING                      │
└─────────────────────────────────────────────────────────────┘

Time: T0 (Start of batch window)
     ↓
  Extract Phase
  ─────────────
  ┌──────────────────────────────┐
  │ Fetch blocks from Ethereum   │
  │ Block range: 18,000,001-100  │ (100 blocks)
  │ Transactions collected: 2,500│
  │ Raw data size: ~50MB         │
  └──────────────────────────────┘
           ↓
         2-5 sec

  Transform Phase
  ───────────────
  ┌──────────────────────────────┐
  │ Clean transaction data       │
  │ Normalize addresses          │
  │ Calculate features:          │
  │ • tx_volume_1h               │
  │ • gas_price_zscore           │
  │ • address_age_days           │
  │ • value_deviation            │
  │ • ... (9 total features)     │
  │                              │
  │ Clean data: 2,450 txs        │
  │ (50 duplicates removed)      │
  └──────────────────────────────┘
           ↓
        10-20 sec

  Model Training Phase
  ────────────────────
  ┌──────────────────────────────┐
  │ Training Data: 2,450 txs     │
  │ Feature Matrix: 2450x9       │
  │                              │
  │ Train Models:                │
  │ • Random Forest (100 trees)  │
  │   Accuracy: 94.5%            │
  │   ROC-AUC: 0.982             │
  │                              │
  │ • Isolation Forest (if opt 2)│
  │   Contamination: 10%         │
  │   Anomalies found: 245       │
  │                              │
  │ Model saved: fraud_model.pkl │
  └──────────────────────────────┘
           ↓
       30-60 sec

  Prediction Phase
  ────────────────
  ┌──────────────────────────────┐
  │ Apply trained models         │
  │ Input: 2,450 txs × 9 features│
  │                              │
  │ Random Forest Predictions:   │
  │ • Fraud score: [0.0-1.0]     │
  │ • Threshold: 0.5             │
  │ • Flagged as fraud: 60 txs   │
  │                              │
  │ Isolation Forest Predictions:│
  │ • Anomaly scores             │
  │ • Additional flags: 45 txs   │
  │                              │
  │ Combined fraud detection:    │
  │ • Final fraud count: 85 txs  │
  └──────────────────────────────┘
           ↓
        10-15 sec

  Database Storage Phase
  ──────────────────────
  ┌──────────────────────────────┐
  │ INSERT 2,450 transactions    │
  │ WITH fraud_score, is_fraud   │
  │                              │
  │ SAVE model_metadata:         │
  │ • training_date              │
  │ • accuracy scores            │
  │ • feature names              │
  │ • model version              │
  │                              │
  │ Database size increases by:  │
  │ ~5MB per batch               │
  │ (grows over time)            │
  └──────────────────────────────┘
           ↓
        10-20 sec

Time: T0 + ~2 minutes (End of batch window)

TOTAL TIME: ~2 minutes per 100 blocks
STORAGE: Full history retained
DATABASE GROWS: ~5MB per batch execution
SCHEDULING: Run every hour/day/week

STATISTICS RETURNED:
├─ total_transactions: 2,450
├─ fraud_count: 85
├─ fraud_percentage: 3.5%
├─ processing_type: "Standard ML Training"
├─ model_accuracy: 94.5%
└─ training_timestamp: 2026-01-15 10:30:45 UTC
```

### REAL-TIME MODE DATA FLOW

```
┌─────────────────────────────────────────────────────────────┐
│                    REAL-TIME PROCESSING                      │
└─────────────────────────────────────────────────────────────┘

Time: T0 (Continuous)
     ↓
  Transaction Stream
  ──────────────────
  ┌──────────────────────────────┐
  │ Monitor Ethereum mempool     │
  │ New transaction arrives      │
  │ • Hash: 0x123...            │
  │ • From: 0xABC...            │
  │ • To: 0xDEF...              │
  │ • Value: 2.5 ETH            │
  │ • Gas: 45 gwei              │
  └──────────────────────────────┘
           ↓
      <10 milliseconds

  Transform Phase
  ───────────────
  ┌──────────────────────────────┐
  │ Clean single transaction     │
  │ Extract features (instantly):│
  │ • Query tx_volume_1h: 5 txs  │
  │ • Query avg_value_1h: 2.3 ET│
  │ • gas_price_zscore: +1.2     │
  │ • address_age_days: 365      │
  │ • ... (9 features total)     │
  │                              │
  │ Feature vector: [5, 2.3, ... │
  └──────────────────────────────┘
           ↓
      <20 milliseconds

  Inference Phase
  ───────────────
  ┌──────────────────────────────┐
  │ Load pre-trained model       │
  │ (Already loaded in memory)   │
  │                              │
  │ Apply Random Forest:         │
  │ Input: [5, 2.3, 1.2, ...]   │
  │ Output: fraud_score = 0.23   │
  │                              │
  │ Risk Assessment:             │
  │ 0.23 < 0.5 threshold         │
  │ Decision: LOW RISK (Normal)  │
  │                              │
  │ (If Risk Scoring option:     │
  │  Multi-factor analysis)      │
  └──────────────────────────────┘
           ↓
      <50 milliseconds

  Database Storage Phase
  ──────────────────────
  ┌──────────────────────────────┐
  │ INSERT 1 detection result    │
  │ • tx_hash: 0x123...          │
  │ • risk_score: 0.23           │
  │ • detection_timestamp: NOW   │
  │ • action: ALLOWED            │
  │ • alert_level: NONE          │
  │                              │
  │ Database size increases by:  │
  │ ~1KB per transaction         │
  │ (minimal growth)             │
  └──────────────────────────────┘
           ↓
      <50 milliseconds

  Dashboard Update
  ────────────────
  ┌──────────────────────────────┐
  │ WebSocket update to frontend │
  │ New detection: 0.23 risk     │
  │ Status: ✅ ALLOWED            │
  │                              │
  │ Live table updates           │
  │ Statistics refresh           │
  │ Alert checks (if configured) │
  └──────────────────────────────┘
           ↓
      <100 milliseconds

Time: T0 + 100ms - 200ms (Total latency)

REPEAT FOR EACH INCOMING TRANSACTION

TOTAL TIME: <200ms per transaction
STORAGE: Results only (~1KB per tx)
DATABASE GROWS: Minimal (~1KB per detection)
PROCESSING: Continuous/streaming

STATISTICS RETURNED (Accumulated):
├─ total_transactions: 47
├─ fraud_count: 1
├─ fraud_percentage: 2.1%
├─ average_risk_score: 0.18
├─ processing_type: "Real-Time Inference"
├─ latest_detection: 0.67 (flagged)
└─ timestamp: 2026-01-15 10:45:32 UTC
```

---

## 🎯 Option Selection Tree

```
USER SELECTS MODE
│
├─ ⏰ SCHEDULED MODE
│  │
│  └─ Option Selection
│     │
│     ├─ Option 1: Standard Batch
│     │  └─ Features:
│     │     • Process: Extract → Transform → Train RF → Predict → Store
│     │     • Models: Random Forest Classifier only
│     │     • Storage: Full transaction history + model metadata
│     │     • Training: Yes, every batch
│     │     • Time: ~2 min per 100 blocks
│     │     └─ Use: General compliance, standard fraud detection
│     │
│     └─ Option 2: Enhanced Batch + Anomaly
│        └─ Features:
│           • Process: Extract → Transform → Train RF+IF → Predict → Store
│           • Models: RF + Isolation Forest (dual learning)
│           • Storage: Full + anomaly scores
│           • Training: Yes, dual models each batch
│           • Time: ~3 min per 100 blocks
│           └─ Use: Unknown pattern detection, advanced analysis
│
└─ ⚡ REAL-TIME MODE
   │
   └─ Option Selection
      │
      ├─ Option 1: Stream Detection
      │  └─ Features:
      │     • Process: Stream → Transform → Inference → Store
      │     • Models: Pre-trained RF (no new training)
      │     • Storage: Detection results only
      │     • Training: No (uses existing model)
      │     • Time: <200ms per transaction
      │     └─ Use: Live monitoring, instant detection
      │
      └─ Option 2: Risk Scoring
         └─ Features:
            • Process: Stream → Multi-factor → Risk Score → Alert
            • Models: Pre-trained RF + risk factors
            • Storage: Scored results + alert flags
            • Training: No (uses existing model)
            • Time: <250ms per transaction
            └─ Use: Security operations, incident response
```

---

## 📊 Information Flow Summary

```
┌────────────────────────────────────────────────────┐
│  USER INTERACTION                                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  1. User Opens App → ModeSelector appears        │
│  2. User Clicks Mode → fetchOptionsForMode()      │
│  3. Dashboard loads with Options                  │
│  4. User Selects Option → handleSelectOption()    │
│  5. User Configures → Sets blockCount/refresh     │
│  6. User Clicks Fetch → fetchTransactions()       │
│  7. Results Display → Dashboard updates           │
│  8. User Views Details → DetailModal opens        │
│  9. User Changes Mode → handleBackToMode()        │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────┐
│  FRONTEND STATE UPDATES                            │
├────────────────────────────────────────────────────┤
│                                                    │
│  processingMode: null → 'scheduled'/'realtime'   │
│  options: [] → [Option1, Option2]                │
│  selectedOption: null → 1/2                      │
│  transactions: [] → [Tx1, Tx2, ...]              │
│  stats: null → {total, fraud, ...}               │
│  loading: false → true → false                   │
│  error: null → error message → null              │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────┐
│  COMPONENT RENDERS                                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  ModeSelector.jsx                                │
│    ├─ Shows when: processingMode === null        │
│    └─ Emits: onSelectMode()                      │
│                                                    │
│  App.jsx Dashboard                               │
│    ├─ Shows when: processingMode !== null        │
│    ├─ Components:                                │
│    │  ├─ OptionCard.jsx × 2                     │
│    │  ├─ StatCard.jsx × 4                       │
│    │  ├─ TransactionTable.jsx                   │
│    │  ├─ DetailModal.jsx                        │
│    │  └─ Header.jsx                             │
│    └─ Emits: onSelectOption(), onFetch()        │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────┐
│  API REQUESTS                                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  GET /api/options?mode=scheduled|realtime        │
│  Returns: [Option1, Option2]                     │
│                                                    │
│  POST /api/transactions {mode, option, count}    │
│  Returns: {transactions, stats, processing_info} │
│                                                    │
│  GET /api/transaction/{hash}                     │
│  Returns: {details}                              │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────┐
│  BACKEND PROCESSING                                │
├────────────────────────────────────────────────────┤
│                                                    │
│  SCHEDULED:                                      │
│  Extract → Transform → Train ML → Predict → DB  │
│  Time: ~2 minutes per batch                      │
│  Storage: Full history                           │
│                                                    │
│  REAL-TIME:                                      │
│  Extract → Transform → Inference → DB            │
│  Time: <200ms per transaction                    │
│  Storage: Results only                           │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────┐
│  DATABASE STORAGE                                  │
├────────────────────────────────────────────────────┤
│                                                    │
│  SCHEDULED: transaction_receipts + model_metadata │
│  REAL-TIME: fraud_detections table               │
│                                                    │
│  Both: Indexed by tx_hash for quick lookups      │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
┌────────────────────────────────────────────────────┐
│  RESPONSE TO FRONTEND                              │
├────────────────────────────────────────────────────┤
│                                                    │
│  Format: {                                        │
│    mode: 'scheduled'|'realtime',                 │
│    transactions: [...],                          │
│    stats: {...},                                 │
│    processing_info: '...'                        │
│  }                                               │
│                                                    │
└────────────────────────────────────────────────────┘
              ↓
            DISPLAY IN UI
```

This comprehensive visualization shows how every component, function, and data flow works together in the dual-mode system!

