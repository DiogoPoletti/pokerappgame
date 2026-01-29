"""API endpoints for training sessions."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.training import (
    QuestionResponse,
    AnswerRequest,
    AnswerResponse,
    CardSchema,
)
from app.learning.question_generator import QuestionGenerator
from app.learning.progression import ProgressionEngine
from app.config import get_settings

router = APIRouter()
settings = get_settings()

# In-memory question cache (for MVP - would use Redis in production)
_question_cache = {}


@router.get("/question", response_model=QuestionResponse)
def get_question(
    question_type: Optional[str] = None,
    difficulty: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Get a training question.

    - question_type: 'hand_ranking', 'which_wins', or 'starting_hand'
    - difficulty: 1-5 (optional, uses adaptive difficulty if not specified)
    """
    user_id = settings.default_user_id

    # Determine question type
    if question_type is None:
        question_type = ProgressionEngine.get_recommended_topic(db, user_id)

    if question_type not in QuestionGenerator.QUESTION_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid question type. Must be one of: {QuestionGenerator.QUESTION_TYPES}",
        )

    # Determine difficulty
    if difficulty is None:
        score = ProgressionEngine.get_or_create_score(db, question_type, user_id)
        difficulty = score.current_difficulty

    difficulty = max(1, min(5, difficulty))

    # Generate question
    question = QuestionGenerator.generate(question_type, difficulty)

    # Cache the question for answer validation
    _question_cache[question.question_id] = question

    # Build response
    cards = [
        CardSchema(
            rank=c.rank.symbol, suit=c.suit.letter, display=c.display, notation=str(c)
        )
        for c in question.cards
    ]

    cards2 = None
    if question.cards2:
        cards2 = [
            CardSchema(
                rank=c.rank.symbol,
                suit=c.suit.letter,
                display=c.display,
                notation=str(c),
            )
            for c in question.cards2
        ]

    return QuestionResponse(
        question_id=question.question_id,
        question_type=question.question_type,
        prompt=question.prompt,
        cards=cards,
        cards2=cards2,
        choices=question.choices,
        difficulty=question.difficulty,
        context=question.question_data.get("position"),
    )


@router.post("/answer", response_model=AnswerResponse)
def submit_answer(request: AnswerRequest, db: Session = Depends(get_db)):
    """
    Submit an answer to a training question.
    Returns whether the answer was correct and updates progress.
    """
    user_id = settings.default_user_id

    # Get cached question
    question = _question_cache.get(request.question_id)

    if question is None:
        # Question not in cache - try to validate from request data
        raise HTTPException(
            status_code=400, detail="Question not found. It may have expired."
        )

    # Check answer
    correct = request.answer == question.correct_answer

    # Record the attempt
    score = ProgressionEngine.record_attempt(
        db=db,
        question_type=request.question_type,
        correct=correct,
        response_time_ms=request.response_time_ms,
        difficulty=question.difficulty,
        question_data=question.question_data,
        user_id=user_id,
    )

    # Clean up cache
    del _question_cache[request.question_id]

    return AnswerResponse(
        correct=correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        streak=score.current_streak,
        accuracy=round(score.accuracy, 1),
        next_difficulty=score.current_difficulty,
    )


@router.get("/types")
def get_question_types():
    """Get available question types with descriptions."""
    return {
        "types": [
            {
                "id": "hand_ranking",
                "name": "Hand Rankings",
                "description": "Identify the poker hand from the cards shown",
            },
            {
                "id": "which_wins",
                "name": "Which Hand Wins",
                "description": "Compare two hands and determine the winner",
            },
            {
                "id": "starting_hand",
                "name": "Starting Hands",
                "description": "Learn which starting hands to play preflop",
            },
        ]
    }
