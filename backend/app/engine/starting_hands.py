"""Texas Hold'em starting hands categorization."""

from enum import IntEnum
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import random

from app.engine.card import Card, Rank, Suit


class HandCategory(IntEnum):
    """Starting hand categories."""

    PREMIUM = 4  # AA, KK, QQ, AKs
    STRONG = 3  # JJ, TT, AK, AQs, KQs
    PLAYABLE = 2  # 99-77, AJs-ATs, KJs, QJs, JTs
    MARGINAL = 1  # 66-22, suited connectors, suited aces
    WEAK = 0  # Everything else


@dataclass
class StartingHand:
    """Represents a starting hand in Texas Hold'em."""

    card1: str  # Higher rank first (e.g., "A")
    card2: str  # Lower or equal rank (e.g., "K")
    suited: bool

    @property
    def notation(self) -> str:
        """Get standard notation (e.g., 'AKs', 'QQ', '72o')."""
        if self.card1 == self.card2:
            return f"{self.card1}{self.card2}"
        suffix = "s" if self.suited else "o"
        return f"{self.card1}{self.card2}{suffix}"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "card1": self.card1,
            "card2": self.card2,
            "suited": self.suited,
            "notation": self.notation,
        }


class StartingHands:
    """Starting hand rankings and categorization."""

    # Premium hands (top ~2.5%)
    PREMIUM = {
        "AA",
        "KK",
        "QQ",
        "AKs",
    }

    # Strong hands (top ~5%)
    STRONG = {
        "JJ",
        "TT",
        "AKo",
        "AQs",
        "AQo",
        "AJs",
        "KQs",
    }

    # Playable hands (top ~15%)
    PLAYABLE = {
        "99",
        "88",
        "77",
        "ATs",
        "AJo",
        "KQo",
        "KJs",
        "KTs",
        "QJs",
        "QTs",
        "JTs",
        "T9s",
        "98s",
        "87s",
        "76s",
    }

    # Marginal hands (situational, ~15-30%)
    MARGINAL = {
        "66",
        "55",
        "44",
        "33",
        "22",
        "A9s",
        "A8s",
        "A7s",
        "A6s",
        "A5s",
        "A4s",
        "A3s",
        "A2s",
        "ATo",
        "KJo",
        "KTo",
        "QJo",
        "QTo",
        "JTo",
        "K9s",
        "Q9s",
        "J9s",
        "T8s",
        "97s",
        "86s",
        "75s",
        "65s",
        "54s",
    }

    # Rank order for sorting
    RANK_ORDER = "AKQJT98765432"

    @classmethod
    def get_category(cls, hand: StartingHand) -> HandCategory:
        """Get the category for a starting hand."""
        notation = hand.notation

        if notation in cls.PREMIUM:
            return HandCategory.PREMIUM
        if notation in cls.STRONG:
            return HandCategory.STRONG
        if notation in cls.PLAYABLE:
            return HandCategory.PLAYABLE
        if notation in cls.MARGINAL:
            return HandCategory.MARGINAL
        return HandCategory.WEAK

    @classmethod
    def get_category_name(cls, category: HandCategory) -> str:
        """Get human-readable category name."""
        names = {
            HandCategory.PREMIUM: "Premium",
            HandCategory.STRONG: "Strong",
            HandCategory.PLAYABLE: "Playable",
            HandCategory.MARGINAL: "Marginal",
            HandCategory.WEAK: "Weak",
        }
        return names[category]

    @classmethod
    def from_cards(cls, card1: Card, card2: Card) -> StartingHand:
        """Create starting hand from two cards."""
        # Ensure higher rank is first
        r1, r2 = card1.rank, card2.rank
        if r2 > r1:
            r1, r2 = r2, r1

        suited = card1.suit == card2.suit
        return StartingHand(card1=Rank(r1).symbol, card2=Rank(r2).symbol, suited=suited)

    @classmethod
    def from_notation(cls, notation: str) -> StartingHand:
        """Create starting hand from notation (e.g., 'AKs', 'QQ')."""
        if len(notation) == 2:
            # Pocket pair
            return StartingHand(card1=notation[0], card2=notation[1], suited=False)
        elif len(notation) == 3:
            suited = notation[2].lower() == "s"
            return StartingHand(card1=notation[0], card2=notation[1], suited=suited)
        raise ValueError(f"Invalid notation: {notation}")

    @classmethod
    def generate_random(
        cls, category: Optional[HandCategory] = None
    ) -> Tuple[StartingHand, List[Card]]:
        """
        Generate a random starting hand.
        Optionally filter by category.
        Returns (StartingHand, [Card, Card])
        """
        if category is not None:
            category_hands = {
                HandCategory.PREMIUM: cls.PREMIUM,
                HandCategory.STRONG: cls.STRONG,
                HandCategory.PLAYABLE: cls.PLAYABLE,
                HandCategory.MARGINAL: cls.MARGINAL,
            }
            if category == HandCategory.WEAK:
                # Generate a random weak hand
                all_categorized = cls.PREMIUM | cls.STRONG | cls.PLAYABLE | cls.MARGINAL
                # Pick random ranks
                while True:
                    r1_idx = random.randint(0, 12)
                    r2_idx = random.randint(0, 12)
                    if r1_idx > r2_idx:
                        r1_idx, r2_idx = r2_idx, r1_idx
                    c1 = cls.RANK_ORDER[r1_idx]
                    c2 = cls.RANK_ORDER[r2_idx]
                    suited = random.choice([True, False])
                    if c1 == c2:
                        notation = f"{c1}{c2}"
                    else:
                        notation = f"{c1}{c2}{'s' if suited else 'o'}"
                    if notation not in all_categorized:
                        hand = cls.from_notation(notation)
                        break
            else:
                notation = random.choice(list(category_hands[category]))
                hand = cls.from_notation(notation)
        else:
            # Random hand from any category
            all_hands = list(cls.PREMIUM | cls.STRONG | cls.PLAYABLE | cls.MARGINAL)
            notation = random.choice(all_hands)
            hand = cls.from_notation(notation)

        # Generate actual cards
        cards = cls._notation_to_cards(hand)
        return hand, cards

    @classmethod
    def _notation_to_cards(cls, hand: StartingHand) -> List[Card]:
        """Convert starting hand to actual card objects."""
        rank1 = Rank.from_symbol(hand.card1)
        rank2 = Rank.from_symbol(hand.card2)

        suits = list(Suit)
        random.shuffle(suits)

        if hand.suited:
            suit = suits[0]
            return [Card(rank1, suit), Card(rank2, suit)]
        else:
            return [Card(rank1, suits[0]), Card(rank2, suits[1])]

    @classmethod
    def get_chart(cls) -> List[Dict]:
        """
        Get the full starting hands chart.
        Returns list of hands with their categories.
        """
        chart = []

        for category_hands, category in [
            (cls.PREMIUM, HandCategory.PREMIUM),
            (cls.STRONG, HandCategory.STRONG),
            (cls.PLAYABLE, HandCategory.PLAYABLE),
            (cls.MARGINAL, HandCategory.MARGINAL),
        ]:
            for notation in sorted(category_hands):
                hand = cls.from_notation(notation)
                chart.append(
                    {
                        "notation": notation,
                        "card1": hand.card1,
                        "card2": hand.card2,
                        "suited": hand.suited,
                        "category": category.value,
                        "category_name": cls.get_category_name(category),
                    }
                )

        return chart

    @classmethod
    def should_play(cls, hand: StartingHand, position: str = "any") -> bool:
        """
        Determine if a hand should be played.
        Position: 'early', 'middle', 'late', 'blinds', 'any'
        """
        category = cls.get_category(hand)

        # Simplified position-based recommendations
        if position == "early":
            return category >= HandCategory.STRONG
        elif position == "middle":
            return category >= HandCategory.PLAYABLE
        elif position in ("late", "blinds"):
            return category >= HandCategory.MARGINAL
        else:
            return category >= HandCategory.PLAYABLE
