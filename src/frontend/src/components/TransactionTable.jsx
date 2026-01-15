import React from 'react'
import {
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Chip,
  Button,
  Box,
  Typography,
  Skeleton,
} from '@mui/material'
import { Eye } from 'lucide-react'

function TransactionTable({ transactions, loading, onViewDetails }) {
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

  const getFraudRiskBg = (risk) => {
    switch (risk.toUpperCase()) {
      case 'LOW':
        return 'rgba(16, 185, 129, 0.15)'
      case 'MEDIUM':
        return 'rgba(245, 158, 11, 0.15)'
      case 'HIGH':
        return 'rgba(249, 115, 22, 0.15)'
      case 'CRITICAL':
        return 'rgba(239, 68, 68, 0.15)'
      default:
        return 'transparent'
    }
  }

  if (!transactions || transactions.length === 0) {
    return (
      <Box sx={{ p: 4, textAlign: 'center' }}>
        <Typography color="textSecondary">
          No transactions loaded. Select an option and click "Fetch & Analyze"
        </Typography>
      </Box>
    )
  }

  return (
    <TableContainer>
      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow
            sx={{
              background: 'linear-gradient(135deg, #334155 0%, #1e293b 100%)',
              '& th': {
                fontWeight: 700,
                color: '#6366f1',
              },
            }}
          >
            <TableCell>Block</TableCell>
            <TableCell>From</TableCell>
            <TableCell>To</TableCell>
            <TableCell align="right">Value (ETH)</TableCell>
            <TableCell align="right">Gas</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Fraud Risk</TableCell>
            <TableCell align="center">Action</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {loading
            ? Array.from({ length: 5 }).map((_, idx) => (
                <TableRow key={idx}>
                  {Array.from({ length: 8 }).map((_, cidx) => (
                    <TableCell key={cidx}>
                      <Skeleton width="80%" />
                    </TableCell>
                  ))}
                </TableRow>
              ))
            : transactions.map((tx, idx) => (
                <TableRow
                  key={idx}
                  hover
                  sx={{
                    '&:hover': {
                      background: 'rgba(99, 102, 241, 0.1)',
                    },
                    borderBottom: '1px solid #334155',
                  }}
                >
                  <TableCell sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                    {tx.block_number}
                  </TableCell>
                  <TableCell
                    sx={{
                      fontFamily: 'monospace',
                      fontSize: '0.8rem',
                      color: '#6366f1',
                    }}
                  >
                    {tx.from_address.substring(0, 10)}...
                  </TableCell>
                  <TableCell
                    sx={{
                      fontFamily: 'monospace',
                      fontSize: '0.8rem',
                      color: '#6366f1',
                    }}
                  >
                    {tx.to_address ? tx.to_address.substring(0, 10) + '...' : '-'}
                  </TableCell>
                  <TableCell align="right" sx={{ fontWeight: 600 }}>
                    {tx.value ? parseFloat(tx.value).toFixed(4) : '0'}
                  </TableCell>
                  <TableCell align="right" sx={{ fontSize: '0.85rem' }}>
                    {tx.gas_used || 'N/A'}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={tx.status}
                      size="small"
                      sx={{
                        background:
                          tx.status === 'success'
                            ? 'rgba(16, 185, 129, 0.2)'
                            : 'rgba(239, 68, 68, 0.2)',
                        color: tx.status === 'success' ? '#10b981' : '#ef4444',
                        fontWeight: 600,
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={tx.fraud_risk}
                      size="small"
                      sx={{
                        background: getFraudRiskBg(tx.fraud_risk),
                        color: getFraudRiskColor(tx.fraud_risk),
                        fontWeight: 600,
                      }}
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Button
                      size="small"
                      variant="contained"
                      startIcon={<Eye size={16} />}
                      onClick={() => onViewDetails(tx.hash)}
                      sx={{
                        background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                        textTransform: 'none',
                        fontWeight: 600,
                      }}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export default TransactionTable
