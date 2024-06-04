import threading
import time

import pygame
print(pygame.font.get_fonts())


def function_one():
    while True:
        print("Function One is running.")
        time.sleep(1)

# Define the second function to run in a separate thread
def function_two():
    while True:
        print("Function Two is running.")
        time.sleep(1)



        
thread_one = threading.Thread(target=function_one)
thread_two = threading.Thread(target=function_two)

thread_one.start()
thread_two.start()