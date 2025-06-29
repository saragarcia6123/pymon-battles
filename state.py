import pygame

from entity import Entity


class State:

    def __init__(self, bg: tuple) -> None:
        self.objects: list[Entity] = []
        self.bg = bg

    def tick(self):
        for o in self.objects:
            o.tick()

    def render(self, screen: pygame.Surface):
        screen.fill(self.bg)
        for o in self.objects:
            o.render(screen)

    def key_down(self, key: int):
        for o in self.objects:
            o.key_down(key)
