import pygame


class State:

    def __init__(self) -> None:
        pass

    def tick(self):
        pass

    def render(self, screen: pygame.Surface):
        pass

    def key_down(self, key: int):
        pass
