// Card types
export interface Card {
  rank: string
  suit: string
  display: string
  notation: string
}

// Question types
export interface Question {
  question_id: string
  question_type: QuestionType
  prompt: string
  cards: Card[]
  cards2?: Card[]
  choices: string[]
  difficulty: number
  context?: string
}

export type QuestionType = 'hand_ranking' | 'which_wins' | 'starting_hand'

// Answer types
export interface AnswerRequest {
  question_id: string
  question_type: string
  answer: string
  response_time_ms?: number
}

export interface AnswerResponse {
  correct: boolean
  correct_answer: string
  explanation: string
  streak: number
  accuracy: number
  next_difficulty: number
}

// Stats types
export interface TopicStats {
  topic: string
  topic_display: string
  total_attempts: number
  correct_attempts: number
  accuracy: number
  current_streak: number
  best_streak: number
  current_difficulty: number
  last_reviewed?: string
}

export interface Stats {
  overall_accuracy: number
  total_questions: number
  total_correct: number
  topics: TopicStats[]
  recent_attempts: RecentAttempt[]
}

export interface RecentAttempt {
  id: string
  question_type: string
  correct: boolean
  response_time_ms?: number
  difficulty: number
  created_at?: string
}

// Hand ranking types
export interface HandRanking {
  rank: number
  name: string
  description: string
  example: string
  strength: number
}

// Starting hand types
export interface StartingHand {
  notation: string
  card1: string
  card2: string
  suited: boolean
  category: number
  category_name: string
}

export interface HandCategory {
  value: number
  name: string
  description: string
  color: string
}

// Question type info
export interface QuestionTypeInfo {
  id: QuestionType
  name: string
  description: string
}
