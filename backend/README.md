# Poker Hand Memorisation App - Backend

FastAPI backend for the Poker Hand Memorisation training application.

## Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Create a virtual environment:

```bash
cd backend
python -m venv venv
```

2. Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   ├── engine/        # Pure Python poker logic
│   ├── learning/      # Learning/progression engine
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic schemas
│   ├── config.py      # App configuration
│   ├── database.py    # Database setup
│   └── main.py        # FastAPI app entry point
├── tests/             # Unit and integration tests
└── requirements.txt
```

## API Endpoints

### Hands Reference

- `GET /api/hands/rankings` - Get all poker hand rankings
- `GET /api/hands/starting` - Get starting hands chart

### Training

- `GET /api/training/question` - Get a training question
- `POST /api/training/answer` - Submit an answer
- `GET /api/training/types` - Get available question types

### Statistics

- `GET /api/stats` - Get user statistics
- `POST /api/stats/reset` - Reset all progress

## Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

## Database

The app uses SQLite by default (`poker_training.db`). The database is created automatically on first run.

To use PostgreSQL in production, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL=postgresql://user:password@host:port/dbname
```
