"""Hand rankings and definitions."""

from enum import IntEnum
from dataclasses import dataclass
from typing import List


class HandRank(IntEnum):
    """Poker hand rankings from lowest to highest."""

    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    @property
    def display_name(self) -> str:
        """Get human-readable name."""
        names = {
            HandRank.HIGH_CARD: "High Card",
            HandRank.ONE_PAIR: "One Pair",
            HandRank.TWO_PAIR: "Two Pair",
            HandRank.THREE_OF_A_KIND: "Three of a Kind",
            HandRank.STRAIGHT: "Straight",
            HandRank.FLUSH: "Flush",
            HandRank.FULL_HOUSE: "Full House",
            HandRank.FOUR_OF_A_KIND: "Four of a Kind",
            HandRank.STRAIGHT_FLUSH: "Straight Flush",
            HandRank.ROYAL_FLUSH: "Royal Flush",
        }
        return names[self]

    @property
    def description(self) -> str:
        """Get description of the hand."""
        descriptions = {
            HandRank.HIGH_CARD: "No matching cards. Highest card plays.",
            HandRank.ONE_PAIR: "Two cards of the same rank.",
            HandRank.TWO_PAIR: "Two different pairs.",
            HandRank.THREE_OF_A_KIND: "Three cards of the same rank.",
            HandRank.STRAIGHT: "Five consecutive cards of mixed suits.",
            HandRank.FLUSH: "Five cards of the same suit.",
            HandRank.FULL_HOUSE: "Three of a kind plus a pair.",
            HandRank.FOUR_OF_A_KIND: "Four cards of the same rank.",
            HandRank.STRAIGHT_FLUSH: "Five consecutive cards of the same suit.",
            HandRank.ROYAL_FLUSH: "A, K, Q, J, 10 all of the same suit.",
        }
        return descriptions[self]

    @property
    def example(self) -> str:
        """Get example cards for this hand."""
        examples = {
            HandRank.HIGH_CARD: "Ah, Kd, 9c, 7s, 2h",
            HandRank.ONE_PAIR: "Ah, Ad, Kc, 7s, 2h",
            HandRank.TWO_PAIR: "Ah, Ad, Kc, Ks, 2h",
            HandRank.THREE_OF_A_KIND: "Ah, Ad, Ac, Ks, 2h",
            HandRank.STRAIGHT: "9h, 8d, 7c, 6s, 5h",
            HandRank.FLUSH: "Ah, Kh, 9h, 7h, 2h",
            HandRank.FULL_HOUSE: "Ah, Ad, Ac, Ks, Kh",
            HandRank.FOUR_OF_A_KIND: "Ah, Ad, Ac, As, Kh",
            HandRank.STRAIGHT_FLUSH: "9h, 8h, 7h, 6h, 5h",
            HandRank.ROYAL_FLUSH: "Ah, Kh, Qh, Jh, 10h",
        }
        return examples[self]


@dataclass
class HandRankingInfo:
    """Complete information about a hand ranking."""

    rank: HandRank
    name: str
    description: str
    example: str
    strength: int  # 1-10

    @classmethod
    def from_rank(cls, rank: HandRank) -> "HandRankingInfo":
        """Create info from a hand rank."""
        return cls(
            rank=rank,
            name=rank.display_name,
            description=rank.description,
            example=rank.example,
            strength=rank.value,
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank.value,
            "name": self.name,
            "description": self.description,
            "example": self.example,
            "strength": self.strength,
        }


def get_all_rankings() -> List[HandRankingInfo]:
    """Get all hand rankings in order from highest to lowest."""
    return [HandRankingInfo.from_rank(rank) for rank in sorted(HandRank, reverse=True)]
