import os
import sys
import random
import pygame
from pygame.locals import QUIT
from itertools import combinations 
import threading
import time
from network import Network
from card import Card


value_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit_list = ["C", "H", "S", "D"]

# Hand values for evaluating poker hands
hand_values = {
    10: "Royal Flush",
    9: "Straight Flush",
    8: "Four of a Kind",
    7: "Full House",
    6: "Flush",
    5: "Straight",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "One Pair",
    1: "High Card"
}

class Game():
    def __init__(self, player_list):
        # pygame.time.delay(3000)

        self.player_list = player_list
        self.players = 0  
        self.button_player = 0
    
    """
    def make_hands(self):
        self.hands = []
        for x in range(self.players):
            self.hands.append(random.sample(self.round_deck, 2))
            for card in self.hands[-1]:
                self.round_deck.remove(card)
    """  

    def start_game(self, money):
        self.player_money = [int(money) for _ in range(self.players)]
        self.turn_to_go = [False for _ in range(self.players)]
        self.responses = ["" for _ in range(self.players)]

    def calculate_hand(hand):
        global value_list, hand_values
        card_count = {}
        suit_count = set()
        arr_rep = [0 for card in value_list]
        for card in hand:
            if card.value in card_count:
                card_count[card.value] += 1
            else:
                card_count[card.value] = 1

            suit_count.add(card.suit)

        # Flush check
        flush = True if len(suit_count) == 1 else False

        # Straight check
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

        # First num is hand type
        # Royal Flush
        if straight and flush and arr_rep[-1] > 0:
            return [10] 
        # High Card on Straight Flush
        if straight and flush:
            return [9, straight_high]
        # Four of a Kind
        if quads:
            return [8]
        # Full House
        if trips == 1 and pairs == 1:
            return [7]
        # Flush
        if flush:
            temp_lst = sorted([value_list.index(card.value) for card in hand], reverse=True)
            fin = [6] + temp_lst
            return fin
        # Straight
        if straight:
            return [5, straight_high]
        # Three of a Kind
        if trips == 1:
            return [4]
        # Two Pair
        if pairs == 2:
            return [3]
        # One Pair
        if pairs == 1:
            return [2]
        else:
            return [1]
        
    def start_turn(self):

        self.blinds = [1 + (pygame.time.get_ticks()//60000), (1 + (pygame.time.get_ticks()//60000))*2]
        self.pot = 0

        def make_deck():
            # global value_list, suit_list
            deck = []
            for value in value_list:
                for suit in suit_list:
                    deck.append((value, suit))
            return deck
        
        # Create a full deck
        self.round_deck = make_deck()

        self.river = random.sample(self.round_deck, 5)
        for card in self.river:
            self.round_deck.remove(card)        

        self.hands = []
        for x in range(self.players):
            self.hands.append(random.sample(self.round_deck, 2))
            for card in self.hands[-1]:
                self.round_deck.remove(card) 

        self.visible_cards = [False for x in range(5)]

        actions = ['F', 'C', 'R']

        self.current_bets = [0 for _ in range(self.players)]

        self.current_bets[self.button+1] += min(self.blinds[0], self.player_money[self.button+1])
        self.player_money[self.button+1] -= min(self.blinds[0], self.player_money[self.button+1])
        self.current_bets[self.button+2] += min(self.blinds[1], self.player_money[self.button+2])
        self.player_money[self.button+2] -= min(self.blinds[1], self.player_money[self.button+2])

        for bet in self.current_bets:
            self.pot += bet
        
        for x in range(self.players):
            curr = (x+self.button+3) % self.players

            if ()
            
            while(self.turn_to_go[curr] == True) or self.responses[curr] not in actions:
                self.turn_to_go[curr] = True

            response = self.responses[curr]



        


        

        

