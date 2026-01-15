import React from 'react'
import { Card, CardContent, Box, Typography, Chip } from '@mui/material'
import { motion } from 'framer-motion'
import { ChevronRight } from 'lucide-react'

const MotionCard = motion(Card)

function OptionCard({ option, isSelected, onSelect }) {
  // Handle both old format (badges, pros, cons) and new API format (features, advantages)
  const badges = option.badges || [option.processing_stage, option.storage_type].filter(Boolean)
  const advantages = option.pros || option.advantages || []
  const features = option.cons || option.features || []

  return (
    <MotionCard
      onClick={onSelect}
      component={motion.div}
      whileHover={{ scale: 1.02, y: -3 }}
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
      <CardContent sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Box
            sx={{
              width: 28,
              height: 28,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #6366f1, #ec4899)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '0.75rem',
            }}
          >
            {option.id}
          </Box>
          <Typography variant="subtitle1" sx={{ fontWeight: 600, flex: 1, fontSize: '0.9rem' }}>
            {option.name}
          </Typography>
          {isSelected && (
            <Box sx={{ color: '#6366f1', fontSize: '1.2rem' }}>✓</Box>
          )}
        </Box>

        <Typography variant="caption" color="textSecondary" sx={{ display: 'block', mb: 1, fontSize: '0.75rem' }}>
          {option.description}
        </Typography>

        {badges.length > 0 && (
          <Box sx={{ display: 'flex', gap: 0.5, mb: 1, flexWrap: 'wrap' }}>
            {badges.slice(0, 2).map((badge, idx) => (
              <Chip
                key={idx}
                label={badge}
                size="small"
                sx={{
                  fontSize: '0.65rem',
                  height: 20,
                  background: 'rgba(99, 102, 241, 0.2)',
                  color: '#6366f1',
                }}
              />
            ))}
          </Box>
        )}

        {advantages.length > 0 && (
          <Box sx={{ mb: 1 }}>
            <Typography variant="caption" sx={{ fontWeight: 600, color: '#10b981', fontSize: '0.7rem' }}>
              ✓ Key Benefits
            </Typography>
            {advantages.slice(0, 3).map((item, idx) => (
              <Typography key={idx} variant="caption" sx={{ display: 'block', fontSize: '0.7rem', lineHeight: 1.3 }}>
                {item}
              </Typography>
            ))}
          </Box>
        )}

        {isSelected && (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 0.5,
              mt: 1.5,
              pt: 1,
              borderTop: '1px solid #334155',
              color: '#6366f1',
              fontWeight: 600,
              fontSize: '0.75rem',
            }}
          >
            Selected <ChevronRight size={14} />
          </Box>
        )}
      </CardContent>
    </MotionCard>
  )
}

export default OptionCard
