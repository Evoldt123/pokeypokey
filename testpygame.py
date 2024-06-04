import pygame
import sys
import time
from pygame.locals import QUIT

print()

pygame.init()
screen = pygame.display.set_mode((640, 480))

fonts = pygame.font.get_fonts()
thing = 0
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    font = pygame.font.SysFont(f"segoeuiblack", 30)
    # print(fonts[thing])

    text_surface = font.render("♦. 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A", True, (255, 0, 0))
    screen.blit(text_surface, (100, 100))
    pygame.display.flip()
    # time.sleep(3)
    # thing += 1
    # broadway bahnschrift segoeuiblack