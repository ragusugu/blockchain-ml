import React from 'react'
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
  Container,
  Grid,
} from '@mui/material'
import { Zap, Wifi, TrendingUp } from 'lucide-react'

function Header({ stats }) {
  return (
    <AppBar
      position="sticky"
      sx={{
        background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
        boxShadow: '0 8px 32px rgba(99, 102, 241, 0.3)',
        backdropFilter: 'blur(10px)',
      }}
    >
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mr: 'auto' }}>
          <Box sx={{ fontSize: '2rem' }}>🔗</Box>
          <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: 1 }}>
            BLOCKCHAIN FRAUD DETECTION
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Wifi size={18} />
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {stats?.latest_block ? `Block: ${stats.latest_block}` : 'Connecting...'}
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Zap size={18} />
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              {stats?.gas_price ? `${stats.gas_price} Gwei` : 'Loading...'}
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
