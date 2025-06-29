import pygame

from game import Game
from pokemon_ids import POKE_ID_MAP
from resources import DEFAULT_FONT, TITLE_FONT
from sprite_loader import SpriteLoader
from state import State
from settings import key_bindings


class StartMenu(State):

    options = ["play", "settings", "exit"]

    def __init__(self) -> None:
        super().__init__((20, 20, 50))
        self.selected = 0
        self.init_title()
        self.init_menu()
        self.background = pygame.image.load("res/backgrounds/start_menu.png")
        self.background_rect = self.background.get_rect(
            center=(int(Game().WIDTH / 2), int(Game().HEIGHT / 2))
        )
        self.pikachu_front = SpriteLoader().get_sprite(
            POKE_ID_MAP["pikachu"], "battle_front"
        )
        self.update_options()

    def init_title(self):
        self.title_object = TITLE_FONT.render("PyMon Battles!", True, (255, 255, 0))
        self.title_rect = self.title_object.get_rect()  # Store the rect
        self.title_rect.centerx = int(Game().WIDTH / 2)
        self.title_rect.centery = int(Game().HEIGHT * 0.25)

    def init_menu(
        self,
        offset: int = Game().HEIGHT - 250,
        gap: int = 50,
    ):
        self.option_text_objects: list[pygame.Surface] = []
        self.option_text_rects: list[pygame.Rect] = []  # Store rects for options

        for i, option in enumerate(self.options):
            option_text = DEFAULT_FONT.render(option, True, (255, 255, 255))
            option_text_rect = option_text.get_rect()

            option_text_rect.centerx = int(Game().WIDTH / 2)
            option_text_rect.centery = offset + i * gap

            self.option_text_objects.append(option_text)
            self.option_text_rects.append(option_text_rect)  # Store the positioned rect

    def update_options(self):
        for i in range(len(self.option_text_objects)):
            if i == self.selected:
                self.option_text_objects[i].set_alpha(255)
            else:
                self.option_text_objects[i].set_alpha(150)

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
        screen.blit(self.background, self.background_rect)
        # Use the stored positioned rect for title
        screen.blit(self.title_object, self.title_rect)

        # Use the stored positioned rects for options
        for i, option_surface in enumerate(self.option_text_objects):
            screen.blit(option_surface, self.option_text_rects[i])
        screen.blit(self.pikachu_front, (150, 50))

    def on_select(self):
        match self.selected:
            case 0:
                Game().change_state("intro")
            case 1:
                Game().change_state("settings")
            case 2:
                Game().stop()
