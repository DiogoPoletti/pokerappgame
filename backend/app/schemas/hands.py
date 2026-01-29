"""Pydantic schemas for hand reference endpoints."""

from typing import List, Optional
from pydantic import BaseModel


class HandRankingInfo(BaseModel):
    """Information about a hand ranking."""

    rank: int
    name: str
    description: str
    example: str
    strength: int


class StartingHandInfo(BaseModel):
    """Information about a starting hand."""

    notation: str
    card1: str
    card2: str
    suited: bool
    category: int
    category_name: str


class HandRankingsResponse(BaseModel):
    """Response containing all hand rankings."""

    rankings: List[HandRankingInfo]


class StartingHandsResponse(BaseModel):
    """Response containing starting hands chart."""

    hands: List[StartingHandInfo]
    categories: List[dict]
