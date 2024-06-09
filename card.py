import os
import sys
import random
import pygame
from pygame.locals import QUIT
from itertools import combinations 
import threading
import time

# Initialize pygame
pygame.init()
# Set up fonts
card_font = pygame.font.SysFont('segoeuiblack', 40)
card_font_small = pygame.font.SysFont('segoeuiblack', 20)

# Define colors
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)

LIGHT_BLUE = (127, 183, 240)
DARK_GREEN = (0, 50, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
NAVY = (133, 33, 255)
BROWN = (97, 34, 2)
TEAL = (74, 217, 193)
PINK = (255, 33, 222)
PURPLE = (160, 32, 240)
MAROON = (128, 0, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (20, 20, 20)

# Debug symbols for card suits
debug_symbols = {
    "S": "♠",
    "H": "♥",
    "D": "♦",
    "C": "♣", 
}

# List to store cards to be drawn
draw_these = []

# Class representing a playing card
class Card():
    def __init__(self, value, suit):
        
        # self.screen = screen
        self.value = value
        self.suit = suit
        self.raw = str(self.value + debug_symbols[self.suit])

        # Suit Colors
        self.color = BLACK   
        if self.suit in ['♦', '♥', 'D', 'H']:
            self.color = RED
        elif self.suit in ['♠', '♣', 'S', 'C']:
            self.color = BLACK        

        # Visuals
        self.image = pygame.Surface([60, 90])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 300

        self.visible = True
         
    def draw(self, screen):
        # Draw visible card
        if self.visible:
            white_bg = pygame.Rect(self.rect.x, self.rect.y, 60, 90)
            pygame.draw.rect(screen, WHITE, white_bg, 0, 10)
            
            card_text = card_font.render(str(self.value), True, self.color)
            card_text_rect = card_text.get_rect(center=(white_bg.center))

            suit_text = card_font_small.render(debug_symbols[self.suit], True, self.color)

            screen.blit(card_text, (card_text_rect))
            screen.blit(suit_text, (self.rect.x+5, self.rect.y+5))
        
        # Card backing
        else:
            red_bg = pygame.Rect(self.rect.x, self.rect.y, 60, 90)
            pygame.draw.rect(screen, RED, red_bg, 0, 10)
        

    def debug_self(self):
        print(self.value + debug_symbols[self.suit], end=' ')