"""API endpoints for hand reference data."""

from fastapi import APIRouter

from app.engine.hand_rankings import get_all_rankings, HandRank
from app.engine.starting_hands import StartingHands, HandCategory

router = APIRouter()


@router.get("/rankings")
def get_hand_rankings():
    """Get all poker hand rankings with descriptions and examples."""
    rankings = get_all_rankings()
    return {"rankings": [r.to_dict() for r in rankings]}


@router.get("/starting")
def get_starting_hands():
    """Get the starting hands chart for Texas Hold'em."""
    chart = StartingHands.get_chart()

    categories = [
        {
            "value": HandCategory.PREMIUM.value,
            "name": "Premium",
            "description": "Top tier hands - always raise",
            "color": "#4CAF50",
        },
        {
            "value": HandCategory.STRONG.value,
            "name": "Strong",
            "description": "Strong hands - raise or call raises",
            "color": "#8BC34A",
        },
        {
            "value": HandCategory.PLAYABLE.value,
            "name": "Playable",
            "description": "Playable hands - good in position",
            "color": "#FFC107",
        },
        {
            "value": HandCategory.MARGINAL.value,
            "name": "Marginal",
            "description": "Marginal hands - situational",
            "color": "#FF9800",
        },
        {
            "value": HandCategory.WEAK.value,
            "name": "Weak",
            "description": "Weak hands - generally fold",
            "color": "#f44336",
        },
    ]

    return {
        "hands": chart,
        "categories": categories,
    }
