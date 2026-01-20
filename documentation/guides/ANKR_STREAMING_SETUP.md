# Ankr Streaming Integration Guide

## Overview

This setup enables **real-time blockchain data streaming using Ankr** completely independently from your batch ETL processing. The batch process (scheduler) continues to work as-is, while Ankr streaming runs in a separate service.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           Blockchain ML System                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐  ┌────────────────────────┐   │
│  │  BATCH PROCESSING    │  │  ANKR STREAMING       │   │
│  │  (Original)          │  │  (New - Independent)  │   │
│  ├──────────────────────┤  ├────────────────────────┤   │
│  │ • Scheduler (ETL)    │  │ • Ankr Streamer       │   │
│  │ • Main ETL Pipeline  │  │ • Stream Service      │   │
│  │ • Batch Processing   │  │ • Polling-based       │   │
│  │ • RPC-based          │  │ • FREE (no cost)      │   │
│  │ • Scheduled runs     │  │ • Real-time blocks    │   │
│  └──────────────────────┘  └────────────────────────┘   │
│           ↓                         ↓                     │
│         PostgreSQL Database (Shared)                     │
└─────────────────────────────────────────────────────────┘
```

## Features

### ✅ Ankr Streamer Features
- **Real-time Block Streaming**: Get new blocks as soon as they're mined
- **Free Service**: Uses Ankr's free RPC endpoint
- **Independent Operation**: Doesn't interfere with batch processing
- **Buffering**: Automatic batching of blocks for efficient processing
- **Error Handling**: Automatic retry on connection failures
- **Statistics**: Real-time streaming statistics
- **Callback Support**: Custom processing for each block

### ✅ Batch Processing (Unchanged)
- Original ETL pipeline continues unchanged
- Can run on a different schedule
- Uses its own configured RPC (Alchemy, Infura, etc.)
- Independent from streaming service

## Installation & Setup

### 1. Environment Variables

Update your `.env` file:

```bash
# ============ Ankr Streaming Configuration ============
ANKR_RPC_URL=https://rpc.ankr.com/eth          # Free endpoint
ANKR_POLLING_INTERVAL=12                       # Ethereum block time (seconds)
ANKR_BATCH_SIZE=10                             # Blocks per batch
STREAMING_ENABLED=true                         # Enable/disable streaming

# ============ Batch Processing (Keep Existing) ============
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY  # Your preferred RPC for batch
DATABASE_URL=postgresql://user:pass@localhost/db
```

### 2. Run Only Batch Processing (Original Setup)

```bash
# Run without streaming
docker-compose up -d

# Services running: backend, frontend, postgres, scheduler (batch ETL)
```

### 3. Run With Both Batch & Streaming

```bash
# Enable the optional streaming service
docker-compose --profile streaming up -d

# Now running: backend, frontend, postgres, scheduler, ankr-streamer
```

### 4. Run Streaming Only (Development)

```bash
# Run streaming service locally
cd src/backend
python -c "from etl.stream_service import AnkrStreamingService; AnkrStreamingService().run()"
```

## Usage Examples

### Example 1: Start Everything with Streaming

```bash
# Build and start all services including streaming
docker-compose --profile streaming up -d

# Check logs
docker-compose logs -f ankr-streamer
docker-compose logs -f scheduler
```

### Example 2: Programmatic Usage

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

# Get stats anytime
stats = get_streaming_stats()
print(f"Blocks streamed: {stats['blocks_streamed']}")
print(f"Transactions: {stats['transactions_streamed']}")
```

### Example 3: Custom Callback

```python
from etl.ankr_streamer import AnkrBlockchainStreamer

def my_callback(block_data):
    print(f"New block: {block_data['block_number']}")
    print(f"Transactions: {block_data['transaction_count']}")
    # Custom processing here

streamer = AnkrBlockchainStreamer(callback=my_callback)
streamer.connect()
streamer.stream()
```

## Configuration Options

### Ankr Streamer Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `ANKR_RPC_URL` | `https://rpc.ankr.com/eth` | Ankr RPC endpoint |
| `ANKR_POLLING_INTERVAL` | `12` | Seconds between polls |
| `ANKR_BATCH_SIZE` | `10` | Blocks per batch |
| `STREAMING_ENABLED` | `true` | Enable/disable service |

### Docker Compose Profiles

```bash
# Start without streaming (default)
docker-compose up

# Start with streaming
docker-compose --profile streaming up

# Start specific service
docker-compose up ankr-streamer
```

## Monitoring

### View Streaming Logs

```bash
# Real-time logs
docker-compose logs -f ankr-streamer

# Last 50 lines
docker-compose logs --tail=50 ankr-streamer
```

### Check Service Status

```bash
# List running services
docker-compose ps

# Check specific service
docker-compose logs ankr-streamer | grep "✅"
```

### Sample Output

```
[Ankr Streamer] - INFO - 🔗 Connecting to Ankr: https://rpc.ankr.com/eth
[Ankr Streamer] - INFO - ✅ Connected to Ankr - Current block: 18945234
[Ankr Streamer] - INFO - 🚀 Starting Ankr streaming (interval: 12s)
[Ankr Streamer] - INFO - 📦 Found 1 new block(s)
[Ankr Streamer] - INFO - ✅ Block 18945235: 156 txs, 234.5678 ETH
[Ankr Streamer] - INFO - ✅ Block 18945236: 142 txs, 189.1234 ETH
```

## Architecture Components

### 1. **ankr_streamer.py** - Core Streaming Engine
- Connects to Ankr RPC
- Polls for new blocks
- Processes transactions
- Maintains statistics
- Buffer management

### 2. **streaming_manager.py** - Service Manager
- Manages streamer lifecycle
- Thread management
- Global instance handling
- Statistics aggregation

### 3. **stream_service.py** - Standalone Service
- Entry point for streaming service
- Graceful shutdown handling
- Logging and monitoring
- Callback system

## Performance Metrics

### Expected Performance

| Metric | Value |
|--------|-------|
| Blocks/sec | 1 (Ethereum block time: 12s) |
| Transactions/block | 100-300 average |
| Memory usage | ~100MB |
| CPU usage | <5% (idle polling) |
| Free tier throughput | Unlimited |

### Optimization Tips

1. **Adjust polling interval** based on your needs:
   ```bash
   ANKR_POLLING_INTERVAL=6  # More frequent polling
   ```

2. **Batch size** for database operations:
   ```bash
   ANKR_BATCH_SIZE=20  # Larger batches
   ```

3. **Use connection pooling** for database operations

## Troubleshooting

### Issue: "Failed to connect to Ankr"

```bash
# Solution: Check internet connection and Ankr status
curl https://rpc.ankr.com/eth -X POST -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' -H "Content-Type: application/json"
```

### Issue: High memory usage

```bash
# Reduce batch size
ANKR_BATCH_SIZE=5

# Increase polling interval
ANKR_POLLING_INTERVAL=20
```

### Issue: Streaming not starting

```bash
# Check logs
docker-compose logs ankr-streamer

# Verify profile is enabled
docker-compose --profile streaming logs ankr-streamer

# Test locally
python src/backend/etl/stream_service.py
```

## Integration with Existing Components

### Database Storage

Streaming data automatically stored in the same PostgreSQL database as batch processing:

```python
# Data is transformed and stored using existing functions
from etl.transform import transform_data

block_data = streamer.get_block_data(block_num)
transformed = transform_data(block_data)  # Uses existing transform logic
# Stored in database
```

### API Access

Streaming data is accessible through the same backend API:

```bash
# Get streaming stats via API (add this endpoint if needed)
curl http://localhost:5000/api/streaming/stats
```

### Frontend Integration

Display streaming statistics in React dashboard:

```javascript
// Real-time updates via polling or WebSocket
useEffect(() => {
  const interval = setInterval(() => {
    fetch('/api/streaming/stats')
      .then(r => r.json())
      .then(data => setStreamingStats(data));
  }, 5000);
  return () => clearInterval(interval);
}, []);
```

## Disable Streaming

To disable streaming without removing the code:

```bash
# Set environment variable
STREAMING_ENABLED=false

# Or don't use the streaming profile
docker-compose up  # Without --profile streaming
```

## Next Steps

1. ✅ Update `.env` with Ankr settings
2. ✅ Start with streaming: `docker-compose --profile streaming up -d`
3. ✅ Monitor logs: `docker-compose logs -f ankr-streamer`
4. ✅ Verify both batch and streaming are running
5. ✅ Add custom callbacks for your use case
6. ✅ Integrate streaming stats into frontend

## Support

For issues or questions:
- Check the logs: `docker-compose logs ankr-streamer`
- Verify Ankr connectivity: `curl https://rpc.ankr.com/eth`
- Review `etl/ankr_streamer.py` for configuration options
