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

  // Fetch options on mount
  useEffect(() => {
    fetchStats()
  }, [])

  // Auto-refresh logic
  useEffect(() => {
    if (!autoRefresh || !selectedOption) return
    const interval = setInterval(() => {
      fetchTransactions()
    }, 5000)
    return () => clearInterval(interval)
  }, [autoRefresh, selectedOption])

  const fetchOptionsForMode = async (mode) => {
    try {
      const response = await axios.get('/api/options', {
        params: { mode }
      })
      setOptions(response.data.options)
    } catch (err) {
      console.error('Error fetching options:', err)
      setError('Failed to load options for this mode')
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
      setTransactions(response.data.transactions || [])
      setStats(response.data.stats)
    } catch (err) {
      console.error('Error fetching transactions:', err)
      setError('Failed to fetch transactions')
    } finally {
      setLoading(false)
    }
  }

  const handleSelectMode = (mode) => {
    setProcessingMode(mode)
    // Fetch options for the selected mode
    fetchOptionsForMode(mode)
  }

  const fetchOptionsForMode = async (mode) => {
    try {
      const response = await axios.get(`/api/options?mode=${mode}`)
      setOptions(response.data.options)
    } catch (err) {
      console.error('Error fetching options:', err)
      setError('Failed to load options for this mode')
    }
  }

  const handleSelectOption = (optionId) => {
    setSelectedOption(optionId)
  }

  const handleFetch = () => {
    fetchTransactions()
  }

  const handleViewDetails = async (hash) => {
    setLoading(true)
    try {
      {/* Mode Badge & Back Button */}
      <Box
        sx={{
          px: 2,
          py: 1.5,
          background: 'linear-gradient(90deg, #1e293b 0%, #0f172a 100%)',
          borderBottom: '1px solid #334155',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip
            label={`Mode: ${processingMode === 'scheduled' ? '⏰ Scheduled Processing' : '⚡ Real-Time Processing'}`}
            variant="outlined"
            sx={{
              borderColor: processingMode === 'scheduled' ? '#3b82f6' : '#ec4899',
              color: processingMode === 'scheduled' ? '#3b82f6' : '#ec4899',
              fontWeight: 600,
            }}
          />
          <Typography variant="caption" color="textSecondary">
            {processingMode === 'scheduled'
              ? 'Batch processing with ML training and full database storage'
              : 'Real-time fraud detection with instant results'}
          </Typography>
        </Box>
        <Button
          size="small"
          onClick={handleBackToMode}
          sx={{ color: '#94a3b8' }}
        >
          ← Change Mode
        </Button>
      </Box>

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
                    mb: 1,
                    py: 1.5,
                    fontWeight: 600,
                  }}
                >
                  {loading ? <CircularProgress size={20} /> : '🔄 Fetch & Analyze'}
                </Button>

                <FormControlLabel
                  control={
                    <Switch
                      checked={autoRefresh}
                      onChange={(e) => setAutoRefresh(e.target.checked)}
                      disabled={!selectedOption}
                    />
                  }
                  label="Auto-Refresh (5s)"
                  sx={{ mt: 1 }}
                />
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
                  <Typography variant="subtitle2" color="textSecondary">
                    Status
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600, color: '#10b981' }}>
                    ✓ Loaded
                  </Typography>

                  <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                    Accuracy
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    94.5%
                  </Typography>

                  <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
                    ROC-AUC
                  </Typography>
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    0.982
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

      {/* Loading Overlay */}
      {loading && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            backdropFilter: 'blur(5px)',
          }}
        >
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress
              size={60}
              sx={{
                color: '#6366f1',
                mb: 2,
              }}
            />
            <Typography sx={{ color: '#cbd5e1', fontWeight: 600 }}>
              Analyzing transactions...
            </Typography>
          </Box>
        </Box>
      )}
    </Box>
  )
}

export default App
