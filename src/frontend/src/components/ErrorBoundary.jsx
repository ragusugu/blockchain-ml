import React from 'react'
import { Box, Typography, Button } from '@mui/material'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo })
    console.error('ErrorBoundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#0f172a',
            color: '#f1f5f9',
            p: 4,
            textAlign: 'center',
          }}
        >
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 2, color: '#ef4444' }}>
            Something went wrong
          </Typography>
          <Typography variant="body1" sx={{ mb: 3, color: '#94a3b8', maxWidth: 500 }}>
            The dashboard encountered an error. Try refreshing the page.
          </Typography>
          <Typography
            variant="body2"
            sx={{
              mb: 3,
              p: 2,
              background: '#1e293b',
              borderRadius: 1,
              fontFamily: 'monospace',
              fontSize: '0.8rem',
              color: '#f59e0b',
              maxWidth: 600,
              overflow: 'auto',
              textAlign: 'left',
            }}
          >
            {this.state.error?.toString()}
          </Typography>
          <Button
            variant="contained"
            onClick={() => window.location.reload()}
            sx={{
              background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
              fontWeight: 600,
            }}
          >
            Reload Page
          </Button>
        </Box>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
