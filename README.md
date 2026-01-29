# Poker Hand Memorisation App

A web application that helps users memorise and internalise optimal poker hands through interactive drills, quizzes, and spaced repetition.

## Features

- **Hand Rankings Quiz**: Identify poker hands from displayed cards
- **Which Hand Wins**: Compare two hands and determine the winner
- **Starting Hands Trainer**: Learn which preflop hands to play
- **Progress Tracking**: Track accuracy, streaks, and difficulty progression
- **Reference Material**: Hand rankings and starting hands charts

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy + SQLite
- Pydantic

### Frontend
- React 18
- TypeScript
- Material UI (MUI)
- Vite
- Axios

## Quick Start

### 1. Start the Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`

### 2. Start the Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs at: `http://localhost:5173`

## Project Structure

```
pokerapp/
├── backend/
│   ├── app/
│   │   ├── api/           # REST endpoints
│   │   ├── engine/        # Poker rules engine
│   │   ├── learning/      # Learning/progression logic
│   │   ├── models/        # Database models
│   │   └── schemas/       # API schemas
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page views
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   └── ...
└── README.md
```

## API Documentation

Once the backend is running, API docs are available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

## Architecture

```
React Frontend
      |
      | REST / JSON
      |
FastAPI Backend
      |
      ├── Poker Rules Engine (pure Python)
      ├── Learning Engine (progression logic)
      └── SQLite Database
```

## Training Modes

### Hand Rankings
Learn to identify poker hands from High Card to Royal Flush.

### Which Hand Wins
Practice comparing two hands to determine the winner.

### Starting Hands
Learn which preflop hands to play based on position and hand strength categories:
- **Premium**: AA, KK, QQ, AKs
- **Strong**: JJ, TT, AK, AQ
- **Playable**: 99-77, suited connectors
- **Marginal**: Small pairs, weak aces
- **Weak**: Everything else

## License

MIT
