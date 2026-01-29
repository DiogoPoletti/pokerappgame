import { Box, Typography, LinearProgress, Chip, Stack } from '@mui/material'
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'

interface ProgressIndicatorProps {
  streak: number
  accuracy: number
  difficulty: number
  questionsAnswered?: number
}

function ProgressIndicator({
  streak,
  accuracy,
  difficulty,
  questionsAnswered = 0,
}: ProgressIndicatorProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        p: 2,
        bgcolor: 'background.paper',
        borderRadius: 2,
      }}
    >
      <Stack direction="row" spacing={2} justifyContent="center">
        <Chip
          icon={<LocalFireDepartmentIcon />}
          label={`Streak: ${streak}`}
          color={streak >= 5 ? 'success' : 'default'}
          variant={streak >= 3 ? 'filled' : 'outlined'}
        />
        <Chip
          icon={<TrendingUpIcon />}
          label={`Accuracy: ${accuracy.toFixed(0)}%`}
          color={accuracy >= 80 ? 'success' : accuracy >= 60 ? 'warning' : 'error'}
          variant="filled"
        />
        <Chip
          label={`Difficulty: ${difficulty}/5`}
          color="primary"
          variant="outlined"
        />
      </Stack>

      {questionsAnswered > 0 && (
        <Box>
          <Typography variant="caption" color="text.secondary">
            Questions this session: {questionsAnswered}
          </Typography>
          <LinearProgress
            variant="determinate"
            value={Math.min((questionsAnswered / 20) * 100, 100)}
            sx={{ mt: 0.5, height: 6, borderRadius: 3 }}
          />
        </Box>
      )}
    </Box>
  )
}

export default ProgressIndicator
