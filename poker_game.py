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
    def __init__(self):

        def make_deck():
            # global value_list, suit_list
            deck = []
            for value in value_list:
                for suit in suit_list:
                    deck.append(Card(value, suit))
            return deck

        # Create a full deck
        self.round_deck = make_deck()

        self.river = random.sample(self.round_deck, 5)
        for card in self.river:
            self.round_deck.remove(card)
        


