import { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Grid,
} from '@mui/material'
import PokerHand from '../components/PokerHand'
import { getHandRankings, getStartingHands } from '../services/api'
import type { HandRanking, StartingHand, HandCategory, Card } from '../types'

// Helper to parse example cards string into Card objects
function parseExampleCards(example: string): Card[] {
  const parts = example.split(', ')
  return parts.map((notation) => {
    const rank = notation.slice(0, -1)
    const suit = notation.slice(-1)
    const suitSymbols: Record<string, string> = {
      h: '♥', d: '♦', c: '♣', s: '♠',
    }
    return {
      rank,
      suit,
      display: `${rank}${suitSymbols[suit] || suit}`,
      notation,
    }
  })
}

function Reference() {
  const [tab, setTab] = useState(0)
  const [rankings, setRankings] = useState<HandRanking[]>([])
  const [startingHands, setStartingHands] = useState<StartingHand[]>([])
  const [categories, setCategories] = useState<HandCategory[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [rankingsData, handsData] = await Promise.all([
        getHandRankings(),
        getStartingHands(),
      ])
      setRankings(rankingsData)
      setStartingHands(handsData.hands)
      setCategories(handsData.categories)
    } catch (err) {
      setError('Failed to load reference data. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
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
      <Alert severity="error">{error}</Alert>
    )
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" sx={{ mb: 3, fontWeight: 700 }}>
        Reference
      </Typography>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tab}
          onChange={(_, newValue) => setTab(newValue)}
          centered
        >
          <Tab label="Hand Rankings" />
          <Tab label="Starting Hands" />
        </Tabs>
      </Paper>

      {/* Hand Rankings Tab */}
      {tab === 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Rank</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Example</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rankings.map((ranking) => (
                <TableRow key={ranking.rank}>
                  <TableCell>
                    <Chip
                      label={`#${11 - ranking.rank}`}
                      color={ranking.rank >= 9 ? 'success' : ranking.rank >= 6 ? 'warning' : 'default'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                      {ranking.name}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="text.secondary">
                      {ranking.description}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <PokerHand
                      cards={parseExampleCards(ranking.example)}
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Starting Hands Tab */}
      {tab === 1 && (
        <Box>
          {/* Category Legend */}
          <Paper sx={{ p: 2, mb: 3 }}>
            <Typography variant="subtitle1" sx={{ mb: 1, fontWeight: 600 }}>
              Hand Categories
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              {categories.map((cat) => (
                <Box key={cat.value} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Box
                    sx={{
                      width: 16,
                      height: 16,
                      borderRadius: 1,
                      bgcolor: cat.color,
                    }}
                  />
                  <Typography variant="body2">
                    <strong>{cat.name}:</strong> {cat.description}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Paper>

          {/* Hands Grid by Category */}
          {categories
            .filter((cat) => cat.value > 0)
            .map((category) => {
              const handsInCategory = startingHands.filter(
                (h) => h.category === category.value
              )
              if (handsInCategory.length === 0) return null

              return (
                <Paper key={category.value} sx={{ p: 2, mb: 2 }}>
                  <Typography
                    variant="h6"
                    sx={{
                      mb: 2,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                    }}
                  >
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        borderRadius: '50%',
                        bgcolor: category.color,
                      }}
                    />
                    {category.name} Hands
                  </Typography>
                  <Grid container spacing={1}>
                    {handsInCategory.map((hand) => (
                      <Grid item key={hand.notation}>
                        <Chip
                          label={hand.notation}
                          sx={{
                            bgcolor: `${category.color}20`,
                            borderColor: category.color,
                            fontWeight: 600,
                          }}
                          variant="outlined"
                        />
                      </Grid>
                    ))}
                  </Grid>
                </Paper>
              )
            })}
        </Box>
      )}
    </Box>
  )
}

export default Reference
