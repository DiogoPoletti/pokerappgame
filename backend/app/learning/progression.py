"""Progression and difficulty management for learning."""

from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.models.training import KnowledgeScore, QuestionAttempt
from app.config import get_settings

settings = get_settings()


class ProgressionEngine:
    """Manages user progression and difficulty adjustment."""

    # Thresholds for difficulty changes
    ACCURACY_INCREASE_THRESHOLD = 80  # Increase difficulty if accuracy > 80%
    ACCURACY_DECREASE_THRESHOLD = 50  # Decrease difficulty if accuracy < 50%
    STREAK_FOR_INCREASE = 5  # Consecutive correct answers to increase difficulty
    MIN_ATTEMPTS_FOR_ADJUSTMENT = 5  # Minimum attempts before adjusting

    MAX_DIFFICULTY = 5
    MIN_DIFFICULTY = 1

    TOPICS = ["hand_ranking", "which_wins", "starting_hand"]
    TOPIC_DISPLAY_NAMES = {
        "hand_ranking": "Hand Rankings",
        "which_wins": "Which Hand Wins",
        "starting_hand": "Starting Hands",
    }

    @classmethod
    def get_or_create_score(
        cls, db: Session, topic: str, user_id: str = None
    ) -> KnowledgeScore:
        """Get or create a knowledge score for a topic."""
        user_id = user_id or settings.default_user_id

        score = (
            db.query(KnowledgeScore)
            .filter(KnowledgeScore.user_id == user_id, KnowledgeScore.topic == topic)
            .first()
        )

        if not score:
            score = KnowledgeScore(
                user_id=user_id,
                topic=topic,
                total_attempts=0,
                correct_attempts=0,
                current_streak=0,
                best_streak=0,
                current_difficulty=1,
            )
            db.add(score)
            db.commit()
            db.refresh(score)

        return score

    @classmethod
    def record_attempt(
        cls,
        db: Session,
        question_type: str,
        correct: bool,
        response_time_ms: Optional[int] = None,
        difficulty: int = 1,
        question_data: Optional[Dict] = None,
        user_id: str = None,
    ) -> KnowledgeScore:
        """Record an attempt and update progression."""
        user_id = user_id or settings.default_user_id

        # Create attempt record
        attempt = QuestionAttempt(
            user_id=user_id,
            question_type=question_type,
            correct=correct,
            response_time_ms=response_time_ms,
            difficulty=difficulty,
            question_data=question_data,
        )
        db.add(attempt)

        # Update knowledge score
        score = cls.get_or_create_score(db, question_type, user_id)
        score.total_attempts += 1
        if correct:
            score.correct_attempts += 1
            score.current_streak += 1
            if score.current_streak > score.best_streak:
                score.best_streak = score.current_streak
        else:
            score.current_streak = 0

        score.last_reviewed = datetime.utcnow()

        # Adjust difficulty
        score.current_difficulty = cls._calculate_new_difficulty(score)

        db.commit()
        db.refresh(score)

        return score

    @classmethod
    def _calculate_new_difficulty(cls, score: KnowledgeScore) -> int:
        """Calculate new difficulty based on performance."""
        current = score.current_difficulty

        # Not enough data yet
        if score.total_attempts < cls.MIN_ATTEMPTS_FOR_ADJUSTMENT:
            return current

        accuracy = score.accuracy

        # Increase difficulty
        if (
            accuracy >= cls.ACCURACY_INCREASE_THRESHOLD
            or score.current_streak >= cls.STREAK_FOR_INCREASE
        ):
            return min(current + 1, cls.MAX_DIFFICULTY)

        # Decrease difficulty
        if accuracy < cls.ACCURACY_DECREASE_THRESHOLD:
            return max(current - 1, cls.MIN_DIFFICULTY)

        return current

    @classmethod
    def get_recommended_topic(cls, db: Session, user_id: str = None) -> str:
        """Get the recommended topic to practice based on weaknesses."""
        user_id = user_id or settings.default_user_id

        scores = (
            db.query(KnowledgeScore).filter(KnowledgeScore.user_id == user_id).all()
        )

        if not scores:
            # New user - start with hand rankings
            return "hand_ranking"

        # Find weakest topic (lowest accuracy with some attempts)
        weakest = None
        lowest_accuracy = 100

        for score in scores:
            if score.total_attempts >= 3 and score.accuracy < lowest_accuracy:
                lowest_accuracy = score.accuracy
                weakest = score.topic

        # If no weak topic found, pick least practiced
        if weakest is None:
            practiced_topics = {s.topic for s in scores}
            for topic in cls.TOPICS:
                if topic not in practiced_topics:
                    return topic

            # All practiced - return the one with fewest attempts
            scores.sort(key=lambda s: s.total_attempts)
            return scores[0].topic

        return weakest

    @classmethod
    def get_all_stats(cls, db: Session, user_id: str = None) -> Dict:
        """Get comprehensive statistics for the user."""
        user_id = user_id or settings.default_user_id

        scores = (
            db.query(KnowledgeScore).filter(KnowledgeScore.user_id == user_id).all()
        )

        # Calculate overall stats
        total_attempts = sum(s.total_attempts for s in scores)
        total_correct = sum(s.correct_attempts for s in scores)
        overall_accuracy = (
            (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        )

        # Get recent attempts
        recent = (
            db.query(QuestionAttempt)
            .filter(QuestionAttempt.user_id == user_id)
            .order_by(QuestionAttempt.created_at.desc())
            .limit(10)
            .all()
        )

        # Build topic stats
        topic_stats = []
        for topic in cls.TOPICS:
            score = next((s for s in scores if s.topic == topic), None)
            if score:
                topic_stats.append(
                    {
                        "topic": topic,
                        "topic_display": cls.TOPIC_DISPLAY_NAMES.get(topic, topic),
                        "total_attempts": score.total_attempts,
                        "correct_attempts": score.correct_attempts,
                        "accuracy": round(score.accuracy, 1),
                        "current_streak": score.current_streak,
                        "best_streak": score.best_streak,
                        "current_difficulty": score.current_difficulty,
                        "last_reviewed": (
                            score.last_reviewed.isoformat()
                            if score.last_reviewed
                            else None
                        ),
                    }
                )
            else:
                topic_stats.append(
                    {
                        "topic": topic,
                        "topic_display": cls.TOPIC_DISPLAY_NAMES.get(topic, topic),
                        "total_attempts": 0,
                        "correct_attempts": 0,
                        "accuracy": 0,
                        "current_streak": 0,
                        "best_streak": 0,
                        "current_difficulty": 1,
                        "last_reviewed": None,
                    }
                )

        return {
            "overall_accuracy": round(overall_accuracy, 1),
            "total_questions": total_attempts,
            "total_correct": total_correct,
            "topics": topic_stats,
            "recent_attempts": [a.to_dict() for a in recent],
        }

    @classmethod
    def reset_stats(cls, db: Session, user_id: str = None) -> bool:
        """Reset all statistics for a user."""
        user_id = user_id or settings.default_user_id

        db.query(QuestionAttempt).filter(QuestionAttempt.user_id == user_id).delete()

        db.query(KnowledgeScore).filter(KnowledgeScore.user_id == user_id).delete()

        db.commit()
        return True
