import pygame


# renderable pygame object
class Sprite:

    def __init__(self, source: pygame.Surface, dest: pygame.Rect) -> None:
        self.source = source
        self.dest = dest

    def render(self, screen: pygame.Surface):
        screen.blit(self.source, self.dest)
