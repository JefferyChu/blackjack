import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blackjack_game.class_def import Card


class TestCard:

    def test_card_initialization(self):
        card = Card(5, 5, 'hearts', 5)
        assert card.value1 == 5
        assert card.value2 == 5
        assert card.suit == 'hearts'
        assert card.indexvalue == 5

    def test_ace_card_initialization(self):
        ace = Card(1, 11, 'spades', 1)
        assert ace.value1 == 1
        assert ace.value2 == 11
        assert ace.suit == 'spades'
        assert ace.indexvalue == 1

    def test_face_card_initialization(self):
        king = Card(10, 10, 'diamonds', 13)
        assert king.value1 == 10
        assert king.value2 == 10
        assert king.suit == 'diamonds'
        assert king.indexvalue == 13

    def test_card_str_representation(self):
        card = Card(7, 7, 'clubs', 7)
        expected = "This card has values 7 and 7 and is of suit clubs"
        assert str(card) == expected

    def test_ace_str_representation(self):
        ace = Card(1, 11, 'hearts', 1)
        expected = "This card has values 1 and 11 and is of suit hearts"
        assert str(ace) == expected

    def test_different_suits(self):
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        for suit in suits:
            card = Card(5, 5, suit, 5)
            assert card.suit == suit

    def test_card_values_range(self):
        # Test all possible card values
        for value in range(1, 14):
            if value == 1:  # Ace
                card = Card(1, 11, 'hearts', 1)
                assert card.value1 == 1 and card.value2 == 11
            elif value > 10:  # Face cards
                card = Card(10, 10, 'hearts', value)
                assert card.value1 == 10 and card.value2 == 10
            else:  # Number cards
                card = Card(value, value, 'hearts', value)
                assert card.value1 == value and card.value2 == value