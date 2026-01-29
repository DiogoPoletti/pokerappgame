"""API endpoint tests."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine


@pytest.fixture(autouse=True)
def setup_db():
    """Setup test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


class TestHandsAPI:
    """Test suite for hands API endpoints."""

    def test_get_rankings(self, client):
        """Test getting hand rankings."""
        response = client.get("/api/hands/rankings")
        assert response.status_code == 200

        data = response.json()
        assert "rankings" in data
        assert len(data["rankings"]) == 10  # 10 hand ranks

        # Check structure
        first = data["rankings"][0]
        assert "rank" in first
        assert "name" in first
        assert "description" in first
        assert "example" in first

    def test_get_starting_hands(self, client):
        """Test getting starting hands chart."""
        response = client.get("/api/hands/starting")
        assert response.status_code == 200

        data = response.json()
        assert "hands" in data
        assert "categories" in data
        assert len(data["hands"]) > 0
        assert len(data["categories"]) == 5


class TestTrainingAPI:
    """Test suite for training API endpoints."""

    def test_get_question(self, client):
        """Test getting a training question."""
        response = client.get("/api/training/question")
        assert response.status_code == 200

        data = response.json()
        assert "question_id" in data
        assert "question_type" in data
        assert "prompt" in data
        assert "cards" in data
        assert "choices" in data
        assert "difficulty" in data

    def test_get_question_specific_type(self, client):
        """Test getting a specific question type."""
        response = client.get("/api/training/question?question_type=hand_ranking")
        assert response.status_code == 200

        data = response.json()
        assert data["question_type"] == "hand_ranking"

    def test_get_question_invalid_type(self, client):
        """Test getting question with invalid type."""
        response = client.get("/api/training/question?question_type=invalid")
        assert response.status_code == 400

    def test_submit_answer(self, client):
        """Test submitting an answer."""
        # First get a question
        question_response = client.get("/api/training/question")
        question = question_response.json()

        # Submit an answer
        answer_response = client.post(
            "/api/training/answer",
            json={
                "question_id": question["question_id"],
                "question_type": question["question_type"],
                "answer": question["choices"][0],
                "response_time_ms": 1500,
            },
        )

        assert answer_response.status_code == 200

        data = answer_response.json()
        assert "correct" in data
        assert "correct_answer" in data
        assert "explanation" in data
        assert "streak" in data
        assert "accuracy" in data

    def test_get_question_types(self, client):
        """Test getting available question types."""
        response = client.get("/api/training/types")
        assert response.status_code == 200

        data = response.json()
        assert "types" in data
        assert len(data["types"]) == 3


class TestStatsAPI:
    """Test suite for stats API endpoints."""

    def test_get_stats(self, client):
        """Test getting user stats."""
        response = client.get("/api/stats")
        assert response.status_code == 200

        data = response.json()
        assert "overall_accuracy" in data
        assert "total_questions" in data
        assert "topics" in data

    def test_reset_stats(self, client):
        """Test resetting stats."""
        # First answer some questions to create data
        question_response = client.get("/api/training/question")
        question = question_response.json()
        client.post(
            "/api/training/answer",
            json={
                "question_id": question["question_id"],
                "question_type": question["question_type"],
                "answer": question["choices"][0],
            },
        )

        # Reset
        reset_response = client.post("/api/stats/reset")
        assert reset_response.status_code == 200

        data = reset_response.json()
        assert data["success"] is True

    def test_stats_update_after_answer(self, client):
        """Test that stats update after answering questions."""
        # Get initial stats
        initial_stats = client.get("/api/stats").json()
        initial_total = initial_stats["total_questions"]

        # Answer a question
        question = client.get("/api/training/question").json()
        client.post(
            "/api/training/answer",
            json={
                "question_id": question["question_id"],
                "question_type": question["question_type"],
                "answer": question["choices"][0],
            },
        )

        # Check updated stats
        updated_stats = client.get("/api/stats").json()
        assert updated_stats["total_questions"] == initial_total + 1
