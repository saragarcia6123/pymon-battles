import pygame

from game import Game
from state import State
from settings import key_bindings


class SettingsMenu(State):

    def __init__(self, prev_state: State | None) -> None:
        super().__init__((0, 0, 0))
        self.selected = 0
        self.prev_state = prev_state

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def key_down(self, key: int):
        super().key_down(key)
        if key == key_bindings["b"]:
            Game().STATE = self.prev_state
        if key == key_bindings["a"]:
            self.on_select()

    def on_select(self):
        pass
