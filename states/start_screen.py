import pygame
from components.menu import Menu
from components.start_screen import title
from game import Game
from state import State


class StartScreenMenu(Menu):

    options = ["play", "settings", "exit"]

    def __init__(self) -> None:
        super().__init__(self.options, Game().HEIGHT - 250, 50, False)

    def on_select(self):
        super().on_select()
        match self.selected:
            case 0:
                Game().change_state("intro")
            case 1:
                Game().change_state("settings")
            case 2:
                Game().stop()


class StartScreen(State):

    def __init__(self) -> None:
        super().__init__()
        self.title, self.title_rect = title()

        self.menu = StartScreenMenu()
        self.selected: int = 0

    def tick(self):
        super().tick()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("up")

    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.fill((0, 0, 80))

        # TITLE
        screen.blit(self.title, self.title_rect)

        # MENU OPTIONS
        self.menu.render()

    def key_down(self, key: int):
        super().key_down(key)
        self.menu.key_down(key)

    def on_play(self):
        pass
