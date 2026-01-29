import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Paper,
  ToggleButton,
  ToggleButtonGroup,
} from '@mui/material'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import NavigateNextIcon from '@mui/icons-material/NavigateNext'
import PokerHand from '../components/PokerHand'
import ActionButtons from '../components/ActionButtons'
import ProgressIndicator from '../components/ProgressIndicator'
import FeedbackDisplay from '../components/FeedbackDisplay'
import { getQuestion, submitAnswer, getQuestionTypes } from '../services/api'
import type { Question, AnswerResponse, QuestionTypeInfo, QuestionType } from '../types'

function Training() {
  const { type } = useParams<{ type?: string }>()
  const navigate = useNavigate()
  
  const [questionTypes, setQuestionTypes] = useState<QuestionTypeInfo[]>([])
  const [selectedType, setSelectedType] = useState<QuestionType | null>(null)
  const [question, setQuestion] = useState<Question | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [feedback, setFeedback] = useState<AnswerResponse | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [startTime, setStartTime] = useState<number>(0)
  
  const [streak, setStreak] = useState(0)
  const [accuracy, setAccuracy] = useState(0)
  const [difficulty, setDifficulty] = useState(1)
  const [questionsAnswered, setQuestionsAnswered] = useState(0)

  // Load question types
  useEffect(() => {
    const loadTypes = async () => {
      try {
        const types = await getQuestionTypes()
        setQuestionTypes(types)
        
        // Set initial type from URL or first available
        if (type && types.some(t => t.id === type)) {
          setSelectedType(type as QuestionType)
        } else if (types.length > 0) {
          setSelectedType(types[0].id)
        }
      } catch (err) {
        setError('Failed to load question types')
        console.error(err)
      }
    }
    loadTypes()
  }, [type])

  // Load question when type changes
  const loadQuestion = useCallback(async () => {
    if (!selectedType) return
    
    try {
      setLoading(true)
      setError(null)
      setSelectedAnswer(null)
      setFeedback(null)
      
      const q = await getQuestion(selectedType)
      setQuestion(q)
      setDifficulty(q.difficulty)
      setStartTime(Date.now())
    } catch (err) {
      setError('Failed to load question. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [selectedType])

  useEffect(() => {
    if (selectedType) {
      loadQuestion()
    }
  }, [selectedType, loadQuestion])

  const handleTypeChange = (_: React.MouseEvent<HTMLElement>, newType: QuestionType | null) => {
    if (newType) {
      setSelectedType(newType)
      navigate(`/train/${newType}`, { replace: true })
    }
  }

  const handleAnswer = async (answer: string) => {
    if (!question || submitting || feedback) return
    
    setSelectedAnswer(answer)
    setSubmitting(true)
    
    const responseTime = Date.now() - startTime
    
    try {
      const result = await submitAnswer({
        question_id: question.question_id,
        question_type: question.question_type,
        answer,
        response_time_ms: responseTime,
      })
      
      setFeedback(result)
      setStreak(result.streak)
      setAccuracy(result.accuracy)
      setDifficulty(result.next_difficulty)
      setQuestionsAnswered(prev => prev + 1)
    } catch (err) {
      setError('Failed to submit answer')
      console.error(err)
    } finally {
      setSubmitting(false)
    }
  }

  const handleNext = () => {
    loadQuestion()
  }

  const getCurrentTypeName = () => {
    return questionTypes.find(t => t.id === selectedType)?.name || 'Training'
  }

  if (error) {
    return (
      <Box sx={{ py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={loadQuestion}>
          Retry
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
        >
          Back
        </Button>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 700, flex: 1 }}>
          {getCurrentTypeName()}
        </Typography>
      </Box>

      {/* Type Selector */}
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'center' }}>
        <ToggleButtonGroup
          value={selectedType}
          exclusive
          onChange={handleTypeChange}
          size="small"
        >
          {questionTypes.map((qt) => (
            <ToggleButton key={qt.id} value={qt.id}>
              {qt.name}
            </ToggleButton>
          ))}
        </ToggleButtonGroup>
      </Box>

      {/* Progress */}
      <ProgressIndicator
        streak={streak}
        accuracy={accuracy}
        difficulty={difficulty}
        questionsAnswered={questionsAnswered}
      />

      {/* Question */}
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
          <CircularProgress />
        </Box>
      ) : question ? (
        <Paper sx={{ p: 4, mt: 3, textAlign: 'center' }}>
          <Typography variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
            {question.prompt}
          </Typography>

          {/* Cards Display */}
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              gap: 4,
              flexWrap: 'wrap',
              mb: 2,
            }}
          >
            <PokerHand
              cards={question.cards}
              label={question.cards2 ? 'Hand 1' : undefined}
              size="large"
              highlighted={feedback?.correct_answer === 'Hand 1'}
            />
            {question.cards2 && (
              <PokerHand
                cards={question.cards2}
                label="Hand 2"
                size="large"
                highlighted={feedback?.correct_answer === 'Hand 2'}
              />
            )}
          </Box>

          {/* Context info */}
          {question.context && (
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Position: {question.context}
            </Typography>
          )}

          {/* Answer Buttons */}
          <ActionButtons
            choices={question.choices}
            onSelect={handleAnswer}
            disabled={submitting || !!feedback}
            selectedAnswer={selectedAnswer || undefined}
            correctAnswer={feedback?.correct_answer}
          />

          {/* Feedback */}
          <FeedbackDisplay
            show={!!feedback}
            correct={feedback?.correct || false}
            correctAnswer={feedback?.correct_answer || ''}
            explanation={feedback?.explanation || ''}
          />

          {/* Next Button */}
          {feedback && (
            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                size="large"
                endIcon={<NavigateNextIcon />}
                onClick={handleNext}
              >
                Next Question
              </Button>
            </Box>
          )}
        </Paper>
      ) : null}
    </Box>
  )
}

export default Training
