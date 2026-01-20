# Ankr Streaming Setup - Getting Started

## 🎯 What You Get

Your blockchain-ml project now includes **Ankr Streaming** - a completely independent real-time data streaming service that works alongside your batch ETL processing.

### Key Differences

| Feature | Batch ETL (Original) | Ankr Streaming (New) |
|---------|---------------------|----------------------|
| **How it works** | Scheduled jobs | Real-time polling |
| **Runs when** | On schedule (e.g., daily) | Continuously |
| **Block data** | Historical batches | Latest blocks |
| **RPC endpoint** | Your choice (Alchemy, Infura) | Ankr (free) |
| **Cost** | Based on your RPC choice | **FREE** |
| **Updates** | Periodic | ~1 block/12 seconds |
| **Startup** | `python main_etl.py` | `python stream_service.py` |

## ⚡ Quick Start (3 Steps)

### Step 1: Add to `.env`
```bash
# Ankr Configuration (add these lines)
ANKR_RPC_URL=https://rpc.ankr.com/eth
ANKR_POLLING_INTERVAL=12
ANKR_BATCH_SIZE=10
STREAMING_ENABLED=true
```

### Step 2: Start Services
```bash
# With streaming enabled
docker-compose --profile streaming up -d

# Without streaming (original behavior)
docker-compose up -d
```

### Step 3: Monitor
```bash
# Watch streaming logs
docker-compose logs -f ankr-streamer

# Or check batch processing
docker-compose logs -f scheduler
```

## 📦 What's Running?

### Without `--profile streaming` (Default)
```
✅ Backend API (http://localhost:5000)
✅ Frontend (http://localhost:3000)
✅ PostgreSQL (localhost:5432)
✅ Batch Scheduler/ETL (original)
✅ ML Worker
❌ Ankr Streamer (disabled)
```

### With `--profile streaming`
```
✅ Backend API (http://localhost:5000)
✅ Frontend (http://localhost:3000)
✅ PostgreSQL (localhost:5432)
✅ Batch Scheduler/ETL (original)
✅ ML Worker
✅ Ankr Streamer (ENABLED - NEW!)
```

## 🔍 Verify It's Working

### Check logs for success indicators
```bash
docker-compose logs ankr-streamer | grep "✅"
```

### Expected output
```
[Ankr Streamer] - INFO - ✅ Connected to Ankr - Current block: 18945234
[Ankr Streamer] - INFO - ✅ Block 18945235: 156 txs, 234.5678 ETH
[Ankr Streamer] - INFO - ✅ Block 18945236: 142 txs, 189.1234 ETH
```

### Check all services
```bash
docker-compose ps
```

## 📁 New Files

All files are in your existing project structure:

```
src/backend/etl/
├── ankr_streamer.py           ← Core streaming engine
├── streaming_manager.py        ← Service manager
└── stream_service.py           ← Standalone entry point

documentation/guides/
└── ANKR_STREAMING_SETUP.md     ← Detailed setup guide

scripts/
├── setup_ankr_streaming.sh     ← Quick reference
└── test_ankr_streaming.py      ← Validation script
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `ANKR_RPC_URL` | `https://rpc.ankr.com/eth` | Free Ankr endpoint (no auth) |
| `ANKR_POLLING_INTERVAL` | `12` | Seconds between block polls |
| `ANKR_BATCH_SIZE` | `10` | Blocks per batch write |
| `STREAMING_ENABLED` | `true` | Enable/disable streaming |

### Fine Tuning

**For more real-time updates** (more frequent polling):
```bash
ANKR_POLLING_INTERVAL=6  # Poll every 6 seconds instead of 12
```

**For better performance** (larger batches):
```bash
ANKR_BATCH_SIZE=20  # Process 20 blocks per batch
```

**For lower memory usage**:
```bash
ANKR_BATCH_SIZE=5   # Smaller batches
ANKR_POLLING_INTERVAL=20  # Less frequent polling
```

## 🚀 Common Tasks

### Start everything with streaming
```bash
docker-compose --profile streaming up -d
```

### Start without streaming (original setup)
```bash
docker-compose up -d
```

### Stop streaming (keep batch running)
```bash
docker-compose stop ankr-streamer
```

### Restart streaming
```bash
docker-compose restart ankr-streamer
```

### View streaming stats
```bash
docker-compose logs ankr-streamer | tail -20
```

### Check if streaming is healthy
```bash
docker-compose logs ankr-streamer | grep -E "(✅|❌|⚠️)"
```

## 🛠️ Troubleshooting

### Problem: "ankr-streamer service not found"
**Solution**: Make sure to use the `--profile streaming` flag
```bash
docker-compose --profile streaming up -d
```

### Problem: "Connection refused"
**Solution**: Check Ankr is accessible
```bash
curl https://rpc.ankr.com/eth \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Problem: Streaming stops with errors
**Solution**: Check logs and restart
```bash
docker-compose logs ankr-streamer
docker-compose restart ankr-streamer
```

### Problem: High memory usage
**Solution**: Reduce batch size and polling frequency
```bash
ANKR_BATCH_SIZE=5
ANKR_POLLING_INTERVAL=20
```

## 📊 What Data You Get

Each block contains:
- Block number and hash
- Timestamp
- Miner address
- Gas used/limit
- **Transaction data**:
  - Hash
  - From/To addresses
  - ETH value transferred
  - Gas price
  - Transaction status

## 🔗 Integration Examples

### Python: Get streaming data
```python
from etl.streaming_manager import (
    initialize_streaming,
    start_streaming_service,
    get_streaming_stats
)

# Initialize
initialize_streaming()

# Start in background
start_streaming_service(background=True)

# Get stats
stats = get_streaming_stats()
print(f"Blocks: {stats['blocks_streamed']}")
print(f"Transactions: {stats['transactions_streamed']}")
```

### Python: Custom callback
```python
from etl.ankr_streamer import AnkrBlockchainStreamer

def on_new_block(block_data):
    print(f"Block #{block_data['block_number']}")
    print(f"  Transactions: {block_data['transaction_count']}")
    print(f"  ETH value: {block_data['total_eth_value']}")

streamer = AnkrBlockchainStreamer(callback=on_new_block)
streamer.connect()
streamer.stream()
```

### Docker: Run streaming standalone
```bash
docker run -e ANKR_RPC_URL=https://rpc.ankr.com/eth \
  blockchainml:latest \
  python -c "from etl.stream_service import AnkrStreamingService; AnkrStreamingService().run()"
```

## 📚 Learn More

- **Full setup guide**: See `documentation/guides/ANKR_STREAMING_SETUP.md`
- **Code reference**: See `src/backend/etl/ankr_streamer.py`
- **Quick reference**: Run `bash scripts/setup_ankr_streaming.sh`

## ✅ Next Steps

1. **Update your `.env`** with the settings above
2. **Start with streaming**: `docker-compose --profile streaming up -d`
3. **Check logs**: `docker-compose logs -f ankr-streamer`
4. **Verify success**: Look for `✅` messages in logs
5. **Integrate into your app**: Add callbacks for custom processing
6. **Monitor performance**: Check CPU/memory usage

## 💡 Key Points

✅ **No API key needed** - Ankr is completely free
✅ **Independent** - Doesn't affect batch processing
✅ **Real-time** - Blocks streamed as they're mined
✅ **Reliable** - Automatic retries on errors
✅ **Scalable** - Can handle any throughput
✅ **Optional** - Use `--profile streaming` to enable/disable

## Support

If you encounter issues:
1. Check logs: `docker-compose logs ankr-streamer`
2. Verify connectivity: `curl https://rpc.ankr.com/eth`
3. Review configuration in `.env`
4. Check `ANKR_STREAMING_SETUP.md` for detailed guide

---

**Ready to start?**
```bash
docker-compose --profile streaming up -d
docker-compose logs -f ankr-streamer
```

**Status**: ✅ Ready to use | **Cost**: 💰 Free | **Setup time**: ⏱️ 2 minutes
