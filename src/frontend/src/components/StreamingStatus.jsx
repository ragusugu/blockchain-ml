import React, { useState, useEffect } from 'react'
import { Box, Paper, Grid, Typography, Chip, CircularProgress, Alert } from '@mui/material'
import { Activity, AlertCircle, CheckCircle, TrendingUp } from 'lucide-react'
import axios from 'axios'

/**
 * StreamingStatus Component
 * Displays real-time Ankr streaming service statistics
 * Shows both batch ETL and streaming service health
 */
const StreamingStatus = () => {
  const [systemStatus, setSystemStatus] = useState(null)
  const [streamingStats, setStreamingStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        setLoading(true)
        
        // Get system status (both batch and streaming)
        const statusRes = await axios.get('/api/system/status')
        setSystemStatus(statusRes.data)
        
        // Get streaming specific stats
        const streamingRes = await axios.get('/api/streaming/stats')
        setStreamingStats(streamingRes.data)
        
        setError(null)
      } catch (err) {
        console.error('Error fetching system status:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    // Initial fetch
    fetchStatus()
    
    // Poll every 10 seconds
    const interval = setInterval(fetchStatus, 10000)
    
    return () => clearInterval(interval)
  }, [])

  if (loading && !systemStatus) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
        <CircularProgress size={24} />
      </Box>
    )
  }

  if (error) {
    return (
      <Alert severity="warning" sx={{ mb: 2 }}>
        Could not fetch system status: {error}
      </Alert>
    )
  }

  if (!systemStatus) {
    return null
  }

  const batch = systemStatus.services?.batch
  const streaming = systemStatus.services?.streaming

  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 'bold' }}>
        📊 System Status
      </Typography>
      
      <Grid container spacing={2}>
        {/* Batch Processing Status */}
        <Grid item xs={12} sm={6}>
          <Paper sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <CheckCircle size={20} style={{ marginRight: 8, color: batch?.w3_connected ? '#4caf50' : '#f44336' }} />
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                Batch ETL
              </Typography>
            </Box>
            
            <Box sx={{ ml: 3 }}>
              <Typography variant="body2" color="textSecondary">
                RPC: {batch?.w3_connected ? '✅ Connected' : '❌ Disconnected'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Block: #{batch?.latest_block || 'N/A'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Gas: {batch?.gas_price?.toFixed(2) || 'N/A'} Gwei
              </Typography>
              <Typography variant="body2" color="textSecondary">
                AI: {batch?.model_enabled ? '✅ Enabled' : '⚪ Disabled'}
              </Typography>
            </Box>
          </Paper>
        </Grid>

        {/* Ankr Streaming Status */}
        <Grid item xs={12} sm={6}>
          <Paper sx={{ p: 2, backgroundColor: streaming?.running ? '#e8f5e9' : '#fff3e0' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Activity 
                size={20} 
                style={{ 
                  marginRight: 8, 
                  color: streaming?.running ? '#4caf50' : '#ff9800',
                  animation: streaming?.running ? 'pulse 2s infinite' : 'none'
                }} 
              />
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                Ankr Streaming
              </Typography>
            </Box>
            
            <Box sx={{ ml: 3 }}>
              <Typography variant="body2" color="textSecondary">
                Status: {streaming?.available ? (streaming?.running ? '✅ Running' : '⏸️ Stopped') : '❌ Not Available'}
              </Typography>
              {streaming?.available && (
                <>
                  <Typography variant="body2" color="textSecondary">
                    Blocks: {streamingStats?.stats?.blocks_streamed || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Transactions: {streamingStats?.stats?.transactions_streamed || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Errors: {streamingStats?.stats?.errors || 0}
                  </Typography>
                </>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Data Sources Info */}
      <Box sx={{ mt: 2, p: 2, backgroundColor: '#e3f2fd', borderRadius: 1 }}>
        <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 1 }}>
          📚 Data Sources:
        </Typography>
        <Box sx={{ ml: 2 }}>
          <Chip 
            label={`Batch ETL: ${systemStatus.data_sources?.batch_etl || 'PostgreSQL'}`}
            size="small"
            sx={{ mr: 1, mb: 1 }}
          />
          <Chip 
            label={`Streaming: ${systemStatus.data_sources?.ankr_streaming || 'Not available'}`}
            size="small"
            color={streaming?.available ? 'success' : 'default'}
          />
        </Box>
      </Box>
    </Box>
  )
}

export default StreamingStatus
