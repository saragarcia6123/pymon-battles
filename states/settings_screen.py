import pygame
from components.menu import Menu
from game import Game
from state import State


class SettingsMenu(Menu):

    options = ["Difficulty", "HOME"]

    def __init__(self) -> None:
        super().__init__(self.options, 200, 50, False)

    def on_select(self):
        super().on_select()
        match self.selected:
            case 0:
                pass
            case 1:
                Game().change_state("start")


class SettingsScreen(State):

    def __init__(self) -> None:
        super().__init__()
        self.menu = SettingsMenu()

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        self.menu.render()

    def key_down(self, key: int):
        super().key_down(key)
        self.menu.key_down(key)
