"""Question generation for training sessions."""

import uuid
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from app.engine.card import Card, Deck, parse_cards
from app.engine.hand_rankings import HandRank, get_all_rankings
from app.engine.hand_evaluator import HandEvaluator, EvaluatedHand
from app.engine.starting_hands import StartingHands, HandCategory


@dataclass
class GeneratedQuestion:
    """A generated training question."""

    question_id: str
    question_type: str
    prompt: str
    cards: List[Card]
    cards2: Optional[List[Card]]
    choices: List[str]
    correct_answer: str
    explanation: str
    difficulty: int
    question_data: Dict


class QuestionGenerator:
    """Generates training questions of various types."""

    QUESTION_TYPES = ["hand_ranking", "which_wins", "starting_hand"]

    POSITIONS = ["early", "middle", "late", "blinds"]

    @classmethod
    def generate(cls, question_type: str, difficulty: int = 1) -> GeneratedQuestion:
        """Generate a question of the specified type."""
        generators = {
            "hand_ranking": cls._generate_hand_ranking_question,
            "which_wins": cls._generate_which_wins_question,
            "starting_hand": cls._generate_starting_hand_question,
        }

        if question_type not in generators:
            raise ValueError(f"Unknown question type: {question_type}")

        return generators[question_type](difficulty)

    @classmethod
    def generate_random(
        cls, difficulty: int = 1, exclude_types: List[str] = None
    ) -> GeneratedQuestion:
        """Generate a random question type."""
        types = [t for t in cls.QUESTION_TYPES if t not in (exclude_types or [])]
        question_type = random.choice(types)
        return cls.generate(question_type, difficulty)

    @classmethod
    def _generate_hand_ranking_question(cls, difficulty: int) -> GeneratedQuestion:
        """
        Generate a 'What hand is this?' question.
        Higher difficulty = less obvious hands.
        """
        question_id = str(uuid.uuid4())

        # Select hand type based on difficulty
        if difficulty <= 2:
            # Easy: obvious hands (pairs, straights, flushes, full houses)
            target_ranks = [
                HandRank.ONE_PAIR,
                HandRank.TWO_PAIR,
                HandRank.THREE_OF_A_KIND,
                HandRank.STRAIGHT,
                HandRank.FLUSH,
                HandRank.FULL_HOUSE,
            ]
        elif difficulty <= 4:
            # Medium: include high card and quads
            target_ranks = list(HandRank)
        else:
            # Hard: focus on tricky cases
            target_ranks = [
                HandRank.HIGH_CARD,
                HandRank.ONE_PAIR,
                HandRank.TWO_PAIR,
                HandRank.STRAIGHT,
                HandRank.FLUSH,
            ]

        target_rank = random.choice(target_ranks)
        cards = cls._generate_hand_of_rank(target_rank)

        # Generate choices (always include correct answer)
        all_ranks = [r.display_name for r in HandRank]
        choices = [target_rank.display_name]

        # Add plausible wrong answers
        nearby_ranks = [
            r
            for r in HandRank
            if abs(r.value - target_rank.value) <= 2 and r != target_rank
        ]
        for r in random.sample(nearby_ranks, min(2, len(nearby_ranks))):
            choices.append(r.display_name)

        # Fill remaining slots
        while len(choices) < 4:
            r = random.choice(list(HandRank))
            if r.display_name not in choices:
                choices.append(r.display_name)

        random.shuffle(choices)

        return GeneratedQuestion(
            question_id=question_id,
            question_type="hand_ranking",
            prompt="What hand is this?",
            cards=cards,
            cards2=None,
            choices=choices,
            correct_answer=target_rank.display_name,
            explanation=f"This is a {target_rank.display_name}. {target_rank.description}",
            difficulty=difficulty,
            question_data={
                "target_rank": target_rank.value,
                "cards": [str(c) for c in cards],
            },
        )

    @classmethod
    def _generate_which_wins_question(cls, difficulty: int) -> GeneratedQuestion:
        """
        Generate a 'Which hand wins?' question.
        Higher difficulty = closer hand strengths.
        """
        question_id = str(uuid.uuid4())

        if difficulty <= 2:
            # Easy: different hand ranks
            rank1 = random.choice(
                [HandRank.ONE_PAIR, HandRank.TWO_PAIR, HandRank.FLUSH]
            )
            rank2_options = [r for r in HandRank if abs(r.value - rank1.value) >= 2]
            rank2 = (
                random.choice(rank2_options) if rank2_options else HandRank.HIGH_CARD
            )
        else:
            # Hard: same rank, different kickers
            rank1 = random.choice(list(HandRank))
            rank2 = rank1

        cards1 = cls._generate_hand_of_rank(rank1)
        cards2 = cls._generate_hand_of_rank(rank2, exclude_cards=cards1)

        eval1 = HandEvaluator.evaluate(cards1)
        eval2 = HandEvaluator.evaluate(cards2)

        if eval1 > eval2:
            correct = "Hand 1"
            explanation = f"Hand 1 ({eval1.rank.display_name}) beats Hand 2 ({eval2.rank.display_name})"
        elif eval2 > eval1:
            correct = "Hand 2"
            explanation = f"Hand 2 ({eval2.rank.display_name}) beats Hand 1 ({eval1.rank.display_name})"
        else:
            correct = "Tie"
            explanation = f"Both hands are {eval1.rank.display_name} with equal kickers - it's a tie!"

        choices = ["Hand 1", "Hand 2", "Tie"]

        return GeneratedQuestion(
            question_id=question_id,
            question_type="which_wins",
            prompt="Which hand wins?",
            cards=cards1,
            cards2=cards2,
            choices=choices,
            correct_answer=correct,
            explanation=explanation,
            difficulty=difficulty,
            question_data={
                "cards1": [str(c) for c in cards1],
                "cards2": [str(c) for c in cards2],
                "eval1": eval1.rank.value,
                "eval2": eval2.rank.value,
            },
        )

    @classmethod
    def _generate_starting_hand_question(cls, difficulty: int) -> GeneratedQuestion:
        """
        Generate a starting hand question.
        Higher difficulty = marginal hands, position-dependent.
        """
        question_id = str(uuid.uuid4())

        # Select category based on difficulty
        if difficulty <= 2:
            # Easy: premium and strong hands
            categories = [HandCategory.PREMIUM, HandCategory.STRONG, HandCategory.WEAK]
        elif difficulty <= 4:
            # Medium: include playable
            categories = [
                HandCategory.PLAYABLE,
                HandCategory.MARGINAL,
                HandCategory.WEAK,
            ]
        else:
            # Hard: marginal hands only
            categories = [HandCategory.MARGINAL, HandCategory.WEAK]

        category = random.choice(categories)
        hand, cards = StartingHands.generate_random(category)

        # Position-based question for higher difficulty
        if difficulty >= 3:
            position = random.choice(cls.POSITIONS)
            should_play = StartingHands.should_play(hand, position)
            prompt = f"Should you play {hand.notation} from {position} position?"
            choices = ["Play", "Fold"]
            correct = "Play" if should_play else "Fold"

            category_name = StartingHands.get_category_name(category)
            if should_play:
                explanation = f"{hand.notation} is a {category_name} hand, playable from {position} position."
            else:
                explanation = f"{hand.notation} is a {category_name} hand, too weak for {position} position."
        else:
            # Simple strength classification
            prompt = f"How strong is {hand.notation}?"
            choices = ["Premium", "Strong", "Playable", "Marginal", "Weak"]
            correct = StartingHands.get_category_name(category)
            explanation = (
                f"{hand.notation} is categorized as a {correct} starting hand."
            )
            position = None

        return GeneratedQuestion(
            question_id=question_id,
            question_type="starting_hand",
            prompt=prompt,
            cards=cards,
            cards2=None,
            choices=choices,
            correct_answer=correct,
            explanation=explanation,
            difficulty=difficulty,
            question_data={
                "notation": hand.notation,
                "category": category.value,
                "position": position,
                "cards": [str(c) for c in cards],
            },
        )

    @classmethod
    def _generate_hand_of_rank(
        cls, target_rank: HandRank, exclude_cards: List[Card] = None
    ) -> List[Card]:
        """Generate 5 cards that form a specific hand rank."""
        deck = Deck()
        if exclude_cards:
            for card in exclude_cards:
                if card in deck.cards:
                    deck.cards.remove(card)

        # Generate hands until we get the target rank
        max_attempts = 100
        for _ in range(max_attempts):
            deck.reset()
            if exclude_cards:
                for card in exclude_cards:
                    if card in deck.cards:
                        deck.cards.remove(card)

            if target_rank == HandRank.ROYAL_FLUSH:
                cards = cls._make_royal_flush(deck)
            elif target_rank == HandRank.STRAIGHT_FLUSH:
                cards = cls._make_straight_flush(deck)
            elif target_rank == HandRank.FOUR_OF_A_KIND:
                cards = cls._make_four_of_a_kind(deck)
            elif target_rank == HandRank.FULL_HOUSE:
                cards = cls._make_full_house(deck)
            elif target_rank == HandRank.FLUSH:
                cards = cls._make_flush(deck)
            elif target_rank == HandRank.STRAIGHT:
                cards = cls._make_straight(deck)
            elif target_rank == HandRank.THREE_OF_A_KIND:
                cards = cls._make_three_of_a_kind(deck)
            elif target_rank == HandRank.TWO_PAIR:
                cards = cls._make_two_pair(deck)
            elif target_rank == HandRank.ONE_PAIR:
                cards = cls._make_one_pair(deck)
            else:  # HIGH_CARD
                cards = cls._make_high_card(deck)

            if cards:
                eval_result = HandEvaluator.evaluate(cards)
                if eval_result.rank == target_rank:
                    return cards

        # Fallback: just draw 5 cards
        deck.reset()
        return deck.draw(5)

    @classmethod
    def _make_royal_flush(cls, deck: Deck) -> List[Card]:
        """Create a royal flush."""
        from app.engine.card import Suit, Rank

        suit = random.choice(list(Suit))
        cards = [
            Card(Rank.ACE, suit),
            Card(Rank.KING, suit),
            Card(Rank.QUEEN, suit),
            Card(Rank.JACK, suit),
            Card(Rank.TEN, suit),
        ]
        return cards

    @classmethod
    def _make_straight_flush(cls, deck: Deck) -> List[Card]:
        """Create a straight flush (not royal)."""
        from app.engine.card import Suit, Rank

        suit = random.choice(list(Suit))
        high_rank = random.randint(5, 9)  # 5-high to 9-high
        cards = [Card(Rank(r), suit) for r in range(high_rank, high_rank - 5, -1)]
        return cards

    @classmethod
    def _make_four_of_a_kind(cls, deck: Deck) -> List[Card]:
        """Create four of a kind."""
        from app.engine.card import Suit, Rank

        quad_rank = random.choice(list(Rank))
        cards = [Card(quad_rank, suit) for suit in Suit]
        # Add kicker
        kicker_rank = random.choice([r for r in Rank if r != quad_rank])
        cards.append(Card(kicker_rank, random.choice(list(Suit))))
        return cards[:5]

    @classmethod
    def _make_full_house(cls, deck: Deck) -> List[Card]:
        """Create a full house."""
        from app.engine.card import Suit, Rank

        trips_rank = random.choice(list(Rank))
        pair_rank = random.choice([r for r in Rank if r != trips_rank])
        suits = list(Suit)
        random.shuffle(suits)
        cards = [Card(trips_rank, suits[i]) for i in range(3)]
        cards.extend([Card(pair_rank, suits[i]) for i in range(2)])
        return cards

    @classmethod
    def _make_flush(cls, deck: Deck) -> List[Card]:
        """Create a flush (not straight)."""
        from app.engine.card import Suit, Rank

        suit = random.choice(list(Suit))
        # Pick 5 non-consecutive ranks
        available_ranks = list(Rank)
        random.shuffle(available_ranks)
        ranks = sorted(available_ranks[:5], reverse=True)
        # Ensure not a straight
        while ranks[0].value - ranks[4].value == 4:
            random.shuffle(available_ranks)
            ranks = sorted(available_ranks[:5], reverse=True)
        cards = [Card(r, suit) for r in ranks]
        return cards

    @classmethod
    def _make_straight(cls, deck: Deck) -> List[Card]:
        """Create a straight (not flush)."""
        from app.engine.card import Suit, Rank

        high_rank = random.randint(5, 14)  # 5-high (wheel) to A-high
        if high_rank == 14:
            ranks = [14, 13, 12, 11, 10]
        elif high_rank == 5:
            ranks = [5, 4, 3, 2, 14]  # Wheel with ace
        else:
            ranks = list(range(high_rank, high_rank - 5, -1))

        suits = list(Suit)
        # Ensure not all same suit
        card_suits = [random.choice(suits) for _ in range(5)]
        while len(set(card_suits)) == 1:
            card_suits = [random.choice(suits) for _ in range(5)]

        cards = [Card(Rank(r), s) for r, s in zip(ranks, card_suits)]
        return cards

    @classmethod
    def _make_three_of_a_kind(cls, deck: Deck) -> List[Card]:
        """Create three of a kind."""
        from app.engine.card import Suit, Rank

        trips_rank = random.choice(list(Rank))
        suits = list(Suit)
        random.shuffle(suits)
        cards = [Card(trips_rank, suits[i]) for i in range(3)]

        # Add 2 kickers (different ranks, not making a pair)
        other_ranks = [r for r in Rank if r != trips_rank]
        random.shuffle(other_ranks)
        cards.append(Card(other_ranks[0], random.choice(suits)))
        cards.append(Card(other_ranks[1], random.choice(suits)))
        return cards

    @classmethod
    def _make_two_pair(cls, deck: Deck) -> List[Card]:
        """Create two pair."""
        from app.engine.card import Suit, Rank

        ranks = random.sample(list(Rank), 3)
        pair1_rank, pair2_rank, kicker_rank = ranks[0], ranks[1], ranks[2]
        suits = list(Suit)
        random.shuffle(suits)

        cards = [
            Card(pair1_rank, suits[0]),
            Card(pair1_rank, suits[1]),
            Card(pair2_rank, suits[2]),
            Card(pair2_rank, suits[3]),
            Card(kicker_rank, random.choice(suits)),
        ]
        return cards

    @classmethod
    def _make_one_pair(cls, deck: Deck) -> List[Card]:
        """Create one pair."""
        from app.engine.card import Suit, Rank

        pair_rank = random.choice(list(Rank))
        suits = list(Suit)
        random.shuffle(suits)
        cards = [Card(pair_rank, suits[0]), Card(pair_rank, suits[1])]

        # Add 3 different kickers
        other_ranks = [r for r in Rank if r != pair_rank]
        random.shuffle(other_ranks)
        for i in range(3):
            cards.append(Card(other_ranks[i], random.choice(suits)))
        return cards

    @classmethod
    def _make_high_card(cls, deck: Deck) -> List[Card]:
        """Create a high card hand (no pairs, no straight, no flush)."""
        from app.engine.card import Suit, Rank

        # Pick 5 different non-consecutive ranks
        available_ranks = list(Rank)
        random.shuffle(available_ranks)
        ranks = sorted(available_ranks[:5], reverse=True)

        # Ensure not a straight
        while ranks[0].value - ranks[4].value == 4 or set(ranks) == {14, 5, 4, 3, 2}:
            random.shuffle(available_ranks)
            ranks = sorted(available_ranks[:5], reverse=True)

        suits = list(Suit)
        # Ensure not all same suit
        card_suits = [random.choice(suits) for _ in range(5)]
        while len(set(card_suits)) == 1:
            card_suits = [random.choice(suits) for _ in range(5)]

        cards = [Card(Rank(r), s) for r, s in zip(ranks, card_suits)]
        return cards
