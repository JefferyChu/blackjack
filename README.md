# BlackJack-Project
Play a game of BlackJack with our friendly dealer

## Features
- **Proper Multiple Aces Handling**: Fixed logic to correctly calculate hand values with multiple Aces
- **Game Continuation**: Play multiple rounds without restarting the program
- **Improved Dealer Logic**: Fixed edge cases in dealer decision making
- **Better User Experience**: Clear prompts, proper card hiding, and balance tracking
- **Automatic Deck Reshuffling**: New deck when cards run low

## How to Play
1. Run `python blackjack_game/blackjack.py`
2. Place your bet (must be within your balance)
3. Try to get as close to 21 as possible without going over
4. Beat the dealer to win!

## Game Rules
- Aces count as 1 or 11 (automatically optimized)
- Face cards (J, Q, K) are worth 10
- Dealer hits on 16 or less, stands on 17 or more
- Blackjack (21 with first two cards) is automatic win
- Win doubles your bet, lose forfeits your bet

## Fixed Issues
- ✅ Multiple Aces calculation
- ✅ Game continuation after rounds
- ✅ Dealer logic edge cases
- ✅ Improved hand value display