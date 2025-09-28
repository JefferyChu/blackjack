import pytest
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blackjack_game.class_def import Card, CardOperations, Player


class TestCardOperations:

    def setup_method(self):
        self.card_ops = CardOperations()
        self.player = Player('Test Player', 1000)
        self.dealer = Player('Dealer', 1000000)

    def test_deck_generator_length(self):
        deck = CardOperations.deck_generator()
        assert len(deck) == 52

    def test_deck_generator_structure(self):
        deck = CardOperations.deck_generator()
        # Check that each item is a tuple with string key and Card object
        for item in deck:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], Card)

    def test_deck_generator_suits(self):
        deck = CardOperations.deck_generator()
        suits = set()
        for item in deck:
            suits.add(item[1].suit)
        expected_suits = {'clubs', 'diamonds', 'hearts', 'spades'}
        assert suits == expected_suits

    def test_deck_generator_card_values(self):
        deck = CardOperations.deck_generator()

        # Count aces, face cards, and number cards
        aces = face_cards = number_cards = 0

        for item in deck:
            card = item[1]
            if card.indexvalue == 1:  # Ace
                aces += 1
                assert card.value1 == 1 and card.value2 == 11
            elif card.indexvalue > 10:  # Face cards
                face_cards += 1
                assert card.value1 == 10 and card.value2 == 10
            else:  # Number cards
                number_cards += 1
                assert card.value1 == card.indexvalue
                assert card.value2 == card.indexvalue

        assert aces == 4  # 4 aces
        assert face_cards == 12  # 4 suits × 3 face cards
        assert number_cards == 36  # 4 suits × 9 number cards

    @patch('random.randint')
    @patch('builtins.print')
    def test_take_1_card(self, mock_print, mock_randint):
        deck = CardOperations.deck_generator()
        original_deck_length = len(deck)
        original_hand_length = len(self.player.hand)

        # Mock random to always pick the first card
        mock_randint.return_value = 0

        player, new_deck = CardOperations.take_1_card(self.player, deck)

        # Check that deck length decreased by 1
        assert len(new_deck) == original_deck_length - 1
        # Check that player hand increased by 1
        assert len(player.hand) == original_hand_length + 1
        # Check that randint was called with correct parameters
        mock_randint.assert_called_once_with(0, original_deck_length - 1)

    @patch('builtins.print')
    def test_take_initial_turn(self, mock_print):
        deck = CardOperations.deck_generator()
        original_deck_length = len(deck)

        player, dealer, new_deck = self.card_ops.take_initial_turn(
            self.player, self.dealer, deck
        )

        # Check that each player has 2 cards
        assert len(player.hand) == 2
        assert len(dealer.hand) == 2
        # Check that deck length decreased by 4
        assert len(new_deck) == original_deck_length - 4

    def test_cal_hand_value_empty_hand(self):
        empty_hand = []
        assert self.card_ops.cal_hand_value(empty_hand) == 0

    def test_cal_hand_value_simple_cards(self):
        # Create hand with 7 and 5
        hand = [
            ('clubs7', Card(7, 7, 'clubs', 7)),
            ('hearts5', Card(5, 5, 'hearts', 5))
        ]
        assert self.card_ops.cal_hand_value(hand) == 12

    def test_cal_hand_value_with_face_cards(self):
        # Create hand with King and Queen
        hand = [
            ('spades13', Card(10, 10, 'spades', 13)),  # King
            ('hearts12', Card(10, 10, 'hearts', 12))   # Queen
        ]
        assert self.card_ops.cal_hand_value(hand) == 20

    def test_cal_hand_value_ace_as_11(self):
        # Ace + 9 = 20 (ace as 11)
        hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),    # Ace
            ('clubs9', Card(9, 9, 'clubs', 9))
        ]
        assert self.card_ops.cal_hand_value(hand) == 20

    def test_cal_hand_value_ace_as_1(self):
        # Ace + King + 5 = 16 (ace as 1)
        hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),    # Ace
            ('clubs13', Card(10, 10, 'clubs', 13)),   # King
            ('spades5', Card(5, 5, 'spades', 5))
        ]
        assert self.card_ops.cal_hand_value(hand) == 16

    def test_cal_hand_value_multiple_aces(self):
        # Two aces + 9 = 21 (one ace as 11, one as 1)
        hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),    # Ace
            ('clubs1', Card(1, 11, 'clubs', 1)),      # Ace
            ('spades9', Card(9, 9, 'spades', 9))
        ]
        assert self.card_ops.cal_hand_value(hand) == 21

    def test_cal_hand_value_multiple_aces_bust_prevention(self):
        # Three aces = 13 (all aces as 1 except one)
        hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),    # Ace
            ('clubs1', Card(1, 11, 'clubs', 1)),      # Ace
            ('spades1', Card(1, 11, 'spades', 1))     # Ace
        ]
        assert self.card_ops.cal_hand_value(hand) == 13

    @patch('builtins.print')
    def test_check_bust_safe_hand(self, mock_print):
        # Create hand with value 18
        self.player.hand = [
            ('clubs9', Card(9, 9, 'clubs', 9)),
            ('hearts9', Card(9, 9, 'hearts', 9))
        ]
        result = self.card_ops.check_bust(self.player)
        assert result == 'safe'

    @patch('builtins.print')
    def test_check_bust_busted_hand(self, mock_print):
        # Create hand with value 25
        self.player.hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),
            ('hearts10', Card(10, 10, 'hearts', 10)),
            ('spades5', Card(5, 5, 'spades', 5))
        ]
        self.player.bet_amount = 100
        result = self.card_ops.check_bust(self.player)
        assert result == 'bust'

    @patch('builtins.print')
    def test_display_hand_normal_cards(self, mock_print):
        self.player.hand = [
            ('clubs7', Card(7, 7, 'clubs', 7)),
            ('hearts5', Card(5, 5, 'hearts', 5))
        ]
        deck = [('test', Card(1, 1, 'test', 1))]  # Dummy deck

        self.card_ops.display_hand(self.player, deck)

        # Check that print was called (we don't test exact content due to formatting)
        assert mock_print.called

    @patch('builtins.print')
    def test_display_hand_with_ace(self, mock_print):
        self.player.hand = [
            ('hearts1', Card(1, 11, 'hearts', 1)),   # Ace
            ('clubs9', Card(9, 9, 'clubs', 9))
        ]
        deck = [('test', Card(1, 1, 'test', 1))]  # Dummy deck

        self.card_ops.display_hand(self.player, deck)

        assert mock_print.called

    @patch('builtins.print')
    def test_display_hand_hide_dealer_card(self, mock_print):
        self.dealer.hand = [
            ('clubs7', Card(7, 7, 'clubs', 7)),
            ('hearts5', Card(5, 5, 'hearts', 5))
        ]
        deck = [('test', Card(1, 1, 'test', 1))]  # Dummy deck

        self.card_ops.display_hand(self.dealer, deck, hide_dealer_card=True)

        assert mock_print.called

    @patch('builtins.print')
    def test_update_balance_win(self, mock_print):
        original_balance = self.player.balance
        self.player.bet_amount = 100

        self.card_ops.update_balance(self.player, 'win')

        assert self.player.balance == original_balance + 200  # 2 * bet

    @patch('builtins.print')
    def test_update_balance_lose(self, mock_print):
        original_balance = self.player.balance
        self.player.bet_amount = 100

        self.card_ops.update_balance(self.player, 'lose')

        assert self.player.balance == original_balance - 100

    @patch('builtins.print')
    def test_update_balance_draw(self, mock_print):
        original_balance = self.player.balance
        self.player.bet_amount = 100

        self.card_ops.update_balance(self.player, 'draw')

        assert self.player.balance == original_balance

    @patch('builtins.print')
    def test_dealer_turn_dealer_stands(self, mock_print):
        # Dealer has 18, should stand
        self.dealer.hand = [
            ('clubs9', Card(9, 9, 'clubs', 9)),
            ('hearts9', Card(9, 9, 'hearts', 9))
        ]
        self.player.hand = [
            ('clubs7', Card(7, 7, 'clubs', 7)),
            ('hearts7', Card(7, 7, 'hearts', 7))
        ]
        deck = [('test', Card(1, 1, 'test', 1))]  # Dummy deck

        original_dealer_cards = len(self.dealer.hand)
        self.card_ops.dealer_turn(self.player, self.dealer, deck)

        # Dealer should not draw additional cards
        assert len(self.dealer.hand) == original_dealer_cards

    def test_determine_winner_player_wins(self):
        # Player has 20, dealer has 18
        self.player.hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),
            ('hearts10', Card(10, 10, 'hearts', 10))
        ]
        self.dealer.hand = [
            ('clubs9', Card(9, 9, 'clubs', 9)),
            ('hearts9', Card(9, 9, 'hearts', 9))
        ]
        self.player.bet_amount = 100
        original_balance = self.player.balance

        with patch('builtins.print'):
            self.card_ops.determine_winner(self.player, self.dealer)

        assert self.player.balance == original_balance + 200

    def test_determine_winner_dealer_wins(self):
        # Player has 18, dealer has 20
        self.player.hand = [
            ('clubs9', Card(9, 9, 'clubs', 9)),
            ('hearts9', Card(9, 9, 'hearts', 9))
        ]
        self.dealer.hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),
            ('hearts10', Card(10, 10, 'hearts', 10))
        ]
        self.player.bet_amount = 100
        original_balance = self.player.balance

        with patch('builtins.print'):
            self.card_ops.determine_winner(self.player, self.dealer)

        assert self.player.balance == original_balance - 100

    def test_determine_winner_draw(self):
        # Both have 19
        self.player.hand = [
            ('clubs9', Card(9, 9, 'clubs', 9)),
            ('hearts10', Card(10, 10, 'hearts', 10))
        ]
        self.dealer.hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),
            ('hearts9', Card(9, 9, 'hearts', 9))
        ]
        self.player.bet_amount = 100
        original_balance = self.player.balance

        with patch('builtins.print'):
            self.card_ops.determine_winner(self.player, self.dealer)

        assert self.player.balance == original_balance

    def test_determine_winner_dealer_bust(self):
        # Player has 18, dealer busts with 22
        self.player.hand = [
            ('clubs9', Card(9, 9, 'clubs', 9)),
            ('hearts9', Card(9, 9, 'hearts', 9))
        ]
        self.dealer.hand = [
            ('clubs10', Card(10, 10, 'clubs', 10)),
            ('hearts10', Card(10, 10, 'hearts', 10)),
            ('spades2', Card(2, 2, 'spades', 2))
        ]
        self.player.bet_amount = 100
        original_balance = self.player.balance

        with patch('builtins.print'):
            self.card_ops.determine_winner(self.player, self.dealer)

        assert self.player.balance == original_balance + 200