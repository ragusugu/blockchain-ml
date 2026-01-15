import React from 'react'
import {
  Modal,
  Box,
  Typography,
  IconButton,
  Divider,
  Grid,
  Chip,
  Fade,
} from '@mui/material'
import { X } from 'lucide-react'
import { motion } from 'framer-motion'

const MotionBox = motion(Box)

function DetailModal({ transaction, open, onClose }) {
  if (!transaction) return null

  const getFraudRiskColor = (risk) => {
    switch (risk.toUpperCase()) {
      case 'LOW':
        return '#10b981'
      case 'MEDIUM':
        return '#f59e0b'
      case 'HIGH':
        return '#f97316'
      case 'CRITICAL':
        return '#ef4444'
      default:
        return '#cbd5e1'
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      closeAfterTransition
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Fade in={open}>
        <MotionBox
          component={motion.div}
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          sx={{
            background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
            border: '1px solid #334155',
            borderRadius: 2,
            p: 4,
            maxWidth: 600,
            width: '90%',
            maxHeight: '90vh',
            overflowY: 'auto',
            position: 'relative',
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" sx={{ fontWeight: 700 }}>
              Transaction Details
            </Typography>
            <IconButton
              onClick={onClose}
              sx={{
                color: '#ef4444',
                '&:hover': {
                  background: 'rgba(239, 68, 68, 0.1)',
                },
              }}
            >
              <X size={24} />
            </IconButton>
          </Box>

          <Divider sx={{ mb: 3, borderColor: '#334155' }} />

          <Grid container spacing={2}>
            {[
              { label: 'Transaction Hash', value: transaction.hash, mono: true },
              { label: 'Block Number', value: transaction.block_number },
              { label: 'From Address', value: transaction.from_address, mono: true },
              { label: 'To Address', value: transaction.to_address || '-', mono: true },
              { label: 'Value (ETH)', value: parseFloat(transaction.value).toFixed(4) },
              {
                label: 'Gas Used',
                value: transaction.gas_used || 'N/A',
              },
              {
                label: 'Gas Price (Gwei)',
                value: transaction.gas_price ? (transaction.gas_price / 1e9).toFixed(2) : 'N/A',
              },
              { label: 'Status', value: transaction.status },
              {
                label: 'Fraud Risk',
                value: transaction.fraud_risk,
                chip: true,
              },
              {
                label: 'Fraud Score',
                value: `${(transaction.fraud_score * 100).toFixed(1)}%`,
              },
              {
                label: 'Timestamp',
                value: new Date(transaction.timestamp * 1000).toLocaleString(),
              },
              {
                label: 'Method',
                value: transaction.method || 'N/A',
              },
            ].map((item, idx) => (
              <Grid item xs={12} key={idx}>
                <Box
                  sx={{
                    p: 2,
                    background: 'rgba(99, 102, 241, 0.05)',
                    border: '1px solid #334155',
                    borderRadius: 1,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: 600,
                      color: '#cbd5e1',
                    }}
                  >
                    {item.label}
                  </Typography>
                  {item.chip ? (
                    <Chip
                      label={item.value}
                      sx={{
                        background: `${getFraudRiskColor(item.value)}20`,
                        color: getFraudRiskColor(item.value),
                        fontWeight: 600,
                      }}
                    />
                  ) : (
                    <Typography
                      variant="body2"
                      sx={{
                        fontFamily: item.mono ? 'monospace' : 'inherit',
                        fontSize: item.mono ? '0.8rem' : 'inherit',
                        color: item.mono ? '#6366f1' : '#f1f5f9',
                        fontWeight: 600,
                        textAlign: 'right',
                        maxWidth: '60%',
                        wordBreak: 'break-all',
                      }}
                    >
                      {item.value}
                    </Typography>
                  )}
                </Box>
              </Grid>
            ))}
          </Grid>

          <Divider sx={{ my: 3, borderColor: '#334155' }} />

          <Box
            sx={{
              p: 2,
              background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%)',
              borderRadius: 1,
              border: '1px solid #334155',
            }}
          >
            <Typography variant="body2" color="textSecondary">
              💡 Tip: Click the View button on any transaction to see full details like this.
            </Typography>
          </Box>
        </MotionBox>
      </Fade>
    </Modal>
  )
}

export default DetailModal
