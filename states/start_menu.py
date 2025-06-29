import pygame

from game import Game
from resources import DEFAULT_FONT, TITLE_FONT
from state import State
from settings import key_bindings


class StartMenu(State):

    options = ["play", "settings", "exit"]

    def __init__(self) -> None:
        self.selected = 0
        self.init_title()
        self.init_menu()

    def init_title(self):
        self.title = TITLE_FONT.render("PyMon Battles!", True, (255, 255, 0))
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = int(Game().WIDTH / 2)
        self.title_rect.centery = int(Game().HEIGHT * 0.25)

    def init_menu(
        self,
        offset: int = Game().HEIGHT - 250,
        gap: int = 50,
    ):
        self.option_texts: list[pygame.Surface] = []
        self.option_text_rects: list[pygame.Rect] = []
        for i, option in enumerate(self.options):
            option_text = DEFAULT_FONT.render(option, True, (255, 255, 255))
            option_text_rect = option_text.get_rect()

            option_text_rect.centerx = int(Game().WIDTH / 2)
            option_text_rect.centery = offset + i * gap

            self.option_texts.append(option_text)
            self.option_text_rects.append(option_text_rect)

    def key_down(self, key: int):
        if key == key_bindings["up"]:
            self.selected = (self.selected - 1) % len(self.options)
        if key == key_bindings["down"]:
            self.selected = (self.selected + 1) % len(self.options)
        if key == key_bindings["a"]:
            self.on_select()

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.fill((0, 0, 80))
        for i in range(len(self.option_texts)):
            if i == self.selected:
                self.option_texts[i].set_alpha(255)
            else:
                self.option_texts[i].set_alpha(150)
            Game().screen.blit(self.option_texts[i], self.option_text_rects[i])
        screen.blit(self.title, self.title_rect)

    def on_select(self):
        match self.selected:
            case 0:
                Game().change_state("intro")
            case 1:
                Game().change_state("settings")
            case 2:
                Game().stop()
