import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import PlayArrowIcon from '@mui/icons-material/PlayArrow'
import RefreshIcon from '@mui/icons-material/Refresh'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment'
import StatsCard from '../components/StatsCard'
import { getStats, resetStats, getQuestionTypes } from '../services/api'
import type { Stats, QuestionTypeInfo } from '../types'

function Dashboard() {
  const navigate = useNavigate()
  const [stats, setStats] = useState<Stats | null>(null)
  const [questionTypes, setQuestionTypes] = useState<QuestionTypeInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [resetDialogOpen, setResetDialogOpen] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [statsData, typesData] = await Promise.all([
        getStats(),
        getQuestionTypes(),
      ])
      setStats(statsData)
      setQuestionTypes(typesData)
    } catch (err) {
      setError('Failed to load data. Make sure the backend server is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    try {
      await resetStats()
      setResetDialogOpen(false)
      loadData()
    } catch (err) {
      console.error('Failed to reset stats:', err)
    }
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return (
      <Box sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={loadData}>
          Retry
        </Button>
      </Box>
    )
  }

  const bestStreak = stats?.topics.reduce((max, t) => Math.max(max, t.best_streak), 0) || 0

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 700 }}>
          Dashboard
        </Typography>
        <Button
          variant="outlined"
          color="error"
          startIcon={<RefreshIcon />}
          onClick={() => setResetDialogOpen(true)}
        >
          Reset Progress
        </Button>
      </Box>

      {/* Overall Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Overall Accuracy"
            value={`${stats?.overall_accuracy.toFixed(0)}%`}
            progress={stats?.overall_accuracy || 0}
            color={
              (stats?.overall_accuracy || 0) >= 80
                ? '#4CAF50'
                : (stats?.overall_accuracy || 0) >= 60
                ? '#FF9800'
                : '#f44336'
            }
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Total Questions"
            value={stats?.total_questions || 0}
            subtitle="answered"
            color="#2196F3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Correct Answers"
            value={stats?.total_correct || 0}
            subtitle={`of ${stats?.total_questions || 0}`}
            color="#4CAF50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Best Streak"
            value={bestStreak}
            subtitle="in a row"
            color="#FF9800"
          />
        </Grid>
      </Grid>

      {/* Training Modes */}
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
        Training Modes
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {questionTypes.map((type) => {
          const topicStats = stats?.topics.find((t) => t.topic === type.id)
          return (
            <Grid item xs={12} md={4} key={type.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flex: 1 }}>
                  <Typography variant="h6" gutterBottom>
                    {type.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {type.description}
                  </Typography>
                  
                  {topicStats && topicStats.total_attempts > 0 ? (
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <TrendingUpIcon fontSize="small" color="primary" />
                        <Typography variant="body2">
                          {topicStats.accuracy.toFixed(0)}% accuracy
                        </Typography>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <LocalFireDepartmentIcon fontSize="small" color="warning" />
                        <Typography variant="body2">
                          Best: {topicStats.best_streak}
                        </Typography>
                      </Box>
                    </Box>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      Not started yet
                    </Typography>
                  )}
                </CardContent>
                <CardActions>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<PlayArrowIcon />}
                    onClick={() => navigate(`/train/${type.id}`)}
                  >
                    Start Training
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          )
        })}
      </Grid>

      {/* Topic Progress */}
      <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
        Progress by Topic
      </Typography>
      <Grid container spacing={2}>
        {stats?.topics.map((topic) => (
          <Grid item xs={12} md={4} key={topic.topic}>
            <Card>
              <CardContent>
                <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
                  {topic.topic_display}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Questions: {topic.total_attempts}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Difficulty: {topic.current_difficulty}/5
                  </Typography>
                </Box>
                <Box
                  sx={{
                    height: 8,
                    bgcolor: 'rgba(255,255,255,0.1)',
                    borderRadius: 4,
                    overflow: 'hidden',
                  }}
                >
                  <Box
                    sx={{
                      height: '100%',
                      width: `${topic.accuracy}%`,
                      bgcolor:
                        topic.accuracy >= 80
                          ? 'success.main'
                          : topic.accuracy >= 60
                          ? 'warning.main'
                          : 'error.main',
                      borderRadius: 4,
                      transition: 'width 0.3s',
                    }}
                  />
                </Box>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  {topic.accuracy.toFixed(0)}% accuracy
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Reset Dialog */}
      <Dialog open={resetDialogOpen} onClose={() => setResetDialogOpen(false)}>
        <DialogTitle>Reset Progress?</DialogTitle>
        <DialogContent>
          <Typography>
            This will delete all your training history and statistics. This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setResetDialogOpen(false)}>Cancel</Button>
          <Button color="error" variant="contained" onClick={handleReset}>
            Reset
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default Dashboard
