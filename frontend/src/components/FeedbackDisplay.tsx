import { Box, Typography, Paper, Grow } from '@mui/material'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import CancelIcon from '@mui/icons-material/Cancel'

interface FeedbackDisplayProps {
  show: boolean
  correct: boolean
  correctAnswer: string
  explanation: string
}

function FeedbackDisplay({
  show,
  correct,
  correctAnswer,
  explanation,
}: FeedbackDisplayProps) {
  if (!show) return null

  return (
    <Grow in={show}>
      <Paper
        sx={{
          p: 3,
          mt: 3,
          bgcolor: correct ? 'rgba(76, 175, 80, 0.1)' : 'rgba(244, 67, 54, 0.1)',
          border: `2px solid ${correct ? '#4CAF50' : '#f44336'}`,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          {correct ? (
            <CheckCircleIcon sx={{ color: 'success.main', fontSize: 32 }} />
          ) : (
            <CancelIcon sx={{ color: 'error.main', fontSize: 32 }} />
          )}
          <Typography variant="h5" sx={{ fontWeight: 700 }}>
            {correct ? 'Correct!' : 'Incorrect'}
          </Typography>
        </Box>

        {!correct && (
          <Typography variant="body1" sx={{ mb: 1 }}>
            The correct answer was: <strong>{correctAnswer}</strong>
          </Typography>
        )}

        <Typography variant="body1" color="text.secondary">
          {explanation}
        </Typography>
      </Paper>
    </Grow>
  )
}

export default FeedbackDisplay
