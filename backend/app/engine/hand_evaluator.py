"""Hand evaluation logic for poker."""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from collections import Counter
from itertools import combinations

from app.engine.card import Card, Rank
from app.engine.hand_rankings import HandRank


@dataclass
class EvaluatedHand:
    """Result of hand evaluation."""

    rank: HandRank
    primary_values: Tuple[int, ...]  # Values that make up the hand (e.g., pair rank)
    kickers: Tuple[int, ...]  # Remaining cards for tiebreaking
    cards: List[Card]  # The 5 cards that make up the best hand

    @property
    def score(self) -> Tuple[int, ...]:
        """Get comparable score tuple for hand comparison."""
        return (self.rank.value,) + self.primary_values + self.kickers

    def __lt__(self, other: "EvaluatedHand") -> bool:
        return self.score < other.score

    def __gt__(self, other: "EvaluatedHand") -> bool:
        return self.score > other.score

    def __eq__(self, other: "EvaluatedHand") -> bool:
        return self.score == other.score

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "rank": self.rank.value,
            "rank_name": self.rank.display_name,
            "cards": [c.to_dict() for c in self.cards],
            "description": self.rank.description,
        }


class HandEvaluator:
    """Evaluates poker hands."""

    @staticmethod
    def evaluate(cards: List[Card]) -> EvaluatedHand:
        """
        Evaluate a poker hand (5-7 cards).
        Returns the best possible 5-card hand.
        """
        if len(cards) < 5:
            raise ValueError(f"Need at least 5 cards, got {len(cards)}")

        if len(cards) == 5:
            return HandEvaluator._evaluate_five(cards)

        # For 6-7 cards, find the best 5-card combination
        best_hand: Optional[EvaluatedHand] = None
        for combo in combinations(cards, 5):
            hand = HandEvaluator._evaluate_five(list(combo))
            if best_hand is None or hand > best_hand:
                best_hand = hand

        return best_hand

    @staticmethod
    def _evaluate_five(cards: List[Card]) -> EvaluatedHand:
        """Evaluate exactly 5 cards."""
        ranks = sorted([c.rank.value for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        rank_counts = Counter(ranks)

        is_flush = len(set(suits)) == 1
        is_straight, straight_high = HandEvaluator._check_straight(ranks)

        # Check for straight flush / royal flush
        if is_flush and is_straight:
            if straight_high == 14:  # Ace high
                return EvaluatedHand(
                    rank=HandRank.ROYAL_FLUSH,
                    primary_values=(14,),
                    kickers=(),
                    cards=cards,
                )
            return EvaluatedHand(
                rank=HandRank.STRAIGHT_FLUSH,
                primary_values=(straight_high,),
                kickers=(),
                cards=cards,
            )

        # Four of a kind
        if 4 in rank_counts.values():
            quad_rank = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = [r for r in ranks if r != quad_rank][0]
            return EvaluatedHand(
                rank=HandRank.FOUR_OF_A_KIND,
                primary_values=(quad_rank,),
                kickers=(kicker,),
                cards=cards,
            )

        # Full house
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            trips_rank = [r for r, c in rank_counts.items() if c == 3][0]
            pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
            return EvaluatedHand(
                rank=HandRank.FULL_HOUSE,
                primary_values=(trips_rank, pair_rank),
                kickers=(),
                cards=cards,
            )

        # Flush
        if is_flush:
            return EvaluatedHand(
                rank=HandRank.FLUSH,
                primary_values=tuple(ranks),
                kickers=(),
                cards=cards,
            )

        # Straight
        if is_straight:
            return EvaluatedHand(
                rank=HandRank.STRAIGHT,
                primary_values=(straight_high,),
                kickers=(),
                cards=cards,
            )

        # Three of a kind
        if 3 in rank_counts.values():
            trips_rank = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r in ranks if r != trips_rank], reverse=True)
            return EvaluatedHand(
                rank=HandRank.THREE_OF_A_KIND,
                primary_values=(trips_rank,),
                kickers=tuple(kickers),
                cards=cards,
            )

        # Two pair
        pairs = [r for r, c in rank_counts.items() if c == 2]
        if len(pairs) == 2:
            pairs = sorted(pairs, reverse=True)
            kicker = [r for r in ranks if r not in pairs][0]
            return EvaluatedHand(
                rank=HandRank.TWO_PAIR,
                primary_values=tuple(pairs),
                kickers=(kicker,),
                cards=cards,
            )

        # One pair
        if len(pairs) == 1:
            pair_rank = pairs[0]
            kickers = sorted([r for r in ranks if r != pair_rank], reverse=True)
            return EvaluatedHand(
                rank=HandRank.ONE_PAIR,
                primary_values=(pair_rank,),
                kickers=tuple(kickers),
                cards=cards,
            )

        # High card
        return EvaluatedHand(
            rank=HandRank.HIGH_CARD,
            primary_values=(ranks[0],),
            kickers=tuple(ranks[1:]),
            cards=cards,
        )

    @staticmethod
    def _check_straight(ranks: List[int]) -> Tuple[bool, int]:
        """
        Check if ranks form a straight.
        Returns (is_straight, high_card).
        Handles wheel straight (A-2-3-4-5).
        """
        unique_ranks = sorted(set(ranks), reverse=True)

        if len(unique_ranks) != 5:
            return False, 0

        # Normal straight check
        if unique_ranks[0] - unique_ranks[4] == 4:
            return True, unique_ranks[0]

        # Wheel straight (A-2-3-4-5)
        if unique_ranks == [14, 5, 4, 3, 2]:
            return True, 5  # 5-high straight

        return False, 0

    @staticmethod
    def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
        """
        Compare two hands.
        Returns: 1 if hand1 wins, -1 if hand2 wins, 0 if tie.
        """
        eval1 = HandEvaluator.evaluate(hand1)
        eval2 = HandEvaluator.evaluate(hand2)

        if eval1 > eval2:
            return 1
        elif eval1 < eval2:
            return -1
        return 0
