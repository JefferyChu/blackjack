# Blackjack Rules

"""
Conditions
- One deck of 52 cards
- Ace counts as 1 or 11
- Face cards are 10

Some exceptional cases to consider:
- More than 1 ace

Logical Flow
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
from class_def import Card, Player, CardOperations
    
# Initialize player, house and CardOperations
player = Player('Player 1', 5000)
dealer = Player('Dealer', 1000000)
card_ops = CardOperations()

print(f'Your balance: {player.balance}')

# Initialize hands and initial distribution counter
deck_list = card_ops.deck_generator()  # Generate new deck at start of game

# Input and check for bet amount
while True:
    try:
        bet_amount = int(input('How much do you want to bet? '))
        if (bet_amount > player.balance or bet_amount < 0):
            print('You cannot bet more than your balance or a negative number!')
        else:
            break
    except:
        print('Please enter proper integer value for the bet!')

# Take first turn
player.bet_amount = bet_amount
player, dealer, desk_list = card_ops.take_initial_turn(player, dealer, deck_list)

# Display Hand and Current Values
card_ops.display_hand(player, deck_list)

#####################
### Player's Turn ###
#####################

# Ask for input to HIT or STAY
while True:
    player_decision = input('\nHIT or STAY? Type h for HIT or s for STAY: ').lower()
    
    if player_decision not in ['h', 's']:
        print('Please select valid decision!')
    elif player_decision == 'h':
        player, deck_list = card_ops.take_1_card(player, deck_list)
        card_ops.display_hand(player, deck_list)
        if card_ops.check_bust(player) == 'bust':
            break
    elif player_decision == 's':
        break

#####################
### Dealer's Turn ###
#####################

if min(card_ops.cal_hand_value(player.hand)) > 21:
    pass
else:
    card_ops.display_hand(dealer, deck_list)
    card_ops.dealer_turn(player, dealer, deck_list)

# To fix
# (Rectified, check) Player hand was 18,18 and dealer went first (4,14) then (14,24) then stopped drawing even though min still drawable
# player => 7,2,2,1,7 => gave 19,19 so max value not working? Issue with 2 aces as then 3 distinct combos (2,12,22)
