import pygame

from game_object import GameObject


class State(GameObject):

    def __init__(self, bg: tuple) -> None:
        self.objects: list[GameObject] = []
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
