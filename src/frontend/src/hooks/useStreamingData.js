import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'

/**
 * useStreamingData Hook
 * Fetches and manages streaming data from Ankr
 * 
 * Usage:
 * const { streamingStats, systemStatus, loading, error } = useStreamingData()
 */
export const useStreamingData = (pollInterval = 10000) => {
  const [streamingStats, setStreamingStats] = useState(null)
  const [systemStatus, setSystemStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchStreamingData = useCallback(async () => {
    try {
      setLoading(true)

      // Fetch both streaming stats and system status in parallel
      const [statsRes, systemRes] = await Promise.all([
        axios.get('/api/streaming/stats'),
        axios.get('/api/system/status'),
      ])

      setStreamingStats(statsRes.data)
      setSystemStatus(systemRes.data)
      setError(null)
    } catch (err) {
      console.error('Error fetching streaming data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    // Initial fetch
    fetchStreamingData()

    // Poll for updates
    const interval = setInterval(fetchStreamingData, pollInterval)

    return () => clearInterval(interval)
  }, [fetchStreamingData, pollInterval])

  return { streamingStats, systemStatus, loading, error, refetch: fetchStreamingData }
}

/**
 * useStreamingHealth Hook
 * Checks if streaming service is running
 */
export const useStreamingHealth = () => {
  const [health, setHealth] = useState(null)
  const [isHealthy, setIsHealthy] = useState(false)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await axios.get('/api/streaming/health')
        setHealth(res.data)
        setIsHealthy(res.data.status === 'running')
      } catch (err) {
        console.error('Health check failed:', err)
        setIsHealthy(false)
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 15000) // Check every 15 seconds

    return () => clearInterval(interval)
  }, [])

  return { health, isHealthy }
}

export default useStreamingData
