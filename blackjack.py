'''
A simple BlackJack game written in Python 3 using object oriented programming principles
- written by Arham Jamal.
'''

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        comp = ''
        for card in self.deck:
            comp += '\n' + card.__str__()
        return comp

    def shuffle(self):
        # In place
        random.shuffle(self.deck)

    def deal(self):
        # self.shuffle()
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        if card.rank == "Ace":
            self.adjust_for_ace()
            self.value += self.aces
        else:
            self.value += values[card.rank]

    def adjust_for_ace(self):
        if self.value + 11 > 21:
            self.aces = 1
        else:
            self.aces = 11


class Chips:

    def __init__(self):
        self.total = 0
        while self.total == 0:
            try:
                self.total = int(input('Please enter a value > 0 of the starting amount of chips the player wants: '))
            # This can be set to a default value or supplied by a user input
            except:
                print("Please enter a correct value in numbers.")
                continue
            else:
                break
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Please enter the betting amount:"))
        except:
            print("Please enter a correct amount in digits.")
            continue
        else:
            if chips.bet <= chips.total:
                break
            else:
                print("The betting amount is greater than chips available.")
                continue


def hit(deck,hand):
    #dealtcard = deck.deal()
    # print(dealtcard)
    hand.add_card(deck.deal())


def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    while True:
        x = input('Hit or Stand?')
        if x[0].lower() == 'h':
            hit(deck,hand)
            break
        elif x[0].lower() == 's':
            print("Player stands. Dealer's turn.")
            playing = False
            break
        else:
            print("Something's wrong. Enter again.")
            continue


def show_some(player, dealer):
    print("Dealer's hand: ")
    print(dealer.cards[0])
    print('\n')
    print("Player's hand: ")
    print(*player.cards)
    print('\n')


def show_all(player, dealer):
    print("Dealer's hand: ")
    # asterisk * symbol is used to print every item in a collection
    print(*dealer.cards)
    print("Dealer's value ", dealer.value)
    print('\n')
    print("Player's hand: ")
    print(*player.cards)
    print("Player's hand: ", player.value)
    print('\n')


def player_busts(player, dealer, chips):
    chips.lose_bet()
    print("Player busted")


def player_wins(player, dealer, chips):
    chips.win_bet()
    print("Player won!")


def dealer_busts(player, dealer, chips):
    chips.win_bet()
    print("Dealer busted")


def dealer_wins(player, dealer, chips):
    chips.lose_bet()
    print("Dealer won!")


def push(player, dealer):
    print("Dealer and player tie. PUSH")


while True:
    # Print an opening statement
    print("Welcome to the game of BlackJack")

    # Create & shuffle the deck, deal two cards to each player
    playing_deck = Deck()
    playing_deck.shuffle()

    player1 = Hand()
    dealer = Hand()

    player1.add_card(playing_deck.deal())
    player1.add_card(playing_deck.deal())
    dealer.add_card(playing_deck.deal())
    dealer.add_card(playing_deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player1, dealer)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(playing_deck, player1)

        # Show cards (but keep one dealer card hidden)
        show_some(player1, dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player1.value > 21:
            player_busts(player1, dealer, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player1.value <= 21:

        while dealer.value < 17:
            hit(playing_deck, dealer)

        # Show all cards
        show_all(player1, dealer)

        # Run different winning scenarios
        if dealer.value > 21:
            dealer_busts(player1, dealer, player_chips)

        elif dealer.value > player1.value:
            dealer_wins(player1, dealer, player_chips)

        elif player1.value > dealer.value:
            player_wins(player1, dealer, player_chips)

        else:
            push(player1, dealer)

    # Inform Player of their chips total
    print("Player 1 the total number of chips that you have are: ", player_chips.total)

    # Ask to play again
    play_again = input("Would you like to play again? Enter Y for Yes and N for No: ").lower()

    if play_again == 'y' or play_again == 'yes':
        playing = True
        continue
    elif play_again == 'n' or play_again == 'no':
        break
    else:
        print("Please enter a correct value!")
        continue
