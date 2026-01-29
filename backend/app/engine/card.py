"""Card representation for poker hands."""

from enum import IntEnum
from dataclasses import dataclass
from typing import List
import random


class Suit(IntEnum):
    """Card suits."""

    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

    @property
    def symbol(self) -> str:
        """Get suit symbol."""
        symbols = {
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦",
            Suit.CLUBS: "♣",
            Suit.SPADES: "♠",
        }
        return symbols[self]

    @property
    def letter(self) -> str:
        """Get suit letter (h, d, c, s)."""
        letters = {
            Suit.HEARTS: "h",
            Suit.DIAMONDS: "d",
            Suit.CLUBS: "c",
            Suit.SPADES: "s",
        }
        return letters[self]

    @classmethod
    def from_letter(cls, letter: str) -> "Suit":
        """Create suit from letter."""
        mapping = {"h": cls.HEARTS, "d": cls.DIAMONDS, "c": cls.CLUBS, "s": cls.SPADES}
        return mapping[letter.lower()]


class Rank(IntEnum):
    """Card ranks (2-14, where 14 is Ace)."""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @property
    def symbol(self) -> str:
        """Get rank symbol."""
        if self.value <= 10:
            return str(self.value)
        symbols = {Rank.JACK: "J", Rank.QUEEN: "Q", Rank.KING: "K", Rank.ACE: "A"}
        return symbols[self]

    @classmethod
    def from_symbol(cls, symbol: str) -> "Rank":
        """Create rank from symbol."""
        symbol = symbol.upper()
        if symbol.isdigit():
            return cls(int(symbol))
        mapping = {
            "T": cls.TEN,
            "J": cls.JACK,
            "Q": cls.QUEEN,
            "K": cls.KING,
            "A": cls.ACE,
        }
        return mapping[symbol]


@dataclass(frozen=True)
class Card:
    """Represents a playing card."""

    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        """String representation (e.g., 'Ah' for Ace of hearts)."""
        return f"{self.rank.symbol}{self.suit.letter}"

    def __repr__(self) -> str:
        return f"Card({self.rank.symbol}{self.suit.letter})"

    @property
    def display(self) -> str:
        """Display with suit symbol (e.g., 'A♥')."""
        return f"{self.rank.symbol}{self.suit.symbol}"

    @classmethod
    def from_string(cls, s: str) -> "Card":
        """Create card from string notation (e.g., 'Ah', 'Ks', '2d')."""
        if len(s) < 2:
            raise ValueError(f"Invalid card notation: {s}")
        rank_str = s[:-1]
        suit_str = s[-1]
        return cls(rank=Rank.from_symbol(rank_str), suit=Suit.from_letter(suit_str))

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "rank": self.rank.symbol,
            "suit": self.suit.letter,
            "display": self.display,
            "notation": str(self),
        }


class Deck:
    """Standard 52-card deck."""

    def __init__(self):
        """Create a new shuffled deck."""
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        """Reset and shuffle the deck."""
        self.cards = [Card(rank=rank, suit=suit) for suit in Suit for rank in Rank]
        random.shuffle(self.cards)

    def draw(self, n: int = 1) -> List[Card]:
        """Draw n cards from the deck."""
        if n > len(self.cards):
            raise ValueError(f"Cannot draw {n} cards, only {len(self.cards)} remaining")
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

    def draw_specific(self, card_strings: List[str]) -> List[Card]:
        """Draw specific cards from the deck."""
        cards = [Card.from_string(s) for s in card_strings]
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)
            else:
                raise ValueError(f"Card {card} not in deck")
        return cards

    def __len__(self) -> int:
        return len(self.cards)


def parse_cards(card_strings: List[str]) -> List[Card]:
    """Parse a list of card strings into Card objects."""
    return [Card.from_string(s) for s in card_strings]
