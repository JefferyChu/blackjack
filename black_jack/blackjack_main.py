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
### Logical Flow
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
from class_def import Card, Player, CardOperations
    
# Initialize player, house and CardOperations
player1 = Player('Player 1', 5000)
house = Player('House', 1000000)
card_ops = CardOperations()

# Initialize hands and initial distribution counter
deck_list = card_ops.deck_generator()  # Generate new deck at start of game
player1_hand = []
dealer_hand = []

print(f'Your balance: {player1.balance}')

# Input and check for bet amount
while True:
    try:
        bet_amount = int(input('How much do you want to bet? '))
        if (bet_amount > player1.balance or bet_amount < 0):
            print('You cannot bet more than your balance or a negative number!')
        else:
            break
    except:
        print('Please enter proper integer value for the bet!')

# Take first turn
(player1_hand, dealer_hand, desk_list) = card_ops.take_one_turn(player1_hand, dealer_hand, deck_list)

# Display Hand and Current Values
card_ops.display_hand(player1, player1_hand, card_ops.cal_hand_value, deck_list)

# Player's Turn

# Ask for input to HIT or STAY
while True:
    player_decision = input('HIT or STAY? Type h for HIT or s for STAY: ').lower()
    if player_decision not in ['h', 's']:
        print('Please select valid decision!')
    else:
        break

if player_decision == 'h':
    
    player1_hand, deck_list = card_ops.take_1_card(player1_hand, deck_list)
    
    card_ops.display_hand(player1, player1_hand, card_ops.cal_hand_value, deck_list)
    
    # Checks for bust
    if min(card_ops.cal_hand_value(player1_hand)) > 21:
        print(f'Unfortunate! You went Bust with a hand value of {min(card_ops.cal_hand_value(player1_hand))}.')
        print('Dealer: "Hahaha, your money is safer with us!"')
        player1.balance_change(-bet_amount)
        print(f'Your balance is now: {player1.balance}')
        break
    else:
        pass
    
    player_decision = input('HIT or STAY? Type h for HIT or s for STAY: ').lower()
    
# Dealer's Turn

if min(card_ops.cal_hand_value(player1_hand)) > 21:
    pass
else:
    card_ops.display_hand(house,dealer_hand,card_ops.cal_hand_value,deck_list)

    # Dealer will HIT on less than 17, otherwise STAND
    while max(card_ops.cal_hand_value(dealer_hand)) < 17:
        print('\nHouse draws a card...')
        dealer_hand, deck_list = card_ops.take_1_card(dealer_hand,deck_list)
        card_ops.display_hand(house,dealer_hand,card_ops.cal_hand_value,deck_list)
    if max(card_ops.cal_hand_value(dealer_hand)) > 21:
        while min(card_ops.cal_hand_value(dealer_hand)) < 17:
            print('\nHouse draws a card...')
            dealer_hand, deck_list = card_ops.take_1_card(dealer_hand,deck_list)
            card_ops.display_hand(house,dealer_hand,card_ops.cal_hand_value,deck_list)
    # Compare dealer and player hands and determine outcome
    
    # First ensures anything above 21 hand value is bust
    if min(card_ops.cal_hand_value(dealer_hand)) > 21:
        print('\nDealer busted! You win!')
        print('Your previous balance was: ', player1.balance)
        player1.balance_change(2 * bet_amount)
        print('Your balance is now:', player1.balance)
        print('\nDealer: "Nooooooo!"')
    
    else:
        player1_final_value = 0
        house_final_value = 0
        
        # Checks Player's Max Hand Value
        if max(card_ops.cal_hand_value(player1_hand)) > 21:
            player1_final_value = min(card_ops.cal_hand_value(player1_hand))
        
        else: 
            player1_final_value = max(card_ops.cal_hand_value(player1_hand))
        
        # Checks House's Max Hand Value
        if max(card_ops.cal_hand_value(dealer_hand)) > 21:
            house_final_value = min(card_ops.cal_hand_value(dealer_hand))
        
        else: 
            house_final_value = max(card_ops.cal_hand_value(dealer_hand))
            
        # Compares player and dealer hand values
        if house_final_value > player1_final_value:
            print('\nHouse has the better hand. House wins!')
            print('Your previous balance was: ',player1.balance)
            player1.balance_change(-bet_amount)
            print('Your balance is now: ',player1.balance)
            print('\nDealer: "You will always lose against me!"')
        
        elif house_final_value == player1_final_value:
            print('Draw!')
            print('Your previous balance was: ', player1.balance)
            print('Your balance remains unchanged at: ', player1.balance)
            print('Dealer: "Let us play again!"')
        
        else:
            print('You have the better hand. You win!')
            print('Your previous balance was: ', player1.balance)
            player1.balance_change(2 * bet_amount)
            print('Your balance is now: ', player1.balance)
            print('Dealer: "I\'ll get you for this"')

# To fix
# (Rectified, check) Player hand was 18,18 and dealer went first (4,14) then (14,24) then stopped drawing even though min still drawable
# Player1 => 7,2,2,1,7 => gave 19,19 so max value not working? Issue with 2 aces as then 3 distinct combos (2,12,22)


