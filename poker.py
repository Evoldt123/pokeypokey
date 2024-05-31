import os
import random
from collections import defaultdict 


debug_symbols = {
    "S": "♠",
    "H": "♥",
    "D": "♦",
    "C": "♣",
}

class Card():
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def debug_self(self):
        print(self.value + debug_symbols[self.suit], end = ' ')

value_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit_list = ["C", "H", "S", "D"]
hand_values = {
    1: "Royal Flush",
    2: "Straight Flush",
    3: "Four of a Kind",
    4: "Full House",
    5: "Flush",
    6: "Straight",
    7: "Three of a Kind",
    8: "Two Pair",
    9: "One Pair",
    10: "High Card"
}


def make_deck():
    deck = []
    for value in value_list:
        for suit in suit_list:
            deck.append( Card(value, suit) )
    return deck

full_deck = make_deck()

def calculate_hand(hand):
    global value_list, hand_values
    card_count = {}
    suit_count = {}
    arr_rep = [0 for card in value_list]
    for card in hand:

        if card.value in card_count:
            card_count[card.value] += 1
        else:
            card_count[card.value] = 1

        if card.suit in suit_count:
            suit_count[card.suit] += 1
        else:
            suit_count[card.suit] = 1
    # Flush Check
    flush = True if suit_count == 1 else False

    # Straight Check
    straight = False
    for key, val in card_count.items():
        arr_rep[value_list.index(key)] = val

    for x in range(len(arr_rep)-4):
        sub = arr_rep[x:x+5]
        if sub.count(0) == 0:
            straight = True
            straight_high = x+6

    sub = arr_rep[:4]
    sub.append(arr_rep[-1]) 
    if sub.count(0) == 0:
        straight = True
        straight_high = 5

    # Matches
    pairs = arr_rep.count(2)
    trips = arr_rep.count(3)
    quads = arr_rep.count(4)

    # (1) Royal Flush, (2) Straight Flush, (3) Quads, (4) Full House, (5) Flush
    # (6) Straight, (7) Trips, (8) Two Pair, (9) Pair, (10) High Card

    # First num is hand type :P
    # TRUMPS
    if straight and flush and arr_rep[-1] > 0:
        return [1] 
    # High Card on Straight
    if straight and flush:
        return [2, straight_high]
    # Quad, then kicker
    if quads:
        return [3, arr_rep.find(4), arr_rep.find(1)]
    # Trip, then Doub
    if trips == 1 and pairs == 1:
        return [4, arr_rep.find(3), arr_rep.find(2)]
    # 
    

        
    

def play_hand():
    round_deck = full_deck.copy()

    river = random.sample(round_deck, 5)
    for card in river:
        card.debug_self()
        round_deck.remove(card)
    print()

    hand = random.sample(round_deck, 2)
    for card in hand:
        card.debug_self()
        round_deck.remove(card)
    print()

    calculate_hand(river)

    print()


for x in range(1):
    play_hand()
    

            