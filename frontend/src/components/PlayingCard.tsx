import { Box, Typography } from '@mui/material'
import type { Card } from '../types'

interface PlayingCardProps {
  card: Card
  size?: 'small' | 'medium' | 'large'
}

const suitColors: Record<string, string> = {
  h: '#e53935', // hearts - red
  d: '#e53935', // diamonds - red
  c: '#212121', // clubs - black
  s: '#212121', // spades - black
}

const suitSymbols: Record<string, string> = {
  h: '♥',
  d: '♦',
  c: '♣',
  s: '♠',
}

const sizes = {
  small: { width: 50, height: 70, fontSize: '1rem', suitSize: '1.2rem' },
  medium: { width: 70, height: 100, fontSize: '1.3rem', suitSize: '1.6rem' },
  large: { width: 90, height: 130, fontSize: '1.6rem', suitSize: '2rem' },
}

function PlayingCard({ card, size = 'medium' }: PlayingCardProps) {
  const { width, height, fontSize, suitSize } = sizes[size]
  const color = suitColors[card.suit]
  const symbol = suitSymbols[card.suit]

  return (
    <Box
      sx={{
        width,
        height,
        bgcolor: '#fff',
        borderRadius: 2,
        boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        border: '1px solid #ddd',
        transition: 'transform 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
        },
      }}
    >
      {/* Top left corner */}
      <Box
        sx={{
          position: 'absolute',
          top: 4,
          left: 6,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography
          sx={{
            color,
            fontWeight: 700,
            fontSize,
            lineHeight: 1,
          }}
        >
          {card.rank}
        </Typography>
        <Typography sx={{ color, fontSize: suitSize, lineHeight: 1 }}>
          {symbol}
        </Typography>
      </Box>

      {/* Center suit */}
      <Typography
        sx={{
          color,
          fontSize: `calc(${suitSize} * 1.5)`,
        }}
      >
        {symbol}
      </Typography>

      {/* Bottom right corner (rotated) */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 4,
          right: 6,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          transform: 'rotate(180deg)',
        }}
      >
        <Typography
          sx={{
            color,
            fontWeight: 700,
            fontSize,
            lineHeight: 1,
          }}
        >
          {card.rank}
        </Typography>
        <Typography sx={{ color, fontSize: suitSize, lineHeight: 1 }}>
          {symbol}
        </Typography>
      </Box>
    </Box>
  )
}

export default PlayingCard
