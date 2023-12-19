import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self, suit, rank):
        self.suit=suit
        self.rank=rank
        self.val=values[rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        return f"{[str(card) for card in self.deck]}"

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        curr=self.deck.pop(0)
        return curr
    
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.val = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.val+=card.val
    
    def adjust_for_ace(self):
        if self.val>21 and self.aces !=0 :
            self.val-=10

class Chips:
    
    def __init__(self,money):
        self.total = money
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
        self.bet = 0
    
    def lose_bet(self):
        self.total-=self.bet
        self.bet = 0

def take_bet(chips):
    bet=0
    while  type(bet)!=int or bet>chips.total or bet<=0:
        try:
            bet=int(input("Please place your bets:"))
            if bet>chips.total:
                print("You don't have that much money, please Choose a lower bet")
            else:
                chips.bet=bet
                print(f"Player's bet is {bet}")
            
        except:
            print("Please enter integer number like :10, 15, 20, etc.")

def hit(deck,hand):
    cardnow=deck.deal()
    hand.add_card(cardnow)
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    choice=''
    while choice!='H' and choice !='S':
        choice=input("Please choose 'H' for hits and 'S' for stands:")
    if choice=="H":
        hit(deck,hand)
    else:
        playing=False

def show_some(player,dealer):
    print(f"Dealer: {[str(dealer.cards[i]) for i in range(1,len(dealer.cards))]}, Value:{dealer.val-dealer.cards[0].val}")
    print(f"Player: {[str(player.cards[i]) for i in range(len(player.cards))]}, Value:{player.val}")
    
def show_all(player,dealer):
    print(f"Dealer: {[str(dealer.cards[i]) for i in range(len(dealer.cards))]}, Value:{dealer.val}")
    print(f"Player: {[str(player.cards[i]) for i in range(len(player.cards))]}, Value:{player.val}")

def player_busts(player,dealer,chips):
    print("Your busts")
    show_all(player,dealer)
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("You Win!")
    show_all(player,dealer)
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    show_all(player,dealer)
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("You Lose")
    show_all(player,dealer)
    chips.lose_bet()
    
def push(player,dealer,chips):
    print("Push")
    show_all(player,dealer)

# Set up the Player's chips
money=''
while type(money)!= int:
    try:
        money=int(input("Cash in (Please enter an integer):"))
        chips=Chips(money)
    except:
        print("Please enter integer number like :10, 15, 20, etc.")
    

        
while True:
    # Print an opening statement
    print("Welcome to 'BlackJack'!")
    
    if chips.total <=0:
        print(f"Cash out {chips.total}\nEnjoy your day!")
        break
    
    # Create & shuffle the deck, deal two cards to each player
    deck=Deck()
    deck.shuffle()
    dealer=Hand()
    player=Hand()
    for i in range(2):
        dealer.add_card(deck.deal())
        player.add_card(deck.deal())
        

    
    # Prompt the Player for their bet
    take_bet(chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)
    
    playing=True
    while playing: 
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player,dealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.val>21:
            player_busts(player,dealer,chips)

            break
    
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    dealer_b=False
    if player.val<=21:
        while dealer.val<17:
            hit(deck,dealer)
            if dealer.val>21:
                dealer_busts(player,dealer,chips)
                dealer_b=True
                break
                

            # Show all cards
        #show_all(player,dealer)
        if dealer_b==False:
            # Run different winning scenarios
            if dealer.val>player.val:
                dealer_wins(player,dealer,chips)
            elif dealer.val<player.val:
                player_wins(player,dealer,chips)
            else:
                push(player,dealer,chips)
    
    # Inform Player of their chips total 
    print(f"Your current total balance is {chips.total}")
    print("\n")
    
    # Ask to play again
    res=input("Wanna play again? Enter 'q' to quit, others to continue:")
    if res=='q':
        print(f"Cash out {chips.total}\nEnjoy your day!")
        break