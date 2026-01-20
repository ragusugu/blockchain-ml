# ✅ Frontend/Backend Alignment - Deployment Checklist

## 🎯 Pre-Deployment Verification

### Backend Setup ✅

- [x] **Streaming Manager Available**
  ```python
  # src/backend/api/ai_dashboard.py line 30-33
  try:
      from etl.streaming_manager import get_streaming_stats
      HAS_STREAMING = True
  except ImportError:
      HAS_STREAMING = False
  ```

- [x] **API Endpoints Configured**
  - ✅ `GET /api/streaming/stats` (line 896)
  - ✅ `GET /api/streaming/health` (line 923)
  - ✅ `GET /api/system/status` (line 955)

- [x] **Error Handling**
  - Try/except for streaming imports
  - Graceful fallback when streaming unavailable
  - Proper HTTP status codes

### Frontend Setup ✅

- [x] **Components Created**
  - ✅ `StreamingStatus.jsx` - Main display component
  - ✅ `useStreamingData.js` - React hooks for data fetching

- [x] **App.jsx Updated**
  - ✅ Import StreamingStatus (line 54)
  - ✅ Display conditionally (line 438)
  - ✅ Only shows in processing mode

- [x] **React Hooks Implemented**
  - useStreamingData() for streaming stats
  - useStreamingHealth() for service health
  - Auto-polling with 10s interval

---

## 🚀 Deployment Steps

### Step 1: Stop Current Services
```bash
# Stop running containers
docker-compose down

# Verify stopped
docker ps
```

### Step 2: Rebuild Backend Image
```bash
# Rebuild with updated ai_dashboard.py
docker-compose build backend

# Expected: Successfully tagged blockchainml:latest
```

### Step 3: Rebuild Frontend Image
```bash
# Rebuild with new components
docker-compose build frontend

# Expected: Successfully tagged blockchain-ml-frontend:latest
```

### Step 4: Start with Streaming Profile
```bash
# Start all services including streaming
docker-compose --profile streaming up -d

# Expected output:
# Creating postgres ... done
# Creating backend ... done
# Creating frontend ... done
# Creating ankr-streamer ... done

# Verify all running
docker-compose ps
```

### Step 5: Verify Backend Endpoints
```bash
# Wait 5 seconds for services to start
sleep 5

# Test system status endpoint
curl http://localhost:5000/api/system/status -s | jq .

# Expected response:
{
  "services": {
    "batch": {
      "status": "connected",
      "block_number": 18945234
    },
    "streaming": {
      "status": "running",
      "blocks_streamed": 345
    }
  },
  "timestamp": 1705318245
}
```

### Step 6: Test Streaming Stats Endpoint
```bash
# Get streaming statistics
curl http://localhost:5000/api/streaming/stats -s | jq .

# Expected response:
{
  "streaming_enabled": true,
  "blocks_streamed": 345,
  "transactions_streamed": 67890,
  "errors": 0,
  "last_update": "2024-01-15T10:30:45",
  "timestamp": 1705318245
}
```

### Step 7: Test Streaming Health Endpoint
```bash
# Check streaming service health
curl http://localhost:5000/api/streaming/health -s | jq .

# Expected response:
{
  "status": "healthy",
  "running": true,
  "blocks_streamed": 345,
  "errors": 0,
  "last_update": "2024-01-15T10:30:45"
}
```

### Step 8: Open Frontend
```bash
# Open in browser
open http://localhost:3000

# Or if WSL:
echo "http://localhost:3000"
```

### Step 9: Verify Frontend Components
- [ ] Page loads without errors
- [ ] Header displays
- [ ] Select processing mode
- [ ] StreamingStatus component appears
- [ ] Shows batch status
- [ ] Shows streaming status
- [ ] Updates every 10 seconds
- [ ] No console errors

### Step 10: Monitor Logs
```bash
# Terminal 1: Backend logs
docker-compose logs -f backend

# Terminal 2: Streaming service logs
docker-compose logs -f ankr-streamer

# Terminal 3: Frontend logs (if applicable)
docker-compose logs -f frontend

# Look for:
# ✅ Backend: "Running on http://0.0.0.0:5000"
# ✅ Streamer: "Streaming started" and "Block #12345"
# ✅ Frontend: Build successful
```

---

## ✅ Post-Deployment Verification

### Functionality Tests

- [ ] **Batch Processing**
  - Start batch ETL job
  - Verify data flows to database
  - Check `/api/transactions` returns data

- [ ] **Streaming Processing**
  - Verify streaming service is running
  - Check `/api/streaming/stats` shows > 0 blocks
  - Monitor database for streaming data

- [ ] **Combined Data**
  - Query all transactions
  - Should include both batch and streaming data
  - Statistics should reflect both sources

- [ ] **Frontend Display**
  - StreamingStatus shows both services
  - Real-time updates every 10s
  - No errors in browser console
  - Responsive UI

- [ ] **Error Scenarios**
  - Stop streaming service
  - Frontend should show "Not Available"
  - Batch processing continues normally
  - No crashes or exceptions

### Performance Metrics

```bash
# Check container resource usage
docker stats

# Expected:
# NAME              CPU %     MEM USAGE
# backend           1-2%      250-300MB
# ankr-streamer     0.5-1%    100-150MB
# frontend          <0.5%     50-100MB

# Check response times
curl -w "@curl-format.txt" http://localhost:5000/api/system/status
# Expected: Total: ~50-100ms
```

---

## 🔧 Troubleshooting

### Issue: StreamingStatus component not showing

**Diagnosis:**
```bash
# Check frontend console for errors
# Look for missing component import errors
# Verify processing mode is selected
```

**Solution:**
```bash
# Rebuild frontend
docker-compose build frontend --no-cache
docker-compose up -d frontend

# Check for import errors
docker-compose logs frontend
```

### Issue: API endpoints returning 404

**Diagnosis:**
```bash
# Check backend is running
docker-compose logs backend | grep "Running on"

# Test endpoint
curl -v http://localhost:5000/api/system/status
```

**Solution:**
```bash
# Restart backend
docker-compose restart backend

# Verify endpoints added correctly
grep -n "api/system/status" src/backend/api/ai_dashboard.py
```

### Issue: Streaming stats showing 0

**Diagnosis:**
```bash
# Check if ankr-streamer is running
docker-compose ps | grep ankr-streamer

# Check streaming logs
docker-compose logs ankr-streamer | tail -20
```

**Solution:**
```bash
# Restart streaming service
docker-compose restart ankr-streamer

# Check RPC connection
curl https://rpc.ankr.com/eth -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Issue: Frontend showing "Not Available" for streaming

**Check:** Is streaming service enabled?
```bash
# Start with profile
docker-compose --profile streaming up -d

# Without profile, streaming won't run
docker-compose up -d
# This is expected - will show "Not Available"
```

---

## 📋 Deployment Verification Checklist

### Before Starting
- [ ] All Docker images built (`docker-compose build`)
- [ ] Database initialized (`docker-compose up -d postgres`)
- [ ] No port conflicts (5000, 3000, 5432)
- [ ] Environment variables set correctly

### After Starting
- [ ] Backend service running and healthy
- [ ] Frontend service running and responsive
- [ ] Streaming service running (if profile enabled)
- [ ] Database accessible
- [ ] All API endpoints responding

### API Validation
- [ ] `GET /api/system/status` returns 200
- [ ] `GET /api/streaming/stats` returns 200
- [ ] `GET /api/streaming/health` returns 200
- [ ] Data format matches documentation

### Frontend Validation
- [ ] Page loads without console errors
- [ ] StreamingStatus component renders
- [ ] Metrics update automatically
- [ ] Toggle processing mode works
- [ ] No broken links or missing assets

### Data Validation
- [ ] Batch data present in database
- [ ] Streaming data present in database
- [ ] Combined queries work correctly
- [ ] Statistics updated correctly

### Performance Validation
- [ ] Response times < 500ms
- [ ] CPU usage < 10%
- [ ] Memory usage stable
- [ ] No memory leaks

---

## 🎉 Success Criteria

✅ **Deployment Successful When:**
- Backend returns all system status endpoints
- Frontend displays StreamingStatus component
- Real-time metrics update automatically
- Both batch and streaming data visible
- No console errors
- Services remain stable for > 5 minutes

---

## 📞 Support Commands

```bash
# View all logs
docker-compose logs

# View specific service
docker-compose logs backend -f

# See running containers
docker-compose ps

# Execute backend command
docker-compose exec backend python -c "from etl.streaming_manager import get_streaming_stats; print(get_streaming_stats())"

# Check network
docker network ls
docker inspect blockchain-ml_default

# Restart all services
docker-compose restart

# Full rebuild
docker-compose down && docker-compose build --no-cache && docker-compose --profile streaming up -d
```

---

## 📊 Final Checklist

| Component | Status | Notes |
|-----------|--------|-------|
| Backend API | ✅ Ready | 3 endpoints added |
| Frontend Components | ✅ Ready | 2 new components |
| React Hooks | ✅ Ready | useStreamingData implemented |
| Docker Config | ✅ Ready | Profile support added |
| Documentation | ✅ Complete | Full guides provided |
| Error Handling | ✅ Implemented | Graceful degradation |
| Backward Compat | ✅ Verified | No breaking changes |

---

**Status**: ✅ **READY FOR DEPLOYMENT**  
**Expected Time**: ~10 minutes  
**Risk Level**: 🟢 LOW (backward compatible)

