import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material'

interface StatsCardProps {
  title: string
  value: string | number
  subtitle?: string
  color?: string
  progress?: number
}

function StatsCard({ title, value, subtitle, color = 'primary.main', progress }: StatsCardProps) {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {title}
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {progress !== undefined && (
            <Box sx={{ position: 'relative', display: 'inline-flex' }}>
              <CircularProgress
                variant="determinate"
                value={progress}
                size={60}
                thickness={5}
                sx={{ color }}
              />
              <Box
                sx={{
                  top: 0,
                  left: 0,
                  bottom: 0,
                  right: 0,
                  position: 'absolute',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Typography variant="caption" component="div" color="text.secondary">
                  {`${Math.round(progress)}%`}
                </Typography>
              </Box>
            </Box>
          )}
          
          <Box>
            <Typography variant="h4" component="div" sx={{ color, fontWeight: 700 }}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
  )
}

export default StatsCard
