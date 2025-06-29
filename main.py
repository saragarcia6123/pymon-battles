import pygame


pygame.init()

from game import Game
from states.start_screen import StartScreen

game = Game()
game.STATE = StartScreen()
game.start()

while game.running:
    game.tick()
    game.render()

pygame.quit()
