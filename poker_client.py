import os
import sys
import random
import pygame
from pygame.locals import QUIT
from itertools import combinations 
import threading
import time
from network import Network
from poker_game import Game

# Initialize pygame
pygame.init()

# ------------------- {Pygame}

# Set up game state
game_state = 0

# Set screen size
screen_size = [1000, 640]
screen_w = screen_size[0]
screen_h = screen_size[1]
screen = pygame.display.set_mode(screen_size)

# Set the window title
pygame.display.set_caption('')

game_loop = True

# Set up clock for managing FPS
clock = pygame.time.Clock()
FPS = 1000
currentFPS = 0

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

# Possible card values and suits
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

# Function to calculate the value of a poker hand
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

# Function to play a hand of poker
def play_hand():
    global currentFPS
    global draw_these
    clock.tick(FPS)
    player = n.getP()

    
    """
    best = 0
    full_hand = hand + game.river

    combinations_of_5 = combinations(full_hand, 5)
    for combo in combinations_of_5:
        best = max(calculate_hand(combo)[0], best)

    # Print out the best hand
    for card in game.river:
        card.debug_self()
    print()
    for card in hand:
        card.debug_self()
    print(f"BEST: {hand_values[best]}.")

    for i, card in enumerate(game.river):
        draw_these.append(card)
        card.rect.center = (340 + 80*i, 270)
    for i, card in enumerate(hand):
        draw_these.append(card)
        card.rect.center = (465 + 70*i, 550)
    """

# Main game loop
running = True

# --------------------------- Funky Functions

# Function to set background image
def make_bg(image):
    return pygame.transform.scale((pygame.image.load(image).convert_alpha()), (screen_w, screen_h)).convert_alpha()

BRICK_BG = make_bg("images\\bricked.jpg")

def background(BG):
    # BG = pygame.transform.scale((pygame.image.load(image).convert_alpha()), (screen_w, screen_h)).convert_alpha()
    screen.blit(BG, (0, 0))

# Function to draw the poker table
def draw_poker_table():
    # Draw table outline
    table_outline = pygame.Rect(100, 70, 800, 500)
    table_shadow = pygame.Rect(130, 110, 800, 500)

    pygame.draw.rect(screen, BROWN, table_shadow, 0, 200)
    pygame.draw.rect(screen, DARK_GREEN, table_outline, 0, 200)
    
    # Draw table inner
    table_inner = pygame.Rect(0, 0, 750, 450)
    table_inner.center = table_outline.center

    pygame.draw.rect(screen, GREEN, table_inner, 0, 200)

    # Draw yellow outline
    yellow_outline = pygame.Rect(0, 0, 650, 350)
    yellow_outline.center = table_outline.center
    pygame.draw.rect(screen, YELLOW, yellow_outline, 5, 200)

    # Draw card outline
    card_outline = pygame.Rect(0, 0, 70, 100)
    for c in range(-2, 3):
        card_outline.center = table_inner.center
        card_outline.centerx += 80*c
        card_outline.centery -= 50
        pygame.draw.rect(screen, YELLOW, card_outline, 2, 15)

n = Network()

# Main game loop
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

    if event.type == pygame.MOUSEBUTTONDOWN:
        player = n.getP()
        print("You are player", player)

    try:
        game = n.send("boinga")
        pass
    except:
        print("NO GAME NO GAME")

    screen.fill(LIGHT_BLUE)

    # Draw background
    background(BRICK_BG)

    # Draw poker table
    draw_poker_table()

    # Start the game loop
    while game_loop == True:
        game_thread = threading.Thread(target=play_hand)
        game_thread.start()
        game_loop = False
    
    # Draw cards
    for thing in draw_these:
        thing.draw()

    # Update display
    pygame.display.update()