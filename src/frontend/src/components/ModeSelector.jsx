import React from 'react'
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Paper,
  Divider,
} from '@mui/material'
import {
  Clock,
  Zap,
  Database,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
} from 'lucide-react'
import { motion } from 'framer-motion'

const MotionCard = motion(Card)

function ModeSelector({ onSelectMode }) {
  const modes = [
    {
      id: 'scheduled',
      title: '⏰ Scheduled Processing',
      icon: Clock,
      subtitle: 'Batch Processing Mode',
      description: 'Process blockchain data in scheduled batches',
      features: [
        'Process data periodically (hourly/daily)',
        'Train ML models on accumulated data',
        'Store full history in PostgreSQL',
        'Comprehensive analysis & reporting',
        'Lower infrastructure cost',
        'Best for historical analysis',
      ],
      benefits: [
        {
          icon: Database,
          label: 'Full Data Storage',
          desc: 'All transactions stored in DB',
        },
        {
          icon: TrendingUp,
          label: 'Model Training',
          desc: 'ML models retrained periodically',
        },
        {
          icon: CheckCircle,
          label: 'Batch Results',
          desc: 'Detailed batch analysis reports',
        },
      ],
      color: '#3b82f6',
      gradient: 'linear-gradient(135deg, #1e40af 0%, #0c4a6e 100%)',
    },
    {
      id: 'realtime',
      title: '⚡ Real-Time Processing',
      icon: Zap,
      subtitle: 'Stream Processing Mode',
      description: 'Detect fraud in real-time as transactions occur',
      features: [
        'Live fraud detection (no delay)',
        'Stream processing of transactions',
        'Instant results in dashboard',
        'ML inference on each transaction',
        'Store results immediately in DB',
        'Best for immediate threat detection',
      ],
      benefits: [
        {
          icon: AlertTriangle,
          label: 'Instant Detection',
          desc: 'Frauds detected immediately',
        },
        {
          icon: Zap,
          label: 'Live Updates',
          desc: 'Dashboard updates in real-time',
        },
        {
          icon: CheckCircle,
          label: 'Immediate Storage',
          desc: 'Results saved to DB instantly',
        },
      ],
      color: '#ec4899',
      gradient: 'linear-gradient(135deg, #be185d 0%, #831843 100%)',
    },
  ]

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
        py: 8,
      }}
    >
      <Container maxWidth="lg">
        {/* Header */}
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Typography
              variant="h2"
              sx={{
                fontWeight: 900,
                background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 2,
              }}
            >
              Blockchain Fraud Detection
            </Typography>
            <Typography
              variant="h5"
              color="textSecondary"
              sx={{ fontWeight: 400, maxWidth: 600, mx: 'auto' }}
            >
              Choose your processing mode to get started with AI-powered fraud detection
            </Typography>
          </motion.div>
        </Box>

        {/* Mode Selection Cards */}
        <Grid container spacing={4} sx={{ mb: 6 }}>
          {modes.map((mode, idx) => {
            const IconComponent = mode.icon
            return (
              <Grid item xs={12} md={6} key={mode.id}>
                <MotionCard
                  component={motion.div}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: idx * 0.2 }}
                  whileHover={{ y: -8, boxShadow: '0 20px 40px rgba(0,0,0,0.3)' }}
                  sx={{
                    height: '100%',
                    background: mode.gradient,
                    border: `2px solid ${mode.color}`,
                    cursor: 'pointer',
                    position: 'relative',
                    overflow: 'hidden',
                    '&::before': {
                      content: '""',
                      position: 'absolute',
                      top: -50,
                      right: -50,
                      width: 200,
                      height: 200,
                      borderRadius: '50%',
                      background: mode.color,
                      opacity: 0.05,
                    },
                  }}
                >
                  <CardContent sx={{ p: 4, position: 'relative', zIndex: 1 }}>
                    {/* Title Section */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                      <Box
                        sx={{
                          width: 50,
                          height: 50,
                          borderRadius: 2,
                          background: mode.color,
                          opacity: 0.15,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <IconComponent size={28} color={mode.color} />
                      </Box>
                      <Box>
                        <Typography
                          variant="h5"
                          sx={{ fontWeight: 700, color: '#fff', mb: 0.5 }}
                        >
                          {mode.title}
                        </Typography>
                        <Typography
                          variant="body2"
                          sx={{ color: mode.color, fontWeight: 600 }}
                        >
                          {mode.subtitle}
                        </Typography>
                      </Box>
                    </Box>

                    <Typography
                      variant="body2"
                      sx={{
                        color: '#cbd5e1',
                        mb: 3,
                        lineHeight: 1.6,
                      }}
                    >
                      {mode.description}
                    </Typography>

                    <Divider sx={{ my: 2, borderColor: 'rgba(255,255,255,0.1)' }} />

                    {/* Features */}
                    <Box sx={{ mb: 3 }}>
                      <Typography
                        variant="subtitle2"
                        sx={{
                          fontWeight: 700,
                          color: '#cbd5e1',
                          mb: 1.5,
                          textTransform: 'uppercase',
                          fontSize: '0.75rem',
                          letterSpacing: 1,
                        }}
                      >
                        Key Features
                      </Typography>
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.8 }}>
                        {mode.features.slice(0, 4).map((feature, i) => (
                          <Box
                            key={i}
                            sx={{
                              display: 'flex',
                              alignItems: 'center',
                              gap: 1,
                              color: '#e2e8f0',
                              fontSize: '0.9rem',
                            }}
                          >
                            <Box
                              sx={{
                                width: 6,
                                height: 6,
                                borderRadius: '50%',
                                background: mode.color,
                                flexShrink: 0,
                              }}
                            />
                            {feature}
                          </Box>
                        ))}
                      </Box>
                    </Box>

                    {/* Benefits Cards */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, mb: 3 }}>
                      {mode.benefits.map((benefit, i) => {
                        const BenefitIcon = benefit.icon
                        return (
                          <Box
                            key={i}
                            sx={{
                              background: 'rgba(255,255,255,0.05)',
                              borderRadius: 1,
                              p: 1.5,
                              display: 'flex',
                              alignItems: 'center',
                              gap: 1.5,
                            }}
                          >
                            <BenefitIcon size={18} color={mode.color} />
                            <Box>
                              <Typography
                                variant="caption"
                                sx={{ fontWeight: 700, color: '#cbd5e1', display: 'block' }}
                              >
                                {benefit.label}
                              </Typography>
                              <Typography
                                variant="caption"
                                sx={{ color: '#94a3b8', fontSize: '0.7rem' }}
                              >
                                {benefit.desc}
                              </Typography>
                            </Box>
                          </Box>
                        )
                      })}
                    </Box>

                    {/* Action Button */}
                    <Button
                      fullWidth
                      variant="contained"
                      onClick={() => onSelectMode(mode.id)}
                      sx={{
                        background: mode.color,
                        color: '#fff',
                        fontWeight: 700,
                        py: 1.5,
                        fontSize: '1rem',
                        borderRadius: 1,
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          background: mode.color,
                          transform: 'scale(1.02)',
                          boxShadow: `0 10px 25px ${mode.color}40`,
                        },
                      }}
                    >
                      Select {mode.id === 'scheduled' ? 'Batch' : 'Stream'} Mode →
                    </Button>
                  </CardContent>
                </MotionCard>
              </Grid>
            )
          })}
        </Grid>

        {/* Comparison Table */}
        <Paper
          sx={{
            p: 4,
            background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
            border: '1px solid #334155',
            borderRadius: 2,
            mt: 6,
          }}
        >
          <Typography
            variant="h6"
            sx={{ fontWeight: 700, mb: 3, color: '#fff' }}
          >
            📊 Mode Comparison
          </Typography>

          <Box
            sx={{
              overflowX: 'auto',
              '& table': {
                width: '100%',
                borderCollapse: 'collapse',
              },
              '& td, & th': {
                padding: '12px 16px',
                borderBottom: '1px solid #334155',
                textAlign: 'left',
              },
              '& th': {
                background: '#0f172a',
                fontWeight: 700,
                color: '#cbd5e1',
                fontSize: '0.9rem',
              },
              '& tr:hover': {
                background: 'rgba(99, 102, 241, 0.05)',
              },
            }}
          >
            <table>
              <thead>
                <tr>
                  <th>Aspect</th>
                  <th>⏰ Scheduled</th>
                  <th>⚡ Real-Time</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Processing Speed</td>
                  <td>Periodic (hourly/daily)</td>
                  <td>Instant (&lt;100ms)</td>
                </tr>
                <tr>
                  <td>ML Training</td>
                  <td>Regular retraining</td>
                  <td>Inference only</td>
                </tr>
                <tr>
                  <td>Database</td>
                  <td>Full history + models</td>
                  <td>Results only</td>
                </tr>
                <tr>
                  <td>Use Case</td>
                  <td>Historical analysis</td>
                  <td>Live threat detection</td>
                </tr>
                <tr>
                  <td>Cost</td>
                  <td>Low</td>
                  <td>Medium-High</td>
                </tr>
                <tr>
                  <td>Best For</td>
                  <td>Compliance, reporting</td>
                  <td>Active monitoring</td>
                </tr>
              </tbody>
            </table>
          </Box>
        </Paper>
      </Container>
    </Box>
  )
}

export default ModeSelector
