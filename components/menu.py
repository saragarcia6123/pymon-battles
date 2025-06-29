import pygame

from game import Game
from resources import DEFAULT_FONT


class Menu:

    def __init__(
        self, options: list[str], offset: int, gap: int, horizontal: bool
    ) -> None:
        self.selected = 0
        self.options = options
        self.init_components(offset, gap, horizontal)

    def init_components(
        self,
        offset: int,
        gap: int,
        horizontal: bool,
    ):
        self.option_texts: list[pygame.Surface] = []
        self.option_text_rects: list[pygame.Rect] = []
        for i, option in enumerate(self.options):
            option_text = DEFAULT_FONT.render(option, True, (255, 255, 255))
            option_text_rect = option_text.get_rect()
            if horizontal:
                option_text_rect.centerx = offset + i * gap
                option_text_rect.centery = int(Game().HEIGHT / 2)
            else:
                option_text_rect.centerx = int(Game().WIDTH / 2)
                option_text_rect.centery = offset + i * gap

            self.option_texts.append(option_text)
            self.option_text_rects.append(option_text_rect)

    def key_down(self, key: int):
        match key:
            case pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            case pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            case pygame.K_RETURN:
                self.on_select()

    def render(self):
        for i in range(len(self.option_texts)):
            if i == self.selected:
                self.option_texts[i].set_alpha(255)
            else:
                self.option_texts[i].set_alpha(150)
            Game().screen.blit(self.option_texts[i], self.option_text_rects[i])

    def on_select(self):
        pass
