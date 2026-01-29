import { Box, Button } from '@mui/material'

interface ActionButtonsProps {
  choices: string[]
  onSelect: (choice: string) => void
  disabled?: boolean
  selectedAnswer?: string
  correctAnswer?: string
}

function ActionButtons({
  choices,
  onSelect,
  disabled = false,
  selectedAnswer,
  correctAnswer,
}: ActionButtonsProps) {
  const getButtonColor = (choice: string) => {
    if (!selectedAnswer) return 'primary'
    if (choice === correctAnswer) return 'success'
    if (choice === selectedAnswer && choice !== correctAnswer) return 'error'
    return 'primary'
  }

  const getButtonVariant = (choice: string) => {
    if (!selectedAnswer) return 'outlined'
    if (choice === correctAnswer || choice === selectedAnswer) return 'contained'
    return 'outlined'
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: 2,
        justifyContent: 'center',
        mt: 3,
      }}
    >
      {choices.map((choice) => (
        <Button
          key={choice}
          variant={getButtonVariant(choice)}
          color={getButtonColor(choice)}
          onClick={() => onSelect(choice)}
          disabled={disabled}
          sx={{
            minWidth: 120,
            py: 1.5,
            fontSize: '1rem',
          }}
        >
          {choice}
        </Button>
      ))}
    </Box>
  )
}

export default ActionButtons
