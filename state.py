import pygame

from components.dialog_box import DialogBox
from entity import Entity


class State:

    def __init__(self, bg: tuple) -> None:
        self.objects: list[Entity] = []
        self.bg = bg
        self.dialog_box: DialogBox | None = None

    def tick(self):
        if self.dialog_box:
            self.dialog_box.tick()
        for o in self.objects:
            o.tick()

    def render(self, screen: pygame.Surface):
        screen.fill(self.bg)
        for o in self.objects:
            o.render(screen)
        if self.dialog_box:
            self.dialog_box.render(screen)

    def key_down(self, key: int):
        if self.dialog_box:
            self.dialog_box.key_down(key)
        for o in self.objects:
            o.key_down(key)
