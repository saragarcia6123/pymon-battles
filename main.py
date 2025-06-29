import pygame


pygame.init()

from game import Game
from states.start_menu import StartMenu

game = Game()
game.STATE = StartMenu()
game.start()

while game.running:
    game.tick()
    game.render()

pygame.quit()
