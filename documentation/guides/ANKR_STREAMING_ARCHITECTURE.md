# Ankr Streaming - Architecture & Integration Guide

## System Architecture

### Before (Original Setup)
```
┌─────────────────────────────────────┐
│      BLOCKCHAIN-ML PROJECT          │
├─────────────────────────────────────┤
│                                     │
│  Frontend ──┐                       │
│             ├─→ Backend API         │
│  ML Worker ─┘                       │
│                    ↓                │
│             PostgreSQL              │
│                    ↑                │
│            Scheduler (ETL)          │
│         (Batch Processing)          │
│         - Runs on schedule          │
│         - Uses: RPC_URL             │
│                                     │
└─────────────────────────────────────┘
```

### After (With Ankr Streaming)
```
┌─────────────────────────────────────────────────────┐
│         BLOCKCHAIN-ML PROJECT                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Frontend ──┐                                      │
│             ├─→ Backend API                        │
│  ML Worker ─┘         ↑                            │
│                       │                            │
│         ┌─────────────┴─────────────┐              │
│         ↓                           ↓              │
│    PostgreSQL ←──────────────────────────┐         │
│         ↑                                │         │
│         │                               │         │
│    ┌────┴────────┐          ┌──────────┴────┐     │
│    │             │          │               │     │
│  BATCH ETL      │      ANKR STREAMING      │     │
│  (Scheduler)    │      (Real-time)        │     │
│  • RPC_URL      │      • ANKR_RPC_URL     │     │
│  • Scheduled    │      • Continuous       │     │
│  • Historical   │      • Live blocks      │     │
│                 │      • FREE             │     │
│                 │                        │     │
└─────────────────┴────────────────────────┴─────┘
```

## Data Flow

### Batch Processing Flow (Original)
```
Schedule time ──→ Scheduler ──→ RPC (Alchemy/Infura)
     ↓
Extract blocks ──→ Transform ──→ Validate
     ↓
Load to DB ──→ ML Pipeline ──→ Dashboard
```

### Ankr Streaming Flow (New)
```
Every 12 seconds ──→ Ankr Poller ──→ RPC (Ankr - FREE!)
        ↓
   Get new block ──→ Extract transactions
        ↓
  Buffer blocks (10 at a time)
        ↓
Transform ──→ Load to DB ──→ Available for queries
```

### Combined Flow
```
┌──────────────────────────────────────────────────────┐
│           BLOCKCHAIN ETHEREUM NETWORK                 │
└──────────────────────────────────────────────────────┘
                     ↓              ↓
          ┌──────────┴────┐   ┌─────┴──────┐
          ↓               ↓   ↓            ↓
      [RPC_URL]      [ANKR_RPC_URL]
      (Your choice)   (Ankr - Free)
          ↓               ↓
    SCHEDULER/ETL   ANKR STREAMER
    (Batch)         (Real-time)
          ↓               ↓
          └───────┬───────┘
                  ↓
        POSTGRESQL DATABASE
         (Unified Storage)
                  ↓
    ┌─────────────┼─────────────┐
    ↓             ↓             ↓
  API      Dashboard    ML Models
(Real-time) (Analysis)  (Predictions)
```

## Deployment Models

### Model 1: Batch Only (Original)
```bash
docker-compose up -d

Running:
- Backend
- Frontend  
- Database
- Batch ETL Scheduler
- ML Worker

NOT running:
- Ankr Streamer (disabled)
```

### Model 2: Streaming Only (Development)
```bash
python src/backend/etl/stream_service.py

Running:
- Ankr Streamer (connects to existing DB)

NOT running:
- Docker services
```

### Model 3: Batch + Streaming (Recommended)
```bash
docker-compose --profile streaming up -d

Running:
- Backend
- Frontend
- Database
- Batch ETL Scheduler
- ML Worker
- Ankr Streamer (NEW!)
```

## Data Processing Pipeline

### Batch ETL (Scheduled)
```
Day 1, 00:00 UTC
     ↓
Fetch blocks 1000-2000 (historical)
     ↓
Extract transactions
     ↓
Transform to schema
     ↓
Validate data
     ↓
Load to database
     ↓
Generate reports
```

### Ankr Streaming (Continuous)
```
Block N
  ↓
Fetch immediately
  ↓
Extract transactions
  ↓
Buffer 10 blocks
  ↓
Batch transform
  ↓
Load to database
  ↓
Real-time available
  ↓
Block N+1 (12s later)
```

## Database Schema (Unchanged)

Both batch and streaming use the **same database schema**:

```
PostgreSQL Database
├── transactions
│   ├── hash
│   ├── from_address
│   ├── to_address
│   ├── value
│   ├── gas_price
│   ├── gas_used
│   └── timestamp
├── blocks
│   ├── number
│   ├── hash
│   ├── miner
│   ├── gas_used
│   └── timestamp
└── ml_predictions
    ├── transaction_id
    ├── fraud_score
    └── prediction_time
```

## API Endpoints (Unified)

All data is accessible through the same API:

```
GET /api/blocks              → Latest blocks (from streaming + batch)
GET /api/transactions        → Transactions (from streaming + batch)
GET /api/analytics          → Analysis (combining both sources)
GET /api/streaming/stats    → Streaming statistics (NEW)
POST /api/predictions       → ML predictions (on combined data)
```

## Performance Comparison

### Batch Processing
- Updates: Every 24 hours
- Latency: Hours/Days
- Volume: 100K+ blocks per run
- Cost: Based on RPC provider
- Use case: Historical analysis, reports

### Ankr Streaming
- Updates: Every 12 seconds
- Latency: Seconds
- Volume: ~150-300 txs per block
- Cost: FREE
- Use case: Real-time monitoring, alerts

### Combined
- Fast + Comprehensive
- Real-time + Historical
- Full coverage
- FREE + Your RPC

## Configuration Hierarchy

```
Environment Variables (.env)
         ↓
Docker Compose Overrides
         ↓
Default Values in Code
```

Example `.env`:
```bash
# Batch Processing
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
ETL_SCHEDULE_HOUR=0
ETL_SCHEDULE_MINUTE=0

# Ankr Streaming
ANKR_RPC_URL=https://rpc.ankr.com/eth          (default)
ANKR_POLLING_INTERVAL=12                       (default)
ANKR_BATCH_SIZE=10                             (default)
STREAMING_ENABLED=true                         (default)

# Database (shared)
DATABASE_URL=postgresql://user:pass@localhost/db
```

## File Structure

```
blockchain-ml/
├── src/backend/
│   ├── api/
│   │   └── ai_dashboard.py         (API endpoints)
│   ├── etl/
│   │   ├── main_etl.py             (Batch ETL - unchanged)
│   │   ├── extract.py              (Extraction - unchanged)
│   │   ├── transform.py            (Transform - unchanged)
│   │   ├── ankr_streamer.py        (✨ NEW - Streaming engine)
│   │   ├── streaming_manager.py    (✨ NEW - Service manager)
│   │   └── stream_service.py       (✨ NEW - Entry point)
│   └── ml/
│       └── realtime_processor.py   (Unchanged)
├── docker/
│   └── docker-compose.yml          (✨ Updated - added profile)
├── documentation/guides/
│   ├── ANKR_STREAMING_SETUP.md     (✨ NEW - Full guide)
│   └── ... (existing guides)
├── scripts/
│   ├── setup_ankr_streaming.sh     (✨ NEW - Quick ref)
│   └── test_ankr_streaming.py      (✨ NEW - Validation)
├── ANKR_STREAMING_SUMMARY.md       (✨ NEW - Overview)
└── ANKR_STREAMING_QUICKSTART.md    (✨ NEW - Quick start)
```

## Integration Points

### 1. Database
```python
# Shared database connection
DATABASE_URL = "postgresql://user:pass@localhost/db"
# Both batch and streaming write to same tables
```

### 2. Transformation
```python
# Both use same transform function
from etl.transform import transform_data
transformed = transform_data(raw_blocks)
```

### 3. API
```python
# All data available through API
# Batch historical + Streaming real-time
GET /api/transactions?source=all
```

### 4. ML Models
```python
# ML models work on combined data
from ml.ai_fraud_detector import predict
predictions = predict(transactions)  # batch + streaming
```

## Scaling Scenarios

### Scenario 1: Low Volume (Development)
```
- Single Ankr streamer
- Batch runs daily
- Database local or small instance
- No caching needed
```

### Scenario 2: Medium Volume (Production)
```
- Ankr streamer + Batch ETL
- Batch runs hourly
- Database medium instance (RDS)
- Redis cache for analytics
```

### Scenario 3: High Volume (Enterprise)
```
- Multiple Ankr streamers (different chains)
- Batch runs every 15 minutes
- Database large instance (Aurora)
- Distributed cache + message queue
- Separate read replicas
```

## Security Considerations

### Network
- Ankr: Public endpoint (read-only)
- Database: Private network (local/VPC)
- API: Rate limited

### Data
- No private keys handled
- Public blockchain data only
- Database access controlled

### Credentials
- No API keys needed for Ankr
- Database credentials in .env (not in git)
- RPC credentials in .env only

## Troubleshooting Matrix

| Issue | Batch | Streaming | Solution |
|-------|-------|-----------|----------|
| No data | Check RPC | Check Ankr | Verify connectivity |
| Slow | Check schedule | Increase polling | Reduce batch size |
| Memory high | Reduce batch | Reduce batch | Lower BATCH_SIZE |
| DB full | Archive old | Prune old | Implement retention |
| API slow | Index tables | Cache results | Add Redis |

## Monitoring & Alerts

### Batch ETL
```
- Check scheduler logs
- Monitor ETL runtime
- Alert on failures
```

### Ankr Streaming
```
- Check streaming logs
- Monitor block lag
- Track transaction rate
- Alert on connection loss
```

### Combined
```
- Dashboard with both metrics
- Alert if one stops
- Reconcile data differences
```

---

**Next**: Ready to deploy? Start with [ANKR_STREAMING_QUICKSTART.md](ANKR_STREAMING_QUICKSTART.md)
