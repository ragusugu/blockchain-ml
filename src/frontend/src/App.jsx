import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  TextField,
  Card,
  CardContent,
  CircularProgress,
  Modal,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  AppBar,
  Toolbar,
  Switch,
  FormControlLabel,
  Alert,
  Fade,
  Skeleton,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
} from '@mui/material'
import {
  Cloud,
  TrendingUp,
  Zap,
  Database,
  GitBranch,
  AlertTriangle,
  CheckCircle,
  Clock,
  ChevronRight,
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import OptionCard from './components/OptionCard'
import StatCard from './components/StatCard'
import TransactionTable from './components/TransactionTable'
import DetailModal from './components/DetailModal'
import Header from './components/Header'
import ModeSelector from './components/ModeSelector'

const MotionCard = motion(Card)
const MotionPaper = motion(Paper)

function App() {
  const [processingMode, setProcessingMode] = useState(null) // 'scheduled' or 'realtime'
  const [selectedOption, setSelectedOption] = useState(null)
  const [blockCount, setBlockCount] = useState(10)
  const [transactions, setTransactions] = useState([])
  const [stats, setStats] = useState(null)
  const [options, setOptions] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedTx, setSelectedTx] = useState(null)
  const [autoRefresh, setAutoRefresh] = useState(false)
  const [error, setError] = useState(null)
  const [refreshInterval, setRefreshInterval] = useState(5000) // milliseconds
  const [scheduleFrequency, setScheduleFrequency] = useState('5s') // for scheduled mode
  const [modelEnabled, setModelEnabled] = useState(true)
  const [aiLoaded, setAiLoaded] = useState(true)

  // Fetch options on mount and check health
  useEffect(() => {
    checkHealth()
    fetchStats()
  }, [])

  const checkHealth = async () => {
    try {
      const response = await axios.get('/api/health')
      const { w3_connected, ai_loaded, model_enabled } = response.data

      setModelEnabled(model_enabled)
      setAiLoaded(ai_loaded)

      if (!w3_connected) {
        setError('⚠️ Web3 connection failed. Check your RPC URL and network connection.')
        return
      }

      if (model_enabled && !ai_loaded) {
        setError('⚠️ AI models not loaded. Models may still be loading...')
        return
      }

      if (!model_enabled) {
        setError(null)
      }
    } catch (err) {
      console.error('Health check failed:', err)
      setError('⚠️ Backend not responding. Make sure the server is running.')
    }
  }

  // Auto-refresh logic with configurable interval
  useEffect(() => {
    if (!autoRefresh || !selectedOption) return
    const interval = setInterval(() => {
      fetchTransactions()
    }, refreshInterval)
    return () => clearInterval(interval)
  }, [autoRefresh, selectedOption, refreshInterval])

  const fetchOptionsForMode = async (mode) => {
    try {
      const response = await axios.get('/api/options', {
        params: { mode }
      })
      
      if (!response.data.options || response.data.options.length === 0) {
        setError(`❌ No options available for ${mode} mode`)
        setOptions([])
        return
      }
      
      setOptions(response.data.options)
      setError(null)  // Clear any previous errors
      console.log(`✅ Loaded ${response.data.options.length} options for ${mode} mode`)
    } catch (err) {
      console.error('Error fetching options:', err)
      const errorMsg = err.response?.data?.error || err.message || 'Unknown error'
      const errorDetails = err.response?.data?.details || ''
      setError(`❌ Failed to load options for ${mode} mode: ${errorMsg}${errorDetails ? ' - ' + errorDetails : ''}`)
      setOptions([])
    }
  }

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/stats')
      setStats(response.data)
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const fetchTransactions = async () => {
    if (!selectedOption) {
      setError('Please select an option first')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await axios.post('/api/transactions', {
        mode: processingMode,
        option: selectedOption.toString(),
        block_count: blockCount,
      })
      
      if (response.data.error) {
        setError(`❌ ${response.data.error}: ${response.data.details || ''}`)
        return
      }
      
      setTransactions(response.data.transactions || [])
      setStats(response.data.stats)
    } catch (err) {
      console.error('Error fetching transactions:', err)
      const errorMsg = err.response?.data?.error || err.message || 'Unknown error'
      const errorDetails = err.response?.data?.details || ''
      setError(`Failed to fetch transactions: ${errorMsg}${errorDetails ? ' - ' + errorDetails : ''}`)
    } finally {
      setLoading(false)
    }
  }

  const toggleModel = async (enabled) => {
    setModelEnabled(enabled)
    try {
      await axios.post('/api/model-toggle', { enabled })
      if (enabled) {
        // Re-run health to confirm model loads
        await checkHealth()
      }
    } catch (err) {
      console.error('Error toggling model:', err)
      setModelEnabled(!enabled)
      const errorMsg = err.response?.data?.message || 'Failed to update model state'
      setError(`❌ ${errorMsg}`)
    }
  }

  const handleSelectMode = (mode) => {
    setProcessingMode(mode)
    // Fetch options for the selected mode
    fetchOptionsForMode(mode)
  }

  const handleSelectOption = (optionId) => {
    setSelectedOption(optionId)
    // Auto-enable refresh for real-time mode
    if (processingMode === 'realtime') {
      setAutoRefresh(true)
      setRefreshInterval(10000) // 10 seconds for real-time
    }
  }

  const handleFetch = () => {
    fetchTransactions()
  }

  const handleViewDetails = async (hash) => {
    setLoading(true)
    try {
      const response = await axios.get(`/api/transaction/${hash}`)
      setSelectedTx(response.data)
    } catch (err) {
      console.error('Error fetching transaction details:', err)
      setError('Failed to load transaction details')
    } finally {
      setLoading(false)
    }
  }

  const handleBackToMode = () => {
    setProcessingMode(null)
    setSelectedOption(null)
    setTransactions([])
    setStats(null)
    setError(null)
  }

  const selectedOptionData = options.find(o => o.id === selectedOption)

  // Show mode selector first
  if (!processingMode) {
    return <ModeSelector onSelectMode={handleSelectMode} />
  }

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#0f172a' }}>
      <Header stats={stats} />

      <Container maxWidth="xl" sx={{ py: 4 }}>
        {error && (
          <Fade in={!!error}>
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          </Fade>
        )}

        <Grid container spacing={3}>
          {/* Left Panel - Options */}
          <Grid item xs={12} md={3}>
            <MotionPaper
              component={motion.div}
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.5 }}
              sx={{
                p: 2,
                background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                border: '1px solid #334155',
                minHeight: '600px',
                display: 'flex',
                flexDirection: 'column',
                gap: 2,
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                Processing Options
              </Typography>

              {options.map((option) => (
                <OptionCard
                  key={option.id}
                  option={option}
                  isSelected={selectedOption === option.id}
                  onSelect={() => handleSelectOption(option.id)}
                />
              ))}

              <Box sx={{ mt: 'auto', pt: 3, borderTop: '1px solid #334155' }}>
                <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
                  ⚙️ Configuration
                </Typography>

                <TextField
                  fullWidth
                  label="Number of Blocks"
                  type="number"
                  value={blockCount}
                  onChange={(e) => setBlockCount(Math.max(1, Math.min(100, parseInt(e.target.value) || 1)))}
                  inputProps={{ min: 1, max: 100 }}
                  size="small"
                  sx={{ mb: 2 }}
                />

                <Button
                  fullWidth
                  variant="contained"
                  onClick={handleFetch}
                  disabled={!selectedOption || loading}
                  sx={{
                    background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                    mb: 2,
                    py: 1.5,
                    fontWeight: 600,
                    transition: 'all 0.3s ease',
                    opacity: loading ? 0.8 : 1,
                  }}
                >
                  {loading ? (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <CircularProgress size={16} sx={{ color: 'inherit' }} />
                      <span>Analyzing...</span>
                    </Box>
                  ) : (
                    '🔄 Fetch & Analyze'
                  )}
                </Button>

                {/* Scheduling Settings - Only for Scheduled Mode */}
                {processingMode === 'scheduled' && (
                  <Box sx={{ 
                    p: 2, 
                    background: 'rgba(99, 102, 241, 0.1)', 
                    borderRadius: 2,
                    border: '1px solid #334155'
                  }}>
                    <Typography variant="subtitle2" sx={{ mb: 1.5, fontWeight: 600, color: '#94a3b8' }}>
                      📅 Schedule Settings
                    </Typography>

                    <FormControl fullWidth size="small" sx={{ mb: 2 }}>
                      <InputLabel id="frequency-label">Frequency</InputLabel>
                      <Select
                        labelId="frequency-label"
                        value={scheduleFrequency}
                        label="Frequency"
                        onChange={(e) => {
                          setScheduleFrequency(e.target.value)
                          const intervals = {
                            '5s': 5000,
                            '10s': 10000,
                            '30s': 30000,
                            '1m': 60000,
                            '5m': 300000,
                            '10m': 600000,
                          }
                          setRefreshInterval(intervals[e.target.value] || 5000)
                        }}
                        disabled={!selectedOption}
                      >
                        <MenuItem value="5s">Every 5 seconds</MenuItem>
                        <MenuItem value="10s">Every 10 seconds</MenuItem>
                        <MenuItem value="30s">Every 30 seconds</MenuItem>
                        <MenuItem value="1m">Every 1 minute</MenuItem>
                        <MenuItem value="5m">Every 5 minutes</MenuItem>
                        <MenuItem value="10m">Every 10 minutes</MenuItem>
                      </Select>
                    </FormControl>

                    <FormControlLabel
                      control={
                        <Switch
                          checked={autoRefresh}
                          onChange={(e) => setAutoRefresh(e.target.checked)}
                          disabled={!selectedOption}
                          sx={{
                            '& .MuiSwitch-switchBase.Mui-checked': {
                              color: '#3b82f6',
                            },
                            '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                              backgroundColor: '#3b82f6',
                            },
                          }}
                        />
                      }
                      label={
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {autoRefresh ? '🟢 Active' : '⚪ Inactive'}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            Scheduled: {scheduleFrequency}
                          </Typography>
                        </Box>
                      }
                      sx={{ m: 0, width: '100%' }}
                    />

                    {autoRefresh && (
                      <Chip
                        icon={<Clock size={14} />}
                        label={`Next fetch in ${scheduleFrequency}`}
                        size="small"
                        sx={{ 
                          mt: 1.5, 
                          width: '100%',
                          background: 'rgba(59, 130, 246, 0.2)',
                          borderColor: '#3b82f6',
                          color: '#fff',
                          animation: 'pulse 2s infinite',
                          '@keyframes pulse': {
                            '0%, 100%': { opacity: 1 },
                            '50%': { opacity: 0.7 },
                          }
                        }}
                        variant="outlined"
                      />
                    )}
                  </Box>
                )}

                {/* Real-Time Mode Info */}
                {processingMode === 'realtime' && selectedOption && (
                  <Box sx={{ 
                    p: 2, 
                    background: 'rgba(236, 72, 153, 0.1)', 
                    borderRadius: 2,
                    border: '1px solid #ec4899'
                  }}>
                    <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600, color: '#ec4899' }}>
                      ⚡ Real-Time Mode
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ fontSize: '0.875rem' }}>
                      Live processing active. Data updates automatically every 10 seconds.
                    </Typography>
                  </Box>
                )}
              </Box>
            </MotionPaper>
          </Grid>

          {/* Center Panel - Content */}
          <Grid item xs={12} md={6}>
            <AnimatePresence>
              {selectedOptionData && (
                <MotionPaper
                  component={motion.div}
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: 20, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  sx={{
                    p: 3,
                    background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                    border: '1px solid #334155',
                    mb: 3,
                  }}
                >
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                    {selectedOptionData.name}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    {selectedOptionData.description}
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Chip
                        label={`Processing: ${selectedOptionData.processing_stage}`}
                        size="small"
                        sx={{ mb: 1 }}
                      />
                    </Grid>
                    <Grid item xs={6}>
                      <Chip
                        label={`Storage: ${selectedOptionData.storage_type}`}
                        size="small"
                        sx={{ mb: 1 }}
                      />
                    </Grid>
                  </Grid>
                </MotionPaper>
              )}
            </AnimatePresence>

            {/* Analysis Summary - Processing Data */}
            {transactions.length > 0 && (
              <MotionPaper
                component={motion.div}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.3 }}
                sx={{
                  p: 2,
                  background: 'linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(236,72,153,0.1) 100%)',
                  border: '1px solid #334155',
                  borderRadius: 2,
                  mb: 3,
                }}
              >
                <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1.5, color: '#94a3b8' }}>
                  📈 Analysis Summary
                </Typography>

                <Grid container spacing={1} sx={{ fontSize: '0.85rem' }}>
                  <Grid item xs={6}>
                    <Box sx={{ p: 1, background: 'rgba(99,102,241,0.1)', borderRadius: 1 }}>
                      <Typography variant="caption" color="textSecondary">
                        Blocks Analyzed
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: '#6366f1' }}>
                        {blockCount}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={6}>
                    <Box sx={{ p: 1, background: 'rgba(236,72,153,0.1)', borderRadius: 1 }}>
                      <Typography variant="caption" color="textSecondary">
                        Transactions Found
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: '#ec4899' }}>
                        {transactions.length}
                      </Typography>
                    </Box>
                  </Grid>

                  <Grid item xs={12}>
                    <Box sx={{ p: 1, background: 'rgba(16,185,129,0.1)', borderRadius: 1, mt: 0.5 }}>
                      <Typography variant="caption" color="textSecondary">
                        Processing Stage
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600, color: '#10b981' }}>
                        {selectedOptionData?.processing_stage || 'N/A'}
                      </Typography>
                    </Box>
                  </Grid>

                  <Grid item xs={12}>
                    <Box sx={{ p: 1, background: 'rgba(245,158,11,0.1)', borderRadius: 1, mt: 0.5 }}>
                      <Typography variant="caption" color="textSecondary">
                        Storage Type
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600, color: '#f59e0b' }}>
                        {selectedOptionData?.storage_type || 'N/A'}
                      </Typography>
                    </Box>
                  </Grid>

                  <Grid item xs={12}>
                    <Box sx={{ p: 1, background: 'rgba(139,92,246,0.1)', borderRadius: 1, mt: 0.5 }}>
                      <Typography variant="caption" color="textSecondary">
                        ML Model
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 600, color: modelEnabled ? '#8b5cf6' : '#f59e0b' }}>
                        {modelEnabled
                          ? (processingMode === 'scheduled' ? 'Random Forest + Anomaly' : 'Random Forest (Pre-trained)')
                          : 'Disabled (pass-through)'}
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </MotionPaper>
            )}

            {/* Statistics */}
            <Grid container spacing={2} sx={{ mb: 3 }}>
              {stats && [
                {
                  label: 'Total Transactions',
                  value: stats.total_transactions || 0,
                  icon: <TrendingUp size={24} />,
                  color: '#6366f1',
                },
                {
                  label: 'Fraud Detected',
                  value: stats.fraud_count || 0,
                  icon: <AlertTriangle size={24} />,
                  color: '#ef4444',
                },
                {
                  label: 'Avg Value (ETH)',
                  value: (stats.average_value || 0).toFixed(4),
                  icon: <Zap size={24} />,
                  color: '#f59e0b',
                },
                {
                  label: 'Success Rate',
                  value: `${((stats.success_rate || 0) * 100).toFixed(1)}%`,
                  icon: <CheckCircle size={24} />,
                  color: '#10b981',
                },
              ].map((stat, idx) => (
                <Grid item xs={6} key={idx}>
                  <StatCard {...stat} />
                </Grid>
              ))}
            </Grid>

            {/* Transactions Table */}
            <MotionPaper
              component={motion.div}
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.3, delay: 0.1 }}
              sx={{
                background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                border: '1px solid #334155',
                borderRadius: 2,
                overflow: 'hidden',
              }}
            >
              <TransactionTable
                transactions={transactions}
                loading={loading}
                onViewDetails={handleViewDetails}
              />
            </MotionPaper>
          </Grid>

          {/* Right Panel - Details */}
          <Grid item xs={12} md={3}>
            <MotionPaper
              component={motion.div}
              initial={{ x: 20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.5 }}
              sx={{
                p: 2,
                background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
                border: '1px solid #334155',
                minHeight: '600px',
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                📊 AI Model Info
              </Typography>

              <Card
                sx={{
                  background: '#0f172a',
                  border: '1px solid #334155',
                  mb: 2,
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Status
                    </Typography>
                    <FormControlLabel
                      control={
                        <Switch
                          checked={modelEnabled}
                          onChange={(e) => toggleModel(e.target.checked)}
                          sx={{
                            '& .MuiSwitch-switchBase.Mui-checked': {
                              color: '#3b82f6',
                            },
                            '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
                              backgroundColor: '#3b82f6',
                            },
                          }}
                        />
                      }
                      label={modelEnabled ? 'AI On' : 'AI Off'}
                      labelPlacement="start"
                      sx={{ m: 0 }}
                    />
                  </Box>

                  <Typography variant="body1" sx={{ fontWeight: 600, color: modelEnabled && aiLoaded ? '#10b981' : '#f59e0b' }}>
                    {modelEnabled ? (aiLoaded ? '✓ Loaded' : '⏳ Loading...') : '⚪ Disabled'}
                  </Typography>

                  <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                    Accuracy
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    {modelEnabled ? '94.5%' : 'N/A'}
                  </Typography>

                  <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                    ROC-AUC
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    {modelEnabled ? '0.982' : 'N/A'}
                  </Typography>
                </CardContent>
              </Card>

              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                🎨 Fraud Risk Legend
              </Typography>

              {[
                { level: 'LOW', color: '#10b981', desc: '< 25%' },
                { level: 'MEDIUM', color: '#f59e0b', desc: '25-50%' },
                { level: 'HIGH', color: '#f97316', desc: '50-75%' },
                { level: 'CRITICAL', color: '#ef4444', desc: '> 75%' },
              ].map((item) => (
                <Box key={item.level} sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1.5 }}>
                  <Box
                    sx={{
                      width: 20,
                      height: 20,
                      borderRadius: 1,
                      backgroundColor: item.color,
                      opacity: 0.8,
                    }}
                  />
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>
                      {item.level}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {item.desc}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </MotionPaper>
          </Grid>
        </Grid>
      </Container>

      {/* Detail Modal */}
      <DetailModal
        transaction={selectedTx}
        open={!!selectedTx}
        onClose={() => setSelectedTx(null)}
      />

      {/* Loading Bar Under Header */}
      {loading && (
        <Box
          sx={{
            position: 'fixed',
            top: 64,
            left: 0,
            right: 0,
            zIndex: 100,
            height: 4,
            background: 'linear-gradient(90deg, #6366f1 0%, #ec4899 50%, #6366f1 100%)',
            backgroundSize: '200% 100%',
            animation: 'shimmer 2s infinite',
            '@keyframes shimmer': {
              '0%': { backgroundPosition: '200% 0' },
              '100%': { backgroundPosition: '-200% 0' },
            },
            boxShadow: '0 0 20px rgba(99, 102, 241, 0.5)',
          }}
        />
      )}
    </Box>
  )
}

export default App
