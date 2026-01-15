import React from 'react'
import { Card, CardContent, Box, Typography, Chip } from '@mui/material'
import { motion } from 'framer-motion'
import { ChevronRight } from 'lucide-react'

const MotionCard = motion(Card)

function OptionCard({ option, isSelected, onSelect }) {
  return (
    <MotionCard
      onClick={onSelect}
      component={motion.div}
      whileHover={{ scale: 1.05, y: -5 }}
      whileTap={{ scale: 0.98 }}
      sx={{
        cursor: 'pointer',
        border: isSelected ? '2px solid #6366f1' : '1px solid #334155',
        background: isSelected
          ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(236, 72, 153, 0.15) 100%)'
          : '#0f172a',
        transition: 'all 0.3s ease',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: '-100%',
          width: '100%',
          height: '100%',
          background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
          transition: 'left 0.5s',
        },
        '&:hover::before': {
          left: '100%',
        },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #6366f1, #ec4899)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '0.875rem',
            }}
          >
            {option.id}
          </Box>
          <Typography variant="h6" sx={{ fontWeight: 600, flex: 1 }}>
            {option.name}
          </Typography>
          {isSelected && (
            <Box sx={{ color: '#6366f1', fontSize: '1.5rem' }}>✓</Box>
          )}
        </Box>

        <Typography variant="caption" color="textSecondary" sx={{ display: 'block', mb: 1.5 }}>
          {option.description}
        </Typography>

        <Box sx={{ display: 'flex', gap: 0.5, mb: 1.5, flexWrap: 'wrap' }}>
          {option.badges.map((badge) => (
            <Chip
              key={badge}
              label={badge}
              size="small"
              sx={{
                fontSize: '0.7rem',
                background: 'rgba(99, 102, 241, 0.2)',
                color: '#6366f1',
              }}
            />
          ))}
        </Box>

        <Box sx={{ mb: 1 }}>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#10b981' }}>
            ✓ Advantages
          </Typography>
          {option.pros.map((pro, idx) => (
            <Typography key={idx} variant="caption" sx={{ display: 'block', fontSize: '0.75rem' }}>
              • {pro}
            </Typography>
          ))}
        </Box>

        <Box>
          <Typography variant="caption" sx={{ fontWeight: 600, color: '#ef4444' }}>
            ✗ Limitations
          </Typography>
          {option.cons.map((con, idx) => (
            <Typography key={idx} variant="caption" sx={{ display: 'block', fontSize: '0.75rem' }}>
              • {con}
            </Typography>
          ))}
        </Box>

        {isSelected && (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 0.5,
              mt: 2,
              pt: 1.5,
              borderTop: '1px solid #334155',
              color: '#6366f1',
              fontWeight: 600,
              fontSize: '0.875rem',
            }}
          >
            Option Selected <ChevronRight size={16} />
          </Box>
        )}
      </CardContent>
    </MotionCard>
  )
}

export default OptionCard
