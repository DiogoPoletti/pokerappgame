"""Unit tests for the hand evaluator."""

import pytest
from app.engine.card import Card, Rank, Suit, parse_cards
from app.engine.hand_evaluator import HandEvaluator, EvaluatedHand
from app.engine.hand_rankings import HandRank


class TestHandEvaluator:
    """Test suite for HandEvaluator."""

    def test_royal_flush(self):
        """Test royal flush detection."""
        cards = parse_cards(["Ah", "Kh", "Qh", "Jh", "10h"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.ROYAL_FLUSH

    def test_straight_flush(self):
        """Test straight flush detection."""
        cards = parse_cards(["9h", "8h", "7h", "6h", "5h"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT_FLUSH
        assert result.primary_values == (9,)

    def test_four_of_a_kind(self):
        """Test four of a kind detection."""
        cards = parse_cards(["Ah", "Ad", "Ac", "As", "Kh"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FOUR_OF_A_KIND
        assert result.primary_values == (14,)  # Aces

    def test_full_house(self):
        """Test full house detection."""
        cards = parse_cards(["Ah", "Ad", "Ac", "Ks", "Kh"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FULL_HOUSE
        assert result.primary_values == (14, 13)  # Aces over Kings

    def test_flush(self):
        """Test flush detection."""
        cards = parse_cards(["Ah", "Kh", "9h", "7h", "2h"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FLUSH

    def test_straight(self):
        """Test straight detection."""
        cards = parse_cards(["9h", "8d", "7c", "6s", "5h"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT
        assert result.primary_values == (9,)

    def test_wheel_straight(self):
        """Test wheel straight (A-2-3-4-5)."""
        cards = parse_cards(["Ah", "2d", "3c", "4s", "5h"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT
        assert result.primary_values == (5,)  # 5-high straight

    def test_three_of_a_kind(self):
        """Test three of a kind detection."""
        cards = parse_cards(["Ah", "Ad", "Ac", "Ks", "Qh"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.THREE_OF_A_KIND

    def test_two_pair(self):
        """Test two pair detection."""
        cards = parse_cards(["Ah", "Ad", "Kc", "Ks", "Qh"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.TWO_PAIR
        assert result.primary_values == (14, 13)  # Aces and Kings

    def test_one_pair(self):
        """Test one pair detection."""
        cards = parse_cards(["Ah", "Ad", "Kc", "Qs", "Jh"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.ONE_PAIR
        assert result.primary_values == (14,)

    def test_high_card(self):
        """Test high card detection."""
        cards = parse_cards(["Ah", "Kd", "9c", "7s", "2h"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.HIGH_CARD

    def test_compare_hands_different_ranks(self):
        """Test comparing hands with different ranks."""
        flush = parse_cards(["Ah", "Kh", "9h", "7h", "2h"])
        straight = parse_cards(["9h", "8d", "7c", "6s", "5h"])

        result = HandEvaluator.compare_hands(flush, straight)
        assert result == 1  # Flush wins

    def test_compare_hands_same_rank_different_kickers(self):
        """Test comparing hands with same rank but different kickers."""
        pair_aces_k = parse_cards(["Ah", "Ad", "Kc", "Qs", "Jh"])
        pair_aces_q = parse_cards(["As", "Ac", "Qd", "Jh", "10s"])

        result = HandEvaluator.compare_hands(pair_aces_k, pair_aces_q)
        assert result == 1  # First hand wins (King kicker > Queen kicker)

    def test_compare_hands_tie(self):
        """Test comparing identical hands."""
        hand1 = parse_cards(["Ah", "Kh", "Qh", "Jh", "10h"])  # Royal flush hearts
        hand2 = parse_cards(["As", "Ks", "Qs", "Js", "10s"])  # Royal flush spades

        result = HandEvaluator.compare_hands(hand1, hand2)
        assert result == 0  # Tie

    def test_seven_card_evaluation(self):
        """Test evaluation with 7 cards (finds best 5)."""
        cards = parse_cards(["Ah", "Kh", "Qh", "Jh", "10h", "2d", "3c"])
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.ROYAL_FLUSH

    def test_invalid_hand_too_few_cards(self):
        """Test that evaluation fails with fewer than 5 cards."""
        cards = parse_cards(["Ah", "Kh", "Qh", "Jh"])
        with pytest.raises(ValueError):
            HandEvaluator.evaluate(cards)


class TestCard:
    """Test suite for Card class."""

    def test_card_from_string(self):
        """Test creating cards from string notation."""
        card = Card.from_string("Ah")
        assert card.rank == Rank.ACE
        assert card.suit == Suit.HEARTS

    def test_card_to_string(self):
        """Test card string representation."""
        card = Card(Rank.KING, Suit.SPADES)
        assert str(card) == "Ks"

    def test_card_display(self):
        """Test card display with suit symbol."""
        card = Card(Rank.QUEEN, Suit.DIAMONDS)
        assert card.display == "Q♦"

    def test_parse_cards(self):
        """Test parsing multiple cards."""
        cards = parse_cards(["Ah", "Ks", "Qd", "Jc", "10h"])
        assert len(cards) == 5
        assert cards[0].rank == Rank.ACE
        assert cards[1].rank == Rank.KING
