import React from 'react'
import { Card, CardContent, Box, Typography } from '@mui/material'
import { motion } from 'framer-motion'

const MotionCard = motion(Card)

function StatCard({ label, value, icon, color }) {
  return (
    <MotionCard
      component={motion.div}
      whileHover={{ scale: 1.05, y: -5 }}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      sx={{
        background: `linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(${
          color === '#6366f1'
            ? '99, 102, 241'
            : color === '#ef4444'
              ? '239, 68, 68'
              : color === '#f59e0b'
                ? '245, 158, 11'
                : '16, 185, 129'
        }, 0.05) 100%)`,
        border: `1px solid ${color}40`,
        cursor: 'pointer',
      }}
    >
      <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Box
          sx={{
            p: 1.5,
            borderRadius: 2,
            background: `${color}20`,
            color: color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {icon}
        </Box>

        <Box>
          <Typography variant="caption" color="textSecondary" sx={{ display: 'block' }}>
            {label}
          </Typography>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              color: color,
              fontSize: '1.75rem',
            }}
          >
            {value}
          </Typography>
        </Box>
      </CardContent>
    </MotionCard>
  )
}

export default StatCard
