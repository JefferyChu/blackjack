
# Creation of Deck Cards class

class Card:
    
    def __init__(self, value1, value2, suit, indexvalue):
        self.value1 = value1
        self.value2 = value2
        self.suit = suit
        self.indexvalue = indexvalue
        
    def __str__(self):
        return f"This card has values {self.value1} and {self.value2} and is of suit {self.suit}"

# Creation of Player class

class Player:
    
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def balance_change(self, winnings):
        self.balance = self.balance + winnings
