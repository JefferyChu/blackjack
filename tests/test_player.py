import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blackjack_game.class_def import Player, Card


class TestPlayer:

    def test_player_initialization(self):
        player = Player('John', 1000)
        assert player.name == 'John'
        assert player.balance == 1000
        assert player.hand == []
        assert player.bet_amount == 0

    def test_player_initialization_zero_balance(self):
        player = Player('Broke Player', 0)
        assert player.name == 'Broke Player'
        assert player.balance == 0

    def test_player_initialization_negative_balance(self):
        player = Player('Debtor', -500)
        assert player.name == 'Debtor'
        assert player.balance == -500

    def test_balance_change_positive(self):
        player = Player('Winner', 1000)
        player.balance_change(500)
        assert player.balance == 1500

    def test_balance_change_negative(self):
        player = Player('Loser', 1000)
        player.balance_change(-300)
        assert player.balance == 700

    def test_balance_change_zero(self):
        player = Player('Neutral', 1000)
        original_balance = player.balance
        player.balance_change(0)
        assert player.balance == original_balance

    def test_balance_change_large_amounts(self):
        player = Player('High Roller', 10000)
        player.balance_change(50000)
        assert player.balance == 60000

        player.balance_change(-75000)
        assert player.balance == -15000

    def test_clear_hand_empty_hand(self):
        player = Player('Empty', 1000)
        player.clear_hand()
        assert player.hand == []
        assert player.bet_amount == 0

    def test_clear_hand_with_cards(self):
        player = Player('Card Holder', 1000)
        # Add some cards to hand
        player.hand = [
            ('clubs7', Card(7, 7, 'clubs', 7)),
            ('hearts5', Card(5, 5, 'hearts', 5))
        ]
        player.bet_amount = 100

        player.clear_hand()

        assert player.hand == []
        assert player.bet_amount == 0

    def test_clear_hand_preserves_other_attributes(self):
        player = Player('Persistent', 2000)
        original_name = player.name
        original_balance = player.balance

        player.hand = [('clubs7', Card(7, 7, 'clubs', 7))]
        player.bet_amount = 250

        player.clear_hand()

        assert player.name == original_name
        assert player.balance == original_balance

    def test_multiple_balance_changes(self):
        player = Player('Gambler', 1000)

        # Simulate multiple wins and losses
        player.balance_change(200)  # Win
        assert player.balance == 1200

        player.balance_change(-150)  # Loss
        assert player.balance == 1050

        player.balance_change(500)  # Big win
        assert player.balance == 1550

        player.balance_change(-1550)  # Lose everything
        assert player.balance == 0

    def test_hand_manipulation(self):
        player = Player('Card Collector', 1000)

        # Add cards directly to hand
        card1 = ('clubs7', Card(7, 7, 'clubs', 7))
        card2 = ('hearts10', Card(10, 10, 'hearts', 10))

        player.hand.append(card1)
        assert len(player.hand) == 1

        player.hand.append(card2)
        assert len(player.hand) == 2

        assert player.hand[0] == card1
        assert player.hand[1] == card2

    def test_bet_amount_setting(self):
        player = Player('Bettor', 1000)

        player.bet_amount = 50
        assert player.bet_amount == 50

        player.bet_amount = 500
        assert player.bet_amount == 500

        player.bet_amount = 0
        assert player.bet_amount == 0

    def test_dealer_creation(self):
        dealer = Player('Dealer', 1000000)
        assert dealer.name == 'Dealer'
        assert dealer.balance == 1000000
        assert dealer.hand == []
        assert dealer.bet_amount == 0

    def test_player_equality_by_attributes(self):
        player1 = Player('Test', 1000)
        player2 = Player('Test', 1000)

        # They should have same attributes but be different objects
        assert player1.name == player2.name
        assert player1.balance == player2.balance
        assert player1.hand == player2.hand
        assert player1.bet_amount == player2.bet_amount
        assert player1 is not player2

    def test_player_state_independence(self):
        player1 = Player('Player1', 1000)
        player2 = Player('Player2', 1000)

        # Modify player1
        player1.balance_change(500)
        player1.bet_amount = 100
        player1.hand.append(('clubs7', Card(7, 7, 'clubs', 7)))

        # player2 should be unaffected
        assert player2.balance == 1000
        assert player2.bet_amount == 0
        assert player2.hand == []