import axios from 'axios'
import type {
  Question,
  AnswerRequest,
  AnswerResponse,
  Stats,
  HandRanking,
  StartingHand,
  HandCategory,
  QuestionTypeInfo,
} from '../types'

// Use environment variable for API URL, fallback to relative path for local dev
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Training endpoints
export const getQuestion = async (
  questionType?: string,
  difficulty?: number
): Promise<Question> => {
  const params = new URLSearchParams()
  if (questionType) params.append('question_type', questionType)
  if (difficulty) params.append('difficulty', difficulty.toString())
  
  const response = await api.get(`/training/question?${params}`)
  return response.data
}

export const submitAnswer = async (
  request: AnswerRequest
): Promise<AnswerResponse> => {
  const response = await api.post('/training/answer', request)
  return response.data
}

export const getQuestionTypes = async (): Promise<QuestionTypeInfo[]> => {
  const response = await api.get('/training/types')
  return response.data.types
}

// Stats endpoints
export const getStats = async (): Promise<Stats> => {
  const response = await api.get('/stats')
  return response.data
}

export const resetStats = async (): Promise<{ success: boolean; message: string }> => {
  const response = await api.post('/stats/reset')
  return response.data
}

// Hand reference endpoints
export const getHandRankings = async (): Promise<HandRanking[]> => {
  const response = await api.get('/hands/rankings')
  return response.data.rankings
}

export const getStartingHands = async (): Promise<{
  hands: StartingHand[]
  categories: HandCategory[]
}> => {
  const response = await api.get('/hands/starting')
  return response.data
}

export default api
