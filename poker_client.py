import os
import sys
import random
import pygame
from pygame.locals import QUIT
from itertools import combinations 
import threading
import time
from network import Network

import poker_game as poker
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

