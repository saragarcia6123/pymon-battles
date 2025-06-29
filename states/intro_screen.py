from pygame import Surface

from state import State


class IntroScreen(State):

    def __init__(self) -> None:
        super().__init__()

    def tick(self):
        super().tick()

    def render(self, screen: Surface):
        super().render(screen)
        screen.fill("white")

    def key_down(self, key: int):
        super().key_down(key)
