import React from 'react'
import {
  Box,
  Typography,
  IconButton,
  Divider,
  Grid,
  Chip,
  Paper,
  Drawer,
} from '@mui/material'
import { X, Copy, ExternalLink } from 'lucide-react'
import { motion } from 'framer-motion'

const MotionBox = motion(Box)

function TransactionDetailsPanel({ transaction, open, onClose }) {
  if (!transaction) return null

  const getFraudRiskColor = (risk) => {
    switch (risk?.toUpperCase()) {
      case 'LOW':
        return '#10b981'
      case 'MEDIUM':
        return '#f59e0b'
      case 'HIGH':
        return '#f97316'
      case 'CRITICAL':
        return '#ef4444'
      case 'MODEL-OFF':
        return '#94a3b8'
      default:
        return '#cbd5e1'
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      PaperProps={{
        sx: {
          width: { xs: '100%', sm: 400 },
          background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
          border: '1px solid #334155',
        },
      }}
    >
      <MotionBox
        component={motion.div}
        initial={{ x: 20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 20, opacity: 0 }}
        sx={{ p: 3, height: '100%', overflow: 'auto' }}
      >
        {/* Header */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            📋 Transaction Details
          </Typography>
          <IconButton size="small" onClick={onClose} sx={{ color: '#cbd5e1' }}>
            <X size={20} />
          </IconButton>
        </Box>

        <Divider sx={{ borderColor: '#334155', mb: 3 }} />

        {/* Transaction Hash */}
        <Paper
          sx={{
            background: 'rgba(99, 102, 241, 0.1)',
            border: '1px solid #334155',
            p: 2,
            mb: 2.5,
            borderRadius: 1,
          }}
        >
          <Typography variant="caption" color="textSecondary" sx={{ display: 'block', mb: 1 }}>
            Transaction Hash
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <Typography
              variant="body2"
              sx={{
                fontFamily: 'monospace',
                fontSize: '0.75rem',
                color: '#6366f1',
                fontWeight: 600,
                wordBreak: 'break-all',
              }}
            >
              {transaction.hash?.substring(0, 20)}...
            </Typography>
            <IconButton
              size="small"
              onClick={() => copyToClipboard(transaction.hash)}
              sx={{ color: '#6366f1' }}
            >
              <Copy size={14} />
            </IconButton>
          </Box>
        </Paper>

        {/* Main Details Grid */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={6}>
            <Typography variant="caption" color="textSecondary">
              Block Number
            </Typography>
            <Typography variant="body2" sx={{ fontWeight: 600, color: '#cbd5e1' }}>
              {transaction.block_number || 'N/A'}
            </Typography>
          </Grid>

          <Grid item xs={6}>
            <Typography variant="caption" color="textSecondary">
              Value (ETH)
            </Typography>
            <Typography variant="body2" sx={{ fontWeight: 600, color: '#f59e0b' }}>
              {transaction.value ? parseFloat(transaction.value).toFixed(4) : '0'}
            </Typography>
          </Grid>

          <Grid item xs={6}>
            <Typography variant="caption" color="textSecondary">
              Gas Used
            </Typography>
            <Typography variant="body2" sx={{ fontWeight: 600, color: '#cbd5e1' }}>
              {transaction.gas_used || 'N/A'}
            </Typography>
          </Grid>

          <Grid item xs={6}>
            <Typography variant="caption" color="textSecondary">
              Status
            </Typography>
            <Chip
              label={transaction.status}
              size="small"
              sx={{
                background:
                  transaction.status === 'success'
                    ? 'rgba(16, 185, 129, 0.2)'
                    : 'rgba(239, 68, 68, 0.2)',
                color: transaction.status === 'success' ? '#10b981' : '#ef4444',
                fontWeight: 600,
              }}
            />
          </Grid>
        </Grid>

        <Divider sx={{ borderColor: '#334155', mb: 2.5 }} />

        {/* Fraud Detection */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1.5 }}>
            🔍 Fraud Detection
          </Typography>

          <Box sx={{ p: 2, background: 'rgba(0, 0, 0, 0.3)', borderRadius: 1, mb: 1.5 }}>
            <Typography variant="caption" color="textSecondary">
              Risk Level
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mt: 0.8 }}>
              <Chip
                label={transaction.fraud_risk || 'UNKNOWN'}
                size="small"
                sx={{
                  background: `${getFraudRiskColor(transaction.fraud_risk)}22`,
                  color: getFraudRiskColor(transaction.fraud_risk),
                  fontWeight: 700,
                  fontSize: '0.85rem',
                }}
              />
              {transaction.fraud_probability !== undefined && (
                <Typography
                  variant="body2"
                  sx={{
                    color: getFraudRiskColor(transaction.fraud_risk),
                    fontWeight: 600,
                  }}
                >
                  {(parseFloat(transaction.fraud_probability) * 100).toFixed(1)}%
                </Typography>
              )}
            </Box>
          </Box>
        </Box>

        <Divider sx={{ borderColor: '#334155', mb: 2.5 }} />

        {/* Address Information */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1.5 }}>
            👤 Address Information
          </Typography>

          <Box sx={{ mb: 1.5 }}>
            <Typography variant="caption" color="textSecondary">
              From
            </Typography>
            <Box
              sx={{
                p: 1,
                background: 'rgba(99, 102, 241, 0.1)',
                borderRadius: 1,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mt: 0.5,
              }}
            >
              <Typography
                variant="body2"
                sx={{
                  fontFamily: 'monospace',
                  fontSize: '0.75rem',
                  color: '#6366f1',
                  wordBreak: 'break-all',
                }}
              >
                {transaction.from_address?.substring(0, 16)}...
              </Typography>
              <IconButton
                size="small"
                onClick={() => copyToClipboard(transaction.from_address)}
                sx={{ color: '#6366f1' }}
              >
                <Copy size={14} />
              </IconButton>
            </Box>
          </Box>

          <Box sx={{ mb: 1.5 }}>
            <Typography variant="caption" color="textSecondary">
              To
            </Typography>
            <Box
              sx={{
                p: 1,
                background: 'rgba(236, 72, 153, 0.1)',
                borderRadius: 1,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mt: 0.5,
              }}
            >
              <Typography
                variant="body2"
                sx={{
                  fontFamily: 'monospace',
                  fontSize: '0.75rem',
                  color: '#ec4899',
                  wordBreak: 'break-all',
                }}
              >
                {transaction.to_address?.substring(0, 16) || 'Contract Creation'}...
              </Typography>
              {transaction.to_address && (
                <IconButton
                  size="small"
                  onClick={() => copyToClipboard(transaction.to_address)}
                  sx={{ color: '#ec4899' }}
                >
                  <Copy size={14} />
                </IconButton>
              )}
            </Box>
          </Box>
        </Box>

        <Divider sx={{ borderColor: '#334155', mb: 2.5 }} />

        {/* Footer Note */}
        <Box sx={{ p: 1.5, background: 'rgba(139, 92, 246, 0.1)', borderRadius: 1 }}>
          <Typography variant="caption" color="textSecondary">
            💡 Click copy icon to copy address to clipboard. All data is from the latest block scan.
          </Typography>
        </Box>
      </MotionBox>
    </Drawer>
  )
}

export default TransactionDetailsPanel
