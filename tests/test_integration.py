import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blackjack_game.class_def import Card, CardOperations, Player
# Import play_round function directly since it has import issues
# from blackjack_game.blackjack import play_round


class TestGameIntegration:

    def setup_method(self):
        self.player = Player('Test Player', 5000)
        self.dealer = Player('Dealer', 1000000)
        self.card_ops = CardOperations()

    def test_full_deck_integration(self):
        deck = self.card_ops.deck_generator()

        # Test that deck contains all expected cards
        assert len(deck) == 52

        # Test that we can draw all cards
        original_deck_length = len(deck)
        for i in range(52):
            self.player, deck = self.card_ops.take_1_card(self.player, deck)
            assert len(deck) == original_deck_length - (i + 1)
            assert len(self.player.hand) == i + 1

    def test_initial_turn_integration(self):
        deck = self.card_ops.deck_generator()

        player, dealer, new_deck = self.card_ops.take_initial_turn(
            self.player, self.dealer, deck
        )

        # Both players should have 2 cards
        assert len(player.hand) == 2
        assert len(dealer.hand) == 2

        # Deck should have 4 fewer cards
        assert len(new_deck) == 48

        # Each card should be valid
        for hand in [player.hand, dealer.hand]:
            for card_pair in hand:
                assert isinstance(card_pair, tuple)
                assert len(card_pair) == 2
                assert isinstance(card_pair[1], Card)

    def test_hand_value_calculation_scenarios(self):
        # Test blackjack scenario
        blackjack_hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),    # Ace
            ('clubs13', Card(10, 10, 'clubs', 13))    # King
        ]
        assert self.card_ops.cal_hand_value(blackjack_hand) == 21

        # Test soft 17 scenario
        soft_17_hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),    # Ace
            ('clubs6', Card(6, 6, 'clubs', 6))        # 6
        ]
        assert self.card_ops.cal_hand_value(soft_17_hand) == 17

        # Test hard 17 scenario
        hard_17_hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),   # 10
            ('hearts7', Card(7, 7, 'hearts', 7))      # 7
        ]
        assert self.card_ops.cal_hand_value(hard_17_hand) == 17

    def test_bust_detection_integration(self):
        # Create a busting hand
        self.player.hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),   # 10
            ('hearts10', Card(10, 10, 'hearts', 10)), # 10
            ('spades5', Card(5, 5, 'spades', 5))      # 5
        ]
        self.player.bet_amount = 100

        with patch('builtins.print'):
            result = self.card_ops.check_bust(self.player)

        assert result == 'bust'
        assert self.player.balance == 4900  # Lost 100

    def test_ace_handling_complex_scenarios(self):
        # Multiple aces with different outcomes
        test_cases = [
            # (hand_cards, expected_value)
            ([('hearts1', Card(1, 11, 'hearts', 1)),
              ('clubs1', Card(1, 11, 'clubs', 1)),
              ('spades9', Card(9, 9, 'spades', 9))], 21),  # A,A,9 = 21

            ([('hearts1', Card(1, 11, 'hearts', 1)),
              ('clubs1', Card(1, 11, 'clubs', 1)),
              ('spades10', Card(10, 10, 'spades', 10))], 12),  # A,A,10 = 12 (both aces as 1)

            ([('hearts1', Card(1, 11, 'hearts', 1)),
              ('clubs5', Card(5, 5, 'clubs', 5)),
              ('spades5', Card(5, 5, 'spades', 5))], 21),  # A,5,5 = 21
        ]

        for hand, expected_value in test_cases:
            actual_value = self.card_ops.cal_hand_value(hand)
            assert actual_value == expected_value

    def test_complete_game_simulation(self):
        # Test a complete game scenario without importing blackjack.py
        deck = self.card_ops.deck_generator()

        # Clear hands
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.player.bet_amount = 100

        # Deal initial cards
        player, dealer, deck = self.card_ops.take_initial_turn(
            self.player, self.dealer, deck
        )

        # Simulate player standing (no additional cards)
        # Simulate dealer playing according to rules
        with patch('builtins.print'):
            if self.card_ops.cal_hand_value(dealer.hand) < 17:
                # Dealer hits until 17 or higher
                while self.card_ops.cal_hand_value(dealer.hand) < 17:
                    dealer, deck = self.card_ops.take_1_card(dealer, deck)

            # Determine winner
            self.card_ops.determine_winner(player, dealer)

        # Verify game state is consistent
        assert len(player.hand) >= 2
        assert len(dealer.hand) >= 2
        assert len(deck) < 52