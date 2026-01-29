"""API endpoints for user statistics."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.training import StatsResponse, ResetResponse
from app.learning.progression import ProgressionEngine
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """Get user statistics and progress across all topics."""
    user_id = settings.default_user_id
    stats = ProgressionEngine.get_all_stats(db, user_id)

    return StatsResponse(
        overall_accuracy=stats["overall_accuracy"],
        total_questions=stats["total_questions"],
        total_correct=stats["total_correct"],
        topics=[
            {
                "topic": t["topic"],
                "topic_display": t["topic_display"],
                "total_attempts": t["total_attempts"],
                "correct_attempts": t["correct_attempts"],
                "accuracy": t["accuracy"],
                "current_streak": t["current_streak"],
                "best_streak": t["best_streak"],
                "current_difficulty": t["current_difficulty"],
                "last_reviewed": t["last_reviewed"],
            }
            for t in stats["topics"]
        ],
        recent_attempts=stats["recent_attempts"],
    )


@router.post("/reset", response_model=ResetResponse)
def reset_stats(db: Session = Depends(get_db)):
    """Reset all user statistics and progress."""
    user_id = settings.default_user_id
    success = ProgressionEngine.reset_stats(db, user_id)

    return ResetResponse(
        success=success,
        message=(
            "All statistics have been reset."
            if success
            else "Failed to reset statistics."
        ),
    )
