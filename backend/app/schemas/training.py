"""Pydantic schemas for training endpoints."""

from typing import List, Optional, Any
from pydantic import BaseModel
from datetime import datetime


class CardSchema(BaseModel):
    """Card representation for API."""

    rank: str
    suit: str
    display: str
    notation: str


class QuestionResponse(BaseModel):
    """Response containing a training question."""

    question_id: str
    question_type: str  # "hand_ranking", "which_wins", "starting_hand"
    prompt: str
    cards: List[CardSchema]
    cards2: Optional[List[CardSchema]] = None  # For "which_wins" questions
    choices: List[str]
    difficulty: int
    context: Optional[str] = None  # e.g., "preflop", position info


class AnswerRequest(BaseModel):
    """Request to submit an answer."""

    question_id: str
    question_type: str
    answer: str
    response_time_ms: Optional[int] = None
    question_data: Optional[dict] = None  # Echo back for verification


class AnswerResponse(BaseModel):
    """Response after submitting an answer."""

    correct: bool
    correct_answer: str
    explanation: str
    streak: int
    accuracy: float
    next_difficulty: int


class TopicStats(BaseModel):
    """Statistics for a single topic."""

    topic: str
    topic_display: str
    total_attempts: int
    correct_attempts: int
    accuracy: float
    current_streak: int
    best_streak: int
    current_difficulty: int
    last_reviewed: Optional[datetime] = None


class StatsResponse(BaseModel):
    """Overall statistics response."""

    overall_accuracy: float
    total_questions: int
    total_correct: int
    topics: List[TopicStats]
    recent_attempts: List[dict]


class ResetResponse(BaseModel):
    """Response after resetting stats."""

    success: bool
    message: str
