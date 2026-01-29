"""Database models for training data."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Float
from sqlalchemy.dialects.sqlite import JSON

from app.database import Base


class QuestionAttempt(Base):
    """Records each question attempt by the user."""

    __tablename__ = "question_attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, default="anonymous", index=True)
    question_type = Column(
        String, nullable=False
    )  # "hand_ranking", "which_wins", "starting_hand"
    question_data = Column(JSON, nullable=True)  # Store question details
    correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    difficulty = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "question_type": self.question_type,
            "correct": self.correct,
            "response_time_ms": self.response_time_ms,
            "difficulty": self.difficulty,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class KnowledgeScore(Base):
    """Tracks user progress on each topic."""

    __tablename__ = "knowledge_scores"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, default="anonymous", index=True)
    topic = Column(
        String, nullable=False, index=True
    )  # "hand_rankings", "starting_hands", "which_wins"
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    current_difficulty = Column(Integer, default=1)
    last_reviewed = Column(DateTime, default=datetime.utcnow)

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.correct_attempts / self.total_attempts) * 100

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "total_attempts": self.total_attempts,
            "correct_attempts": self.correct_attempts,
            "accuracy": round(self.accuracy, 1),
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "current_difficulty": self.current_difficulty,
            "last_reviewed": (
                self.last_reviewed.isoformat() if self.last_reviewed else None
            ),
        }
