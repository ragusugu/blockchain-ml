# 🏗️ Frontend & Backend Alignment Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ETHEREUM NETWORK                             │
└─────────────────────────────────────────────────────────────────┘
         │                                        │
         │ RPC_URL                    ANKR_RPC_URL (Free)
         ↓                                        ↓
    ┌─────────────┐                     ┌──────────────────┐
    │ Batch ETL   │                     │ Ankr Streamer    │
    │ Service     │                     │ Service          │
    │             │                     │                  │
    │ • Runs on   │                     │ • Continuous     │
    │   schedule  │                     │   polling        │
    │ • RPC calls │                     │ • Block tracking │
    │ • Rate      │                     │ • TX extraction  │
    │   limited   │                     │ • No rate limit  │
    └─────────────┘                     └──────────────────┘
         │                                        │
         └────────────────────┬───────────────────┘
                              ↓
                  ┌──────────────────────┐
                  │  PostgreSQL DB       │
                  │                      │
                  │ • transactions       │
                  │ • stats              │
                  │ • blocks_data        │
                  │ • fraud_flags        │
                  └──────────────────────┘
                              ↑
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
            ↓                                   ↓
    ┌───────────────────┐            ┌──────────────────┐
    │  Backend API      │            │ Streaming Stats  │
    │ (ai_dashboard.py) │            │ Cache            │
    │                   │            │                  │
    │ Endpoints:        │◄───────────┤ • Blocks streamed│
    │ • /api/trans...   │            │ • Transactions   │
    │ • /api/stats      │            │ • Errors         │
    │ • /api/streaming/ │            │ • Last update    │
    │   stats (NEW)     │            └──────────────────┘
    │ • /api/streaming/ │
    │   health (NEW)    │
    │ • /api/system/    │
    │   status (NEW)    │
    └───────────────────┘
            │
            │ HTTP REST
            │
            ↓
    ┌──────────────────────────┐
    │  React Frontend          │
    │  (App.jsx)               │
    │                          │
    │ ┌──────────────────────┐ │
    │ │ StreamingStatus      │ │ ← NEW
    │ │ Component            │ │
    │ │                      │ │
    │ │ Shows:               │ │
    │ │ • RPC status         │ │
    │ │ • Current block      │ │
    │ │ • Gas price          │ │
    │ │ • AI model status    │ │
    │ │ • Streaming running? │ │
    │ │ • Blocks streamed    │ │
    │ │ • Transactions/sec   │ │
    │ │ • Error count        │ │
    │ └──────────────────────┘ │
    │         ↑                │
    │         │                │
    │ ┌──────────────────────┐ │
    │ │ useStreamingData Hook │ │ ← NEW
    │ │                      │ │
    │ │ • Polls every 10s    │ │
    │ │ • Fetches stats      │ │
    │ │ • Error handling     │ │
    │ └──────────────────────┘ │
    │                          │
    └──────────────────────────┘
            │
            │ Browser Display
            │
            ↓
    ┌──────────────────────────┐
    │  User Dashboard          │
    │                          │
    │  ✅ Batch ETL Running    │
    │  ✅ Streaming Active     │
    │  📊 Real-time Metrics    │
    │  📈 Live Updates (10s)   │
    └──────────────────────────┘
```

---

## Data Flow Diagrams

### Scenario 1: Batch ETL Only

```
RPC_URL (Alchemy/Infura)
        ↓
    Batch ETL Job
    (Once per day)
        ↓
   PostgreSQL
        ↓
Backend API (/api/transactions)
        ↓
Frontend (Dashboard)
        ↓
StreamingStatus: ✅ Batch | ❌ Streaming
```

### Scenario 2: Ankr Streaming Only

```
ANKR_RPC_URL (Free)
        ↓
  Ankr Streamer
  (Continuous)
        ↓
   PostgreSQL
        ↓
Backend API (/api/system/status)
        ↓
Frontend (StreamingStatus)
        ↓
StreamingStatus: ⚪ Batch | ✅ Streaming
```

### Scenario 3: Both (Recommended)

```
RPC_URL              ANKR_RPC_URL
    ↓                    ↓
 Batch ETL ←─────────→ Ankr Streamer
    ↓                    ↓
    └────────┬───────────┘
             ↓
        PostgreSQL
         (Unified)
             ↓
      Backend API
    (3 new endpoints)
             ↓
      Frontend React
    (StreamingStatus)
             ↓
   User sees BOTH:
   ✅ Batch ETL Status
   ✅ Streaming Status
   📊 Combined Metrics
```

---

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (React)                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ App.jsx                                          │  │
│  │ ┌─────────────────────────────────────────────┐  │  │
│  │ │ Header Component                            │  │  │
│  │ │ (Mode Selection: Batch/Streaming/Both)      │  │  │
│  │ └─────────────────────────────────────────────┘  │  │
│  │ ┌─────────────────────────────────────────────┐  │  │
│  │ │ {processingMode &&                          │  │  │
│  │ │   <StreamingStatus />}  ← CONDITIONAL       │  │  │
│  │ │                                             │  │  │
│  │ │ Inside StreamingStatus:                     │  │  │
│  │ │ ┌───────────────────────────────────────┐   │  │  │
│  │ │ │ useStreamingData()  ← HOOK            │   │  │  │
│  │ │ │ • Fetch every 10s                     │   │  │  │
│  │ │ │ • GET /api/system/status              │   │  │  │
│  │ │ │ • GET /api/streaming/stats            │   │  │  │
│  │ │ │ • Return state                        │   │  │  │
│  │ │ └───────────────────────────────────────┘   │  │  │
│  │ │                                             │  │  │
│  │ │ ┌───────────────────────────────────────┐   │  │  │
│  │ │ │ Display Status                        │   │  │  │
│  │ │ │ • Batch: RPC, blocks, gas, AI        │   │  │  │
│  │ │ │ • Streaming: running, blocks, txs    │   │  │  │
│  │ │ │ • Colors: green=OK, red=error        │   │  │  │
│  │ │ └───────────────────────────────────────┘   │  │  │
│  │ └─────────────────────────────────────────────┘  │  │
│  │                                                 │  │  │
│  │ ┌─────────────────────────────────────────────┐  │  │
│  │ │ Dashboard Component                        │  │  │
│  │ │ (Existing - Unchanged)                     │  │  │
│  │ └─────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                        ↑                               │
└────────────────────────┼───────────────────────────────┘
                         │
                   HTTP GET Calls
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ↓               ↓               ↓
      /api/trans     /api/streaming   /api/system
     actions         /stats           /status
         │               │               │
         └───────────────┼───────────────┘
                         ↓
        ┌────────────────────────────────┐
        │  BACKEND (Flask)               │
        │  ai_dashboard.py               │
        │                                │
        │  ✅ /api/streaming/stats (NEW) │
        │  ✅ /api/streaming/health (NEW)│
        │  ✅ /api/system/status (NEW)   │
        │  ✅ /api/transactions          │
        │                                │
        │  • Query PostgreSQL            │
        │  • Check streaming stats       │
        │  • Return JSON                 │
        └────────────────────────────────┘
                    ↓
        ┌────────────────────────────────┐
        │  PostgreSQL Database           │
        │                                │
        │  Tables:                       │
        │  • transactions                │
        │  • stats                       │
        │  • blocks_data                 │
        │                                │
        │  Fed by:                       │
        │  • Batch ETL (schedule)        │
        │  • Ankr Streamer (realtime)    │
        └────────────────────────────────┘
```

---

## Request/Response Flow

### Flow 1: Frontend Requests System Status

```
Frontend
  ↓
useStreamingData() hook
  ↓
fetch('/api/system/status')
  ↓ HTTP GET
Backend
  ├─ Check HAS_STREAMING flag
  ├─ Get batch status from DB
  ├─ Get streaming stats (if available)
  └─ Combine response
  ↓ HTTP 200
  {
    services: {
      batch: { status, blocks, gas, ai },
      streaming: { status, blocks, txs, errors }
    }
  }
  ↓
Frontend receives JSON
  ↓
StreamingStatus renders data
  ↓
User sees: Both services status + metrics
```

### Flow 2: Streaming Stats Only

```
Frontend
  ↓
useStreamingData() hook
  ↓
fetch('/api/streaming/stats')
  ↓ HTTP GET
Backend
  ├─ Call get_streaming_stats()
  ├─ Return streaming metrics
  └─ If error: return empty/error
  ↓ HTTP 200
  {
    streaming_enabled: true,
    blocks_streamed: 2345,
    transactions_streamed: 456789,
    errors: 0,
    last_update: "2024-01-15T10:30:45"
  }
  ↓
Frontend receives JSON
  ↓
Update component state
  ↓
User sees: Live streaming metrics
```

---

## Polling Architecture

```
StreamingStatus Component (Render)
        │
        ├─► useStreamingData() Hook
        │
        ├─► useEffect() with interval
        │
        ├─► 10 second interval
        │
        └─► fetch('/api/system/status')
                    │
                    ├─► Response comes in
                    │
                    ├─► Update state
                    │
                    └─► Component re-renders
                              │
                              ├─► Show new metrics
                              │
                              ├─► Animate indicators
                              │
                              └─► Display timestamps
```

---

## Error Handling Architecture

```
Frontend
  ↓
Try fetch data
  ├─ Success → Display metrics
  ├─ Network error → Show "Error loading data"
  ├─ Parse error → Show "Invalid response"
  └─ Timeout → Show "Request timeout"
  ↓
Backend
  ├─ Streaming available → Return stats
  ├─ Streaming unavailable → Return empty
  ├─ DB error → Log error, return error response
  └─ Exception → Catch, return 500
  ↓
Frontend graceful degradation
  ├─ If streaming not available → Show "Not Available"
  ├─ If stats empty → Show "Waiting for data"
  ├─ If error → Show error message
  └─ Keep batch data visible (if available)
```

---

## State Management Flow

```
StreamingStatus Component State:

const [streamingStats, setStreamingStats] = useState(null)
const [systemStatus, setSystemStatus] = useState(null)
const [loading, setLoading] = useState(false)
const [error, setError] = useState(null)

useStreamingData() Hook:
  ├─ Manages local state
  ├─ Handles polling
  ├─ Fetches data
  ├─ Updates state
  └─ Returns { streamingStats, systemStatus, loading, error }

Component Render:
  ├─ If loading → Show skeleton
  ├─ If error → Show error message
  ├─ If no data → Show placeholder
  └─ If data → Display metrics with colors
```

---

## Integration Points Summary

### 1. Backend ↔ Database
```
ai_dashboard.py
  ├─ Query transactions (existing)
  ├─ Query stats (existing)
  ├─ Query streaming stats (NEW)
  └─ Return combined response
```

### 2. Backend ↔ Frontend
```
3 HTTP endpoints:
  ├─ GET /api/streaming/stats → Streaming metrics
  ├─ GET /api/streaming/health → Service health
  └─ GET /api/system/status → Combined status
```

### 3. Frontend ↔ UI
```
React Components:
  ├─ App.jsx → Main application
  ├─ StreamingStatus.jsx → Status display
  └─ useStreamingData.js → Data fetching
```

---

## Service Independence Diagram

```
Batch ETL Service          Ankr Streaming Service
        │                              │
        ├─ RPC_URL (owned)            ├─ ANKR_RPC_URL (free)
        ├─ Schedule-based             ├─ Continuous polling
        ├─ Rate limited               ├─ No rate limit
        ├─ Once per period            ├─ Every 12 seconds
        └─ Can fail silently          └─ Can fail silently
                │                              │
                └──────────┬───────────────────┘
                           ↓
                    PostgreSQL DB
                    (Single source
                     of truth)
                           ↓
                    Both write to
                    same tables
                           ↓
                    No conflicts
                    (independent)
```

---

## 🎯 Key Design Principles

### 1. **Separation of Concerns**
- Batch ETL ≠ Streaming Service
- Each has independent RPC
- Each can fail independently
- No coupling

### 2. **Unified Storage**
- Both write to PostgreSQL
- Same schema
- Combined queries work
- Stats reflect both

### 3. **Optional Streaming**
- Streaming is optional
- Works without streaming
- Graceful fallback
- HAS_STREAMING flag

### 4. **Real-time Frontend**
- Polling every 10 seconds
- Automatic updates
- Error handling
- Loading indicators

### 5. **Backward Compatibility**
- Existing endpoints unchanged
- No breaking changes
- Old clients still work
- Graceful degradation

---

**✅ Architecture Complete & Verified**
