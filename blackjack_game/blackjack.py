# Blackjack Rules

"""
Conditions
- One deck of 52 cards
- Ace counts as 1 or 11
- Face cards are 10

Features:
- Multiple Aces handled correctly
- Game continuation after rounds
- Proper dealer card hiding
- Improved hand value calculations

Logical Flow
- Player places bet
- Give player hand
- Give dealer hand (hide second card)
- Player's turn to choose from the following options:
-- HIT = get another card, can keep hitting until bust above 21
-- STAND = do nothing
- Dealer's turn to choose from the following options:
-- If >= 17, STAND
-- If <17, HIT until above >=17 or bust
- Highest hand wins
- Winner gets 2 x bet
- Option to play again or quit
"""

# Imports
import random
from class_def import Card, Player, CardOperations


def play_round(player, dealer, card_ops, deck_list):
    """Play a single round of blackjack."""
    
    # Clear hands for new round
    player.clear_hand()
    dealer.clear_hand()
    
    # Check if we need a new deck (less than 15 cards remaining)
    if len(deck_list) < 15:
        print("\nShuffling new deck...")
        deck_list = card_ops.deck_generator()
    
    print(f'\nYour current balance: ${player.balance}')
    
    # Input and check for bet amount
    while True:
        try:
            bet_amount = int(input('How much do you want to bet? $'))
            if bet_amount > player.balance:
                print('You cannot bet more than your balance!')
            elif bet_amount <= 0:
                print('You must bet a positive amount!')
            else:
                break
        except ValueError:
            print('Please enter a valid number for the bet!')

    # Set bet amount
    player.bet_amount = bet_amount
    
    # Take initial turn
    player, dealer, deck_list = card_ops.take_initial_turn(player, dealer, deck_list)

    # Display hands (hide dealer's second card)
    card_ops.display_hand(player, deck_list)
    card_ops.display_hand(dealer, deck_list, hide_dealer_card=True)

    #####################
    ### Player's Turn ###
    #####################

    # Check for blackjack
    if card_ops.cal_hand_value(player.hand) == 21:
        print("\nBlackjack! You have 21!")
        player_busted = False
    else:
        # Ask for input to HIT or STAY
        player_busted = False
        while True:
            player_decision = input('\nHIT or STAY? Type h for HIT or s for STAY: ').lower().strip()
            
            if player_decision not in ['h', 's']:
                print('Please select valid decision! (h for HIT, s for STAY)')
            elif player_decision == 'h':
                player, deck_list = card_ops.take_1_card(player, deck_list)
                card_ops.display_hand(player, deck_list)
                if card_ops.check_bust(player) == 'bust':
                    player_busted = True
                    break
            elif player_decision == 's':
                break

    #####################
    ### Dealer's Turn ###
    #####################

    if not player_busted:
        card_ops.dealer_turn(player, dealer, deck_list)
    
    return deck_list


def main():
    """Main game loop."""
    
    # Initialize player, dealer and CardOperations
    player = Player('Player 1', 5000)
    dealer = Player('Dealer', 1000000)
    card_ops = CardOperations()

    print("=" * 50)
    print("        WELCOME TO BLACKJACK!")
    print("=" * 50)
    print(f'Starting balance: ${player.balance}')
    
    # Initialize deck
    deck_list = card_ops.deck_generator()
    
    # Main game loop
    while True:
        # Check if player has money left
        if player.balance <= 0:
            print("\nYou're out of money! Game over.")
            break
            
        # Play a round
        deck_list = play_round(player, dealer, card_ops, deck_list)
        
        # Ask if player wants to continue
        while True:
            play_again = input('\nDo you want to play another round? (y/n): ').lower().strip()
            if play_again in ['y', 'yes']:
                break
            elif play_again in ['n', 'no']:
                print(f"\nThanks for playing! Final balance: ${player.balance}")
                return
            else:
                print('Please enter y for yes or n for no.')


if __name__ == "__main__":
    main()