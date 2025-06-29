import pygame


class GameObject:

    def __init__(self, source: pygame.Surface, dest: pygame.Rect) -> None:
        self.source = source
        self.dest = dest

    def tick(self):
        pass

    def render(self, screen: pygame.Surface):
        screen.blit(self.source, self.dest)

    def key_down(self, key: int):
        pass
