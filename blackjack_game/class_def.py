import random

# Change from feature
# Hello there from feature

# Creation of the deck's Card class
class Card:
    """ Class for card methods and attributes. """

    def __init__(self, value1, value2, suit, indexvalue):
        self.value1 = value1
        self.value2 = value2
        self.suit = suit
        self.indexvalue = indexvalue
        
    def __str__(self):
        return f"This card has values {self.value1} and {self.value2} and is of suit {self.suit}"


# Creation of the CardOperations class
class CardOperations:
    """ Class for card operation methods and attributes. """
    
    @staticmethod
    def deck_generator():
        """ Generates deck dictionary with 52 Card instances. """
        
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
    
    @staticmethod
    def take_1_card(player, deck_list):
        """ Take 1 card from deck. """
        
        print(f'\n{player.name} draws a card...')
        num_picked = random.randint(0, len(deck_list) - 1)
        card_picked = deck_list[num_picked]
        del deck_list[num_picked]
        player.hand.append(card_picked)
        
        return player, deck_list

    def take_initial_turn(self, player, dealer, deck_list):
        """ Distribute initial 2 cards to dealer and player. """

        dist_counter = 0

        # Distribute first 2 cards to player and dealer
        while dist_counter < 2:
            
            # Take 1 card for player
            player, deck_list = self.take_1_card(player, deck_list)
            print(f'{player.name} hand: {[pair[0] for pair in player.hand]}\nCurrent deck len: {len(deck_list)}')
            
            # Take 1 card for dealer, showing only the first drawn card
            dealer, deck_list = self.take_1_card(dealer, deck_list)
            if dist_counter == 0:
                print(f'{dealer.name} hand: {[pair[0] for pair in dealer.hand]}\nCurrent deck len: {len(deck_list)}')
            else:
                print(f'Current deck len: {len(deck_list)}')

            dist_counter += 1
        
        print('\nEnd of initial distribution.')

        return player, dealer, deck_list
    
    @staticmethod
    def cal_hand_value(hand):
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
    
    def check_bust(self, player):
        """ Checks if player hand is a bust. """

        if min(self.cal_hand_value(player.hand)) > 21:
            print(f'\nUnfortunate! Busted with a hand value of {min(self.cal_hand_value(player.hand))}.')
            print('Dealer: "Hahaha, your money is safer with us!"')
            self.update_balance(player, 'lose')
            return 'bust'
        else:
            return 'safe'
    
    def display_hand(self, player, deck_list):
        """ Display hand. """

        print('\n{}\'s hand: '.format(player.name))
        
        for pair in player.hand:
            if pair[1].indexvalue == 1:
                print(f"{pair[1].value1} - Ace of {pair[1].suit}")
            elif pair[1].indexvalue == 11:
                print(f"{pair[1].value1} - Jack of {pair[1].suit}")
            elif pair[1].indexvalue == 12:
                print(f"{pair[1].value1} - Queen of {pair[1].suit}")
            elif pair[1].indexvalue == 13:
                print(f"{pair[1].value1} - King of {pair[1].suit}")
            else:
                print(f"{pair[1].value1} - {pair[1].suit}")
        
        print(f'\n{player.name} hand values are {self.cal_hand_value(player.hand)}')
        print(f'\nCurrent deck len: {len(deck_list)}')
    
    def update_balance(self, player, status='lose'):
        """ Update the player's balance. """

        print('\nYour previous balance was: ', player.balance)
        
        if status == 'lose':
            player.balance_change(-player.bet_amount)
            print('Your balance is now:', player.balance)
        elif status == 'win':
            player.balance_change(2 * player.bet_amount)
            print('Your balance is now:', player.balance)
        else:
            print(f'{player.name} balance remains unchanged at: {player.balance}')

    def dealer_turn(self, player, dealer, deck_list):
        """ Dealer's turn after player has completed their turn. """

        # Dealer will HIT on less than 17, otherwise STAND
        while max(self.cal_hand_value(dealer.hand)) < 17:
            dealer, deck_list = self.take_1_card(dealer, deck_list)
            self.display_hand(dealer, deck_list)

        if max(self.cal_hand_value(dealer.hand)) > 21:
            while min(self.cal_hand_value(dealer.hand)) < 17:
                dealer, deck_list = self.take_1_card(dealer, deck_list)
                self.display_hand(dealer, deck_list)
        
        # Compare dealer and player hands and determine outcome
        
        # Check if dealer bust, otherwise check who wins
        if min(self.cal_hand_value(dealer.hand)) > 21:
            print(f'\n{dealer.name} busted! {player.name} wins!')
            print(f'{dealer.name}: "Nooooooo!"')
            self.update_balance(player, 'win')
        else:
            player_final_value = 0
            dealer_final_value = 0
            
            # Checks Player's max hand value
            if max(self.cal_hand_value(player.hand)) > 21:
                player_final_value = min(self.cal_hand_value(player.hand))
            else: 
                player_final_value = max(self.cal_hand_value(player.hand))
            
            # Checks Dealer's max hand value
            if max(self.cal_hand_value(dealer.hand)) > 21:
                dealer_final_value = min(self.cal_hand_value(dealer.hand))
            else: 
                dealer_final_value = max(self.cal_hand_value(dealer.hand))
                
            # Compares player and dealer hand values and then updates balances
            if dealer_final_value > player_final_value:
                print(f'\n{dealer.name} has the better hand. {dealer.name} wins!')
                print(f'{dealer.name}: "You will always lose against me!"')
                self.update_balance(player, 'lose')
            elif dealer_final_value == player_final_value:
                print('\nDraw!')
                print(f'{dealer.name}: "Let us play again!"')
                self.update_balance(player, 'draw')
            else:
                print(f'\n{player.name} has the better hand. {player.name} wins!')
                print(f'{dealer.name}: "I\'ll get you for this"')
                self.update_balance(player, 'win')


# Creation of Player class
class Player:
    """ Player class that can be instantiated for a player or the dealer. """

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []

    def balance_change(self, winnings):
        self.balance = self.balance + winnings
