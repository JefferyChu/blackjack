import random


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
        """ 
        Calculate hand value with proper Ace handling.
        Returns the best possible hand value (highest without busting, or lowest if all bust).
        """
        if not hand:
            return 0
            
        # Count aces and calculate base value (all aces as 1)
        aces = 0
        total = 0
        
        for pair in hand:
            card = pair[1]
            if card.indexvalue == 1:  # It's an ace
                aces += 1
                total += 1  # Count ace as 1 initially
            else:
                total += card.value1  # Use the primary value
        
        # Try to use one ace as 11 if it doesn't bust
        if aces > 0 and total + 10 <= 21:  # +10 because we change one ace from 1 to 11
            total += 10
            
        return total
    
    def check_bust(self, player):
        """ Checks if player hand is a bust. """

        hand_value = self.cal_hand_value(player.hand)
        if hand_value > 21:
            print(f'\nUnfortunate! Busted with a hand value of {hand_value}.')
            print('Dealer: "Hahaha, your money is safer with us!"')
            self.update_balance(player, 'lose')
            return 'bust'
        else:
            return 'safe'
    
    def display_hand(self, player, deck_list, hide_dealer_card=False):
        """ Display hand. """

        print('\n{}\'s hand: '.format(player.name))
        
        for i, pair in enumerate(player.hand):
            # Hide dealer's second card if specified
            if hide_dealer_card and i == 1 and player.name == 'Dealer':
                print("?? - Hidden card")
                continue
                
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
        
        # Don't show dealer's full hand value if hiding cards
        if not (hide_dealer_card and player.name == 'Dealer'):
            hand_value = self.cal_hand_value(player.hand)
            print(f'\n{player.name} hand value: {hand_value}')
        else:
            # Show only the visible card value for dealer
            visible_value = player.hand[0][1].value1
            print(f'\n{player.name} showing: {visible_value}')
            
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

        print(f"\n{dealer.name}'s full hand revealed:")
        self.display_hand(dealer, deck_list)
        
        # Dealer will HIT on less than 17, otherwise STAND
        while self.cal_hand_value(dealer.hand) < 17:
            print(f"\n{dealer.name} must hit (hand value: {self.cal_hand_value(dealer.hand)})")
            dealer, deck_list = self.take_1_card(dealer, deck_list)
            self.display_hand(dealer, deck_list)
        
        dealer_value = self.cal_hand_value(dealer.hand)
        print(f"\n{dealer.name} stands with hand value: {dealer_value}")
        
        # Compare dealer and player hands and determine outcome
        self.determine_winner(player, dealer)
        
    def determine_winner(self, player, dealer):
        """ Compare hands and determine the winner. """
        
        player_value = self.cal_hand_value(player.hand)
        dealer_value = self.cal_hand_value(dealer.hand)
        
        print(f"\nFinal comparison:")
        print(f"{player.name}: {player_value}")
        print(f"{dealer.name}: {dealer_value}")
        
        # Check if dealer bust
        if dealer_value > 21:
            print(f'\n{dealer.name} busted! {player.name} wins!')
            print(f'{dealer.name}: "Nooooooo!"')
            self.update_balance(player, 'win')
        elif dealer_value > player_value:
            print(f'\n{dealer.name} has the better hand. {dealer.name} wins!')
            print(f'{dealer.name}: "You will always lose against me!"')
            self.update_balance(player, 'lose')
        elif dealer_value == player_value:
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
        self.bet_amount = 0

    def balance_change(self, winnings):
        self.balance = self.balance + winnings
        
    def clear_hand(self):
        """ Clear the player's hand for a new round. """
        self.hand = []
        self.bet_amount = 0