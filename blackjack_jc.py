# Blackjack Rules

"""
Conditions
- One deck of 52 cards
- Ace counts as 1 or 11
- Face cards are 10

Some exceptional cases:
- 2 aces
- 1 ace and other cards
"""

"""
- Player places bet
- Give player hand
- Give dealer hand
- Player's turn to choose from the following options:
-- HIT = get another card, can keep hitting until bust above 21
-- STAND = do nothing
- Dealer's turn to choose from the following options:
-- If >= 17, STAND
-- If <17, HIT until above >=17 or bust
- Highest hand wins
- Winner gets 2 x bet
- Regenerate deck and clear hands
"""
# Imports

import random
from IPython.display import clear_output

# Creation of Deck Cards class

class Card:
    
    def __init__(self,value1,value2,suit,indexvalue):
        self.value1 = value1
        self.value2 = value2
        self.suit = suit
        self.indexvalue = indexvalue
        
    def __str__(self):
        return f"This card has values {self.value1} and {self.value2} and is of suit {self.suit}"
        
# Creation of Player class

class Player:
    
    def __init__(self,name,balance):
        self.name = name
        self.balance = balance
    def balance_change(self,winnings):
        self.balance = self.balance + winnings
        
# Deck Generator function

def deck_generator():
    deck_dict = {}

    suits = ['clubs','diamonds','hearts','spades']
    for suit in suits:
        for x in range(1,14):
            if x == 1:
                deck_dict['{}{}'.format(suit,x)] = Card(x,11,suit,x)
            elif x > 10:
                deck_dict['{}{}'.format(suit,x)] = Card(10,10,suit,x)
            else:
                deck_dict['{}{}'.format(suit,x)] = Card(x,x,suit,x)
    return deck_dict

# General Take 1 Card function

def take_1_card(hand_to_change, deck_list):
    
    num_picked = random.randint(0,len(deck_list)-1)
    #print('index num: ', num_picked)
    card_picked = deck_list[num_picked]
    del deck_list[num_picked]
    hand_to_change.append(card_picked)
    return hand_to_change, deck_list
    
# Hand Value Calculator function

def cal_hand_value(hand):
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
    
# Display Hand function

def display_hand(player, hand,cal_hand_value,deck_list):
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
    print('\nCurrent hand values are ',cal_hand_value(hand))
    print('\nCurrent deck len:', len(deck_list))
    
# Initialize players and balances

player1 = Player('Player 1', 5000)

# Initialize house and balances

house = Player('House', 1000000)

# Generate deck
deck_list = list(deck_generator().items()) # Generate new deck at start of game

# Initialize hands and initial distribution counter
dist_counter = 0
player1_hand = []
dealer_hand = []

print('Your balance: ',player1.balance)

# Input and check for bet amount
while True:
    try:
        bet_amount = int(input('\nWhat is the bet amount? '))
        if (bet_amount > player1.balance or bet_amount < 0):
            print('\nYou cannot bet more than your balance or a negative number!')
        else:
            break
    except:
        print('Please enter proper integer value for the bet!')
    
# Distribute first 2 cards to player and dealer
while dist_counter < 2:
    
    # Take 1 card for player
    player1_hand, deck_list = take_1_card(player1_hand, deck_list)
    #print('Player 1 hand: ',player1_hand, '\nCurrent deck len: ', len(deck_list))
    
    # Take 1 card for dealer
    dealer_hand, deck_list = take_1_card(dealer_hand, deck_list)
    #print('Dealer hand: ',dealer_hand, '\nCurrent deck len: ', len(deck_list))
    
    dist_counter += 1

print('\nEnd of initial distribution.')

# Display Hand and Current Values
display_hand(player1, player1_hand, cal_hand_value, deck_list)

# Player's Turn

# Ask for input to HIT or STAY
pdecision = input('\nHIT or STAY? Type h for HIT or s for STAY: ').lower()

while pdecision == 'h':
    
    player1_hand, deck_list = take_1_card(player1_hand, deck_list)
    
    display_hand(player1, player1_hand, cal_hand_value, deck_list)
    
    # Checks for bust
    if min(cal_hand_value(player1_hand)) > 21:
        print('\nUnfortunate! You went Bust with a hand value of {}.'.format(min(cal_hand_value(player1_hand))))
        print('\nDealer: "Hahaha, your money is safer with us!"')
        player1.balance_change(-bet_amount)
        print('Your balance is now:',player1.balance)
        break
    else:
        pass
    
    pdecision = input('\nHIT or STAY? Type h for HIT or s for STAY: ').lower()
    
# Dealer's Turn

if min(cal_hand_value(player1_hand)) > 21:
    pass
else:
    display_hand(house,dealer_hand,cal_hand_value,deck_list)

    # Dealer will HIT on less than 17, otherwise STAND
    while max(cal_hand_value(dealer_hand)) < 17:
        print('\nHouse draws a card...')
        dealer_hand, deck_list = take_1_card(dealer_hand,deck_list)
        display_hand(house,dealer_hand,cal_hand_value,deck_list)
    if max(cal_hand_value(dealer_hand)) > 21:
        while min(cal_hand_value(dealer_hand)) < 17:
            print('\nHouse draws a card...')
            dealer_hand, deck_list = take_1_card(dealer_hand,deck_list)
            display_hand(house,dealer_hand,cal_hand_value,deck_list)
    # Compare dealer and player hands and determine outcome
    
    # First ensures anything above 21 hand value is bust
    if min(cal_hand_value(dealer_hand)) > 21:
        print('\nDealer busted! You win!')
        print('Your previous balance was: ',player1.balance)
        player1.balance_change(2*bet_amount)
        print('Your balance is now:',player1.balance)
        print('\nDealer: "Nooooooo!"')
    
    else:
        player1_final_value = 0
        house_final_value = 0
        
        # Checks Player's Max Hand Value
        if max(cal_hand_value(player1_hand)) > 21:
            player1_final_value = min(cal_hand_value(player1_hand))
        
        else: 
            player1_final_value = max(cal_hand_value(player1_hand))
        
        # Checks House's Max Hand Value
        if max(cal_hand_value(dealer_hand)) > 21:
            house_final_value = min(cal_hand_value(dealer_hand))
        
        else: 
            house_final_value = max(cal_hand_value(dealer_hand))
            
        # Compares player and dealer hand values
        if house_final_value > player1_final_value:
            print('\nHouse has the better hand. House wins!')
            print('Your previous balance was: ',player1.balance)
            player1.balance_change(-bet_amount)
            print('Your balance is now: ',player1.balance)
            print('\nDealer: "You will always lose against me!"')
        
        elif house_final_value == player1_final_value:
            print('\nDraw!')
            print('Your previous balance was: ',player1.balance)
            print('Your balance remains unchanged at: ',player1.balance)
            print('\nDealer: "Let us play again!"')
        
        else:
            print('\nYou have the better hand. You win!')
            print('Your previous balance was: ',player1.balance)
            player1.balance_change(2*bet_amount)
            print('Your balance is now: ',player1.balance)
            print('\nDealer: "I\'ll get you for this"')

# To fix
# (Rectified, check) Player hand was 18,18 and dealer went first (4,14) then (14,24) then stopped drawing even though min still drawable
# Player1 => 7,2,2,1,7 => gave 19,19 so max value not working? Issue with 2 aces as then 3 distinct combos (2,12,22)


