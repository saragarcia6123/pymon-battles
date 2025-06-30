import pygame

from resource_loader import ResourceLoader



pygame.init()

loader = ResourceLoader()
loader.load_sprite_sheet("pokemon")

from game import Game
from states.start_menu import StartMenu

game = Game()
game.STATE = StartMenu()
game.start()

while game.running:
    game.tick()
    game.render()

pygame.quit()
