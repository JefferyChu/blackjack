import random

# Creation of Deck Cards class

class Card:
    
    def __init__(self, value1, value2, suit, indexvalue):
        self.value1 = value1
        self.value2 = value2
        self.suit = suit
        self.indexvalue = indexvalue
        
    def __str__(self):
        return f"This card has values {self.value1} and {self.value2} and is of suit {self.suit}"

class CardOperations:

    def __init__(self):
        self.test = 'test'

    def deck_generator(self):
        """ Deck Generator function. Generates deck dictionary with 52 Card instances. """
        
        deck_dict = {}
        suits = ['clubs','diamonds','hearts','spades']
        
        for suit in suits:
            for x in range(1, 14):
                # If Ace, possible values can be '1' or '11'
                if x == 1:
                    deck_dict['{}{}'.format(suit, x)] = Card(x, 11, suit, x)
                # For Jacks, Queens and Kings, possible value is '10'
                elif x > 10:
                    deck_dict['{}{}'.format(suit, x)] = Card(10, 10, suit, x)
                # For all other cards, face value is only possible value
                else:
                    deck_dict['{}{}'.format(suit, x)] = Card(x, x, suit, x)

        return list(deck_dict.items())

    def take_1_card(self, hand_to_update, deck_list):
        """ Simulate taking 1 card. """
        
        num_picked = random.randint(0, len(deck_list) - 1)
        card_picked = deck_list[num_picked]
        del deck_list[num_picked]
        hand_to_update.append(card_picked)
        
        return hand_to_update, deck_list

    def take_one_turn(self, player1_hand, dealer_hand, deck_list):
        """ Simulate initial turn. """

        dist_counter = 0

        # Distribute first 2 cards to player and dealer
        while dist_counter < 2:
            
            # Take 1 card for player
            player1_hand, deck_list = self.take_1_card(player1_hand, deck_list)
            print('Player 1 hand: ', player1_hand, '\nCurrent deck len: ', len(deck_list))
            
            # Take 1 card for dealer
            dealer_hand, deck_list = self.take_1_card(dealer_hand, deck_list)
            print('Dealer hand: ', dealer_hand, '\nCurrent deck len: ', len(deck_list))
            
            dist_counter += 1

        print('End of initial distribution.')

        return player1_hand, dealer_hand, deck_list

    def cal_hand_value(self, hand):
        """ Calculate hand value. """

        hand_value1 = 0
        hand_value2 = 0
        
        for pair in hand:
            hand_value1 += pair[1].value1
            
            # To account for 2 aces, take the lower value to prevent 22 value
            if hand_value2 + pair[1].value2 > 21:
                hand_value2 += pair[1].value1
            else:
                hand_value2 += pair[1].value2
        
        return hand_value1, hand_value2

    def display_hand(self, player, hand, cal_hand_value, deck_list):
        """ Display hand. """

        print('\n{}\'s hand: '.format(player.name))
        
        for pair in hand:
            if pair[1].indexvalue == 1:
                print(pair[1].value1,'- Ace of {}'.format(pair[1].suit))
            elif pair[1].indexvalue == 11:
                print(pair[1].value1,'- Jack of {}'.format(pair[1].suit))
            elif pair[1].indexvalue == 12:
                print(pair[1].value1,'- Queen of {}'.format(pair[1].suit))
            elif pair[1].indexvalue == 13:
                print(pair[1].value1,'- King of {}'.format(pair[1].suit))
            else:
                print(pair[1].value1,'of {}'.format(pair[1].suit))
        
        print(f'\nCurrent hand values are {cal_hand_value(hand)}')
        print(f'\nCurrent deck len: {len(deck_list)}')

# Creation of Player class

class Player:
    """ Player class that can be instantiated for a player or the house. """

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.deck = []

    def balance_change(self, winnings):
        self.balance = self.balance + winnings
