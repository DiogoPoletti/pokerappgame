"""Unit tests for starting hands module."""

import pytest
from app.engine.starting_hands import StartingHands, StartingHand, HandCategory
from app.engine.card import Card, Rank, Suit


class TestStartingHands:
    """Test suite for StartingHands."""

    def test_premium_hands(self):
        """Test that premium hands are correctly categorized."""
        premium_notations = ["AA", "KK", "QQ", "AKs"]
        for notation in premium_notations:
            hand = StartingHands.from_notation(notation)
            category = StartingHands.get_category(hand)
            assert category == HandCategory.PREMIUM, f"{notation} should be premium"

    def test_strong_hands(self):
        """Test that strong hands are correctly categorized."""
        strong_notations = ["JJ", "TT", "AKo", "AQs"]
        for notation in strong_notations:
            hand = StartingHands.from_notation(notation)
            category = StartingHands.get_category(hand)
            assert category == HandCategory.STRONG, f"{notation} should be strong"

    def test_weak_hands(self):
        """Test that weak hands are correctly categorized."""
        hand = StartingHands.from_notation("72o")
        category = StartingHands.get_category(hand)
        assert category == HandCategory.WEAK

    def test_from_cards_suited(self):
        """Test creating starting hand from suited cards."""
        card1 = Card(Rank.ACE, Suit.HEARTS)
        card2 = Card(Rank.KING, Suit.HEARTS)
        hand = StartingHands.from_cards(card1, card2)

        assert hand.card1 == "A"
        assert hand.card2 == "K"
        assert hand.suited is True
        assert hand.notation == "AKs"

    def test_from_cards_offsuit(self):
        """Test creating starting hand from offsuit cards."""
        card1 = Card(Rank.ACE, Suit.HEARTS)
        card2 = Card(Rank.KING, Suit.SPADES)
        hand = StartingHands.from_cards(card1, card2)

        assert hand.notation == "AKo"

    def test_from_cards_pocket_pair(self):
        """Test creating starting hand from pocket pair."""
        card1 = Card(Rank.ACE, Suit.HEARTS)
        card2 = Card(Rank.ACE, Suit.SPADES)
        hand = StartingHands.from_cards(card1, card2)

        assert hand.notation == "AA"

    def test_from_notation_pocket_pair(self):
        """Test parsing pocket pair notation."""
        hand = StartingHands.from_notation("QQ")
        assert hand.card1 == "Q"
        assert hand.card2 == "Q"
        assert hand.suited is False

    def test_from_notation_suited(self):
        """Test parsing suited hand notation."""
        hand = StartingHands.from_notation("AKs")
        assert hand.card1 == "A"
        assert hand.card2 == "K"
        assert hand.suited is True

    def test_from_notation_offsuit(self):
        """Test parsing offsuit hand notation."""
        hand = StartingHands.from_notation("AKo")
        assert hand.card1 == "A"
        assert hand.card2 == "K"
        assert hand.suited is False

    def test_should_play_premium_early(self):
        """Test that premium hands should be played from early position."""
        hand = StartingHands.from_notation("AA")
        assert StartingHands.should_play(hand, "early") is True

    def test_should_not_play_weak_early(self):
        """Test that weak hands should not be played from early position."""
        hand = StartingHands.from_notation("72o")
        assert StartingHands.should_play(hand, "early") is False

    def test_generate_random_premium(self):
        """Test generating a random premium hand."""
        hand, cards = StartingHands.generate_random(HandCategory.PREMIUM)
        assert hand.notation in StartingHands.PREMIUM
        assert len(cards) == 2

    def test_get_chart(self):
        """Test getting the full starting hands chart."""
        chart = StartingHands.get_chart()
        assert len(chart) > 0

        # Check structure
        first_hand = chart[0]
        assert "notation" in first_hand
        assert "category" in first_hand
        assert "category_name" in first_hand

    def test_category_names(self):
        """Test that all categories have proper names."""
        for category in HandCategory:
            name = StartingHands.get_category_name(category)
            assert name is not None
            assert len(name) > 0
