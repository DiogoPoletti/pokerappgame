import { Box, Typography } from '@mui/material'
import PlayingCard from './PlayingCard'
import type { Card } from '../types'

interface PokerHandProps {
  cards: Card[]
  label?: string
  size?: 'small' | 'medium' | 'large'
  highlighted?: boolean
}

function PokerHand({ cards, label, size = 'medium', highlighted = false }: PokerHandProps) {
  // Calculate overlap based on size
  const overlaps = {
    small: -15,
    medium: -20,
    large: -25,
  }
  const overlap = overlaps[size]

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        p: 2,
        borderRadius: 2,
        bgcolor: highlighted ? 'rgba(76, 175, 80, 0.1)' : 'transparent',
        border: highlighted ? '2px solid #4CAF50' : '2px solid transparent',
        transition: 'all 0.2s',
      }}
    >
      {label && (
        <Typography
          variant="subtitle1"
          sx={{ mb: 1, fontWeight: 600, color: 'text.secondary' }}
        >
          {label}
        </Typography>
      )}
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
        }}
      >
        {cards.map((card, index) => (
          <Box
            key={`${card.notation}-${index}`}
            sx={{
              marginLeft: index === 0 ? 0 : `${overlap}px`,
              zIndex: index,
            }}
          >
            <PlayingCard card={card} size={size} />
          </Box>
        ))}
      </Box>
    </Box>
  )
}

export default PokerHand
