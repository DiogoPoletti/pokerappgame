# Poker Hand Memorisation App - Frontend

React + TypeScript + MUI frontend for the Poker Hand Memorisation training application.

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Running the Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

**Note:** The backend server must be running on `http://localhost:8000` for the API to work.

## Project Structure

```
frontend/
├── src/
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API client
│   ├── types/         # TypeScript type definitions
│   ├── App.tsx        # Main app component
│   ├── main.tsx       # Entry point
│   └── theme.ts       # MUI theme configuration
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Components

- `PlayingCard` - Visual playing card component
- `PokerHand` - Displays a hand of cards
- `ActionButtons` - Answer selection buttons
- `FeedbackDisplay` - Shows correct/incorrect feedback
- `ProgressIndicator` - Streak and accuracy display
- `StatsCard` - Statistics display card
- `Navbar` - Navigation bar

## Pages

- `Dashboard` (`/`) - Overview and statistics
- `Training` (`/train/:type`) - Interactive training session
- `Reference` (`/reference`) - Hand rankings and starting hands reference

## Building for Production

```bash
npm run build
```

Build output will be in the `dist/` directory.

## Linting

```bash
npm run lint
```
