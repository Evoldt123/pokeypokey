import os
import sys
import random
import pygame
from pygame.locals import QUIT
from itertools import combinations 
import threading
import time

print()

pygame.init()

# ------------------- {Pygame}

game_state = 0

pygame.init()
# Set screen size
screen_size = [1000, 640]
screen_w = screen_size[0]
screen_h = screen_size[1]
screen = pygame.display.set_mode(screen_size)
# Set the window title
pygame.display.set_caption('')

game_loop = True

clock = pygame.time.Clock()
FPS = 1000
currentFPS = 0

card_font = pygame.font.SysFont('segoeuiblack', 40)
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

debug_symbols = {
    "S": "♠",
    "H": "♥",
    "D": "♦",
    "C": "♣", 
}

class Card():
    def __init__(self, value, suit):
        super().__init__()
        self.value = value
        self.suit = suit
        self.raw = str(self.value + debug_symbols[self.suit])

        

        # Visuals
        self.image = pygame.Surface([60, 90])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 300
         
    def draw(self):
        white_bg = pygame.Rect(self.rect.x, self.rect.y, 60, 90)
        pygame.draw.rect(screen, WHITE, white_bg, 0, 10)
        
        card_text = card_font.render(str(self.value), True, RED)
        card_text_rect = card_text.get_rect(center=(white_bg.center))

        screen.blit(card_text, (card_text_rect))
        

    def debug_self(self):
        print(self.value + debug_symbols[self.suit], end = ' ')

value_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suit_list = ["C", "H", "S", "D"]
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
    suit_count = set()
    arr_rep = [0 for card in value_list]
    for card in hand:

        if card.value in card_count:
            card_count[card.value] += 1
        else:
            card_count[card.value] = 1

        suit_count.add(card.suit)
    # Flush Check
    flush = True if len(suit_count) == 1 else False

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
        return [10] 
    # High Card on Straight
    if straight and flush:
        return [9, straight_high]
    # Quad, then kicker
    if quads:
        return [8]
    # Trip, then Doub
    if trips == 1 and pairs == 1:
        return [7]
    # Hand Sorted
    if flush:
        temp_lst = sorted([value_list.index(card.value) for card in hand], reverse=True)
        fin = [6] + temp_lst
        return fin
    # High Card
    if straight:
        return [5, straight_high]
    # Trips, Rest
    if trips == 1:
        return [4]
        tmp_list = [7, arr_rep.find(3)]
    # Doub, Doub, Rest
    if pairs == 2:
        return [3]
    # Doub, Rest
    if pairs == 1:
        return [2]
    else:
        return [1]
    
def play_hand():
    global currentFPS
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if round(clock.get_fps()) != currentFPS:
        # Update window title with current FPS
        pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
        currentFPS = round(clock.get_fps())

    screen.fill(LIGHT_BLUE)

    # background("images\\bricked.jpg")
    draw_poker_table()


    def debug_round(river, hand):
        # Print River Hand Terminal :3
        for card in river:
            card.debug_self()
        print()
        for card in hand:
            card.debug_self()
        print()


    round_deck = full_deck.copy()

    river = random.sample(round_deck, 5)
    for card in river:
        round_deck.remove(card)

    hand = random.sample(round_deck, 2)
    for card in hand:
        round_deck.remove(card)

    best = 0
    full_hand = hand + river

    combinations_of_5 = combinations(full_hand, 5)
    for combo in combinations_of_5:
        best = max(calculate_hand(combo)[0], best)

    # best = calculate_hand(river)
    
    debug_round(river, hand)
    print(f"BEST: {hand_values[best]}.")

    card.draw()
    pygame.display.update()
    






running = True

# --------------------------- Funky Functions
def background(image):
  BG = pygame.transform.scale((pygame.image.load(image)),(screen_w, screen_h)).convert_alpha()
  screen.blit(BG, (0, 0))

def draw_poker_table():
    # 1000 by 640, 500 and 320 - half dim
    table_outline = pygame.Rect(100, 70, 800, 500)
    table_shadow = pygame.Rect(130, 110, 800, 500)

    pygame.draw.rect(screen, BROWN, table_shadow, 0, 200)
    pygame.draw.rect(screen, DARK_GREEN, table_outline, 0, 200)
    

    table_inner = pygame.Rect(0, 0, 750, 450)
    table_inner.center = table_outline.center
    pygame.draw.rect(screen, GREEN, table_inner, 0, 200)

    yellow_outline = pygame.Rect(0, 0, 650, 350)
    yellow_outline.center = table_outline.center
    pygame.draw.rect(screen, YELLOW, yellow_outline, 5, 200)

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if round(clock.get_fps()) != currentFPS:
        # Update window title with current FPS
        pygame.display.set_caption(f'FPS: {round(clock.get_fps())}')
        currentFPS = round(clock.get_fps())

    screen.fill(LIGHT_BLUE)


    # background("images\\bricked.jpg")
    draw_poker_table()

    """
    while game_loop == True:
        game_thread = threading.Thread(target=play_hand)
        game_thread.start()
        game_loop = False
    """

    while game_state == 0:
        play_hand()
    pygame.display.update()