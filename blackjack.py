import random
 
SUITS = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 
         'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5,'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 
         'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace': 11} 
 
playing = True
 
 
class Card:
    
    def __init__(self, suit, rank):
        
        self.suit = suit
        self.rank = rank
        self.value = VALUES[rank]
        
    def __str__(self):
        return f'{self.rank} of {self.suit}'
 
 
 
class Deck:
    
    def __init__(self):
        
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + str(card)
        return f'{len(self.deck)} cards in deck: ' + deck_comp
    
    def shuffle(self):
        
        return random.shuffle(self.deck)
    
    def deal_one(self):
        
        return self.deck.pop()
 
 
 
class Hand:
    
    def __init__(self):
        
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        
        self.cards.append(card)
        self.value += VALUES[card.rank]
        
        if card.rank == 'Ace':
            self.aces += 1
        if card.rank[0] == 'Ace' and card.rank[1] == 'Ace':
            self.aces -= 1
            self.value -= 10
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
 
 
 
class Chips:
    
    def __init__(self):
        
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet      
 
 
 
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Please enter an integer..")
        else:
            if chips.total < chips.bet:
                print("Not enough chips, your total is ", chips.total)
            else:
                break
 
 
 
def hit(deck, hand):
    
    
    hand.add_card(deck.deal_one())
    hand.adjust_for_ace()
 
 
 
def hit_stay_doubledown(deck, hand, chips):
    
    global playing
    global double_down_count 
    global hits
 
    
    while True:
        # count of times player doubled down
        print(f'Double down count -> {double_down_count}')
        print(f'Hit count -> {hits}')
        
        
        # if player doubled down already, input only asks for hit or stay
        if double_down_count or hits:
            result = input("Would you like to Hit, Stand? Enter 'h' or 's' ").lower()
            
            if result.startswith("h"):
                hit(deck, hand)
 
            elif result.startswith("s"):
                print("Player stands. Dealer is playing. ")
                playing = False 
 
            else:
                print("Please enter hit or stand..")
                continue
                
        
        # if player has not doubled down already, input asks for hit, stay, or double down
        elif not double_down_count or not hits: 
            result = input("Would you like to Hit, Stand, or Double Down? Enter 'h' or 's' or 'd' ").lower()
            
            if result.startswith("d"):
                
                if (chips.bet)*2 > chips.total:
                    print("Not enough chips, your total is ", chips.total)
                else:
                    chips.bet += chips.bet
                    hit(deck, hand)
                    hits += 1
                    double_down_count += 1
                    # doubled down so the count adds one, player cannot double down again
            
            elif result.startswith("h"):
                hit(deck, hand)
                hits += 1
                    
            elif result.startswith("s"):
                print("Player stands. Dealer is playing. ")
                playing = False   
            
            else:
                print("Please enter hit or stand..")
                continue
 
        break
 
 
 
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand", *player.cards, sep='\n ')
    print(f"Player's Count is: {player.value}")
 
 
    
def show_all(player, dealer):
    print("\nDealer's Hand", *dealer.cards, sep='\n ')
    print(f"Dealer count is: {dealer.value}")
    print("\nPlayer's Hand", *player.cards, sep='\n ')
    print(f"Player's Count is: {player.value}")
 
 
 
def player_busts(player, dealer, chips):
    print("\nPlayer Busts!")
    chips.lose_bet()
 
def player_wins(player, dealer, chips):
    print("\nPlayer Wins!")
    chips.win_bet()
        
def dealer_busts(player, dealer, chips):
    print("\nDealer Busts!")
    chips.win_bet()
 
def dealer_wins(player, dealer, chips):
    print("\nDealer Wins!")
    chips.lose_bet()
 
def push(player, dealer):
    print("\nPUSH!")
 
 
 
def replay():
    
    answer = "unsure"
    choices = ['y', 'n']
    while answer not in choices:
        answer = input("Keep playing? y/n ").lower()
 
        if answer.startswith("y"):
            return True   
        elif answer.startswith("n"):
            print("\nBye")
            return False
 
 
 
player_chips = Chips()
 
print("Welcome to Blackjack!")
print('\n')
while True: 
    
    double_down_count = 0
    hits = 0
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())
    
    print('\n')
    print(f'Your total chips: {player_chips.total}')
    take_bet(player_chips)
    print('--------------------------------\n')
    
    show_some(player_hand, dealer_hand)
    print('--------------------------------\n')
    
    if player_hand.value == 21:
        print("BLACKJACK!!")
        playing = False
    
    while playing:
        print('\n'*2)
        hit_stay_doubledown(deck, player_hand, player_chips)
        show_some(player_hand, dealer_hand)
 
        if player_hand.value == 21:
            print("BLACKJACK!!")
            playing = False
        
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
            
            
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        
        print('--------------------------------\n')
        show_all(player_hand, dealer_hand)
        print('--------------------------------\n')
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
            
        elif player_hand.value == dealer_hand.value:
            push(player_hand, dealer_hand)
            
        elif player_hand.value == 21:
            print("Blackjack!\n")
            player_wins(player_hand, dealer_hand, player_chips)
            
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
            
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
 
        else: 
            print("Error")
            
    
    print('\n'*2)
    print(f'Your total chips: {player_chips.total}')
    if player_chips.total == 0:
        print("No more chips")
        break
    print('\n')
    
    if replay():
        playing = True
        continue
    else: 
        break