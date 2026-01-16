import React from 'react'
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
  Container,
  Grid,
  Button,
} from '@mui/material'
import { Zap, Wifi, TrendingUp } from 'lucide-react'

function Header({ stats, processingMode, onModeChange }) {
  const gasText =
    stats?.gas_price_display ??
    (typeof stats?.gas_price === 'number'
      ? stats.gas_price.toFixed(8)
      : stats?.gas_price);

  return (
    <AppBar
      position="sticky"
      sx={{
        background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
        boxShadow: '0 8px 32px rgba(99, 102, 241, 0.3)',
        backdropFilter: 'blur(10px)',
      }}
    >
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ fontSize: '2rem' }}>🔗</Box>
          <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: 1 }}>
            BLOCKCHAIN FRAUD DETECTION
          </Typography>
        </Box>

        {/* Mode Switcher */}
        {processingMode && onModeChange && (
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <Button
              variant={processingMode === 'scheduled' ? 'contained' : 'outlined'}
              size="small"
              onClick={() => onModeChange('scheduled')}
              sx={{
                background: processingMode === 'scheduled' ? 'rgba(255,255,255,0.2)' : 'transparent',
                color: '#fff',
                border: '1px solid rgba(255,255,255,0.3)',
                fontWeight: 600,
                fontSize: '0.75rem',
              }}
            >
              📦 Batch
            </Button>
            <Button
              variant={processingMode === 'realtime' ? 'contained' : 'outlined'}
              size="small"
              onClick={() => onModeChange('realtime')}
              sx={{
                background: processingMode === 'realtime' ? 'rgba(255,255,255,0.2)' : 'transparent',
                color: '#fff',
                border: '1px solid rgba(255,255,255,0.3)',
                fontWeight: 600,
                fontSize: '0.75rem',
              }}
            >
              🔄 Real-Time
            </Button>
          </Box>
        )}

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', ml: 'auto' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Wifi size={18} />
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {stats?.latest_block ? `Block: ${stats.latest_block}` : 'Connecting...'}
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Zap size={18} />
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {gasText ? `${gasText} Gwei` : 'Loading...'}
            </Typography>
          </Box>

          <Chip
            label="Live"
            size="small"
            sx={{
              backgroundColor: 'rgba(255, 255, 255, 0.2)',
              animation: 'pulse 2s infinite',
            }}
          />
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header
