import pygame

from game import Game
from game_object import GameObject
from resources import DEFAULT_FONT, TITLE_FONT
from state import State
from settings import key_bindings


class StartMenu(State):

    options = ["play", "settings", "exit"]

    def __init__(self) -> None:
        super().__init__((0, 0, 100))
        self.selected = 0
        self.init_title()
        self.init_menu()
        self.update_options()

    def init_title(self):
        title = TITLE_FONT.render("PyMon Battles!", True, (255, 255, 0))
        title_rect = title.get_rect()
        title_rect.centerx = int(Game().WIDTH / 2)
        title_rect.centery = int(Game().HEIGHT * 0.25)
        self.title_object = GameObject(title, title_rect)
        self.objects.append(self.title_object)

    def init_menu(
        self,
        offset: int = Game().HEIGHT - 250,
        gap: int = 50,
    ):
        self.option_text_objects: list[GameObject] = []
        for i, option in enumerate(self.options):
            option_text = DEFAULT_FONT.render(option, True, (255, 255, 255))
            option_text_rect = option_text.get_rect()

            option_text_rect.centerx = int(Game().WIDTH / 2)
            option_text_rect.centery = offset + i * gap

            option_object = GameObject(option_text, option_text_rect)
            self.option_text_objects.append(option_object)
            self.objects.append(option_object)

    def update_options(self):
        for i in range(len(self.option_text_objects)):
            if i == self.selected:
                self.option_text_objects[i].source.set_alpha(255)
            else:
                self.option_text_objects[i].source.set_alpha(150)

    def key_down(self, key: int):
        if key == key_bindings["a"]:
            self.on_select()
        if key == key_bindings["up"]:
            self.selected = (self.selected - 1) % len(self.options)
            self.update_options()
        if key == key_bindings["down"]:
            self.selected = (self.selected + 1) % len(self.options)
            self.update_options()

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def on_select(self):
        match self.selected:
            case 0:
                Game().change_state("intro")
            case 1:
                Game().change_state("settings")
            case 2:
                Game().stop()
