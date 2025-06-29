from pygame import Surface

from components.dialog_box import DialogBox
from entity import Entity
from state import State


class IntroScreen(State):

    scenes: dict[int, str] = {
        0: "welcome",
        1: "name",
    }

    def __init__(self) -> None:
        super().__init__((255, 255, 255))
        dialog_box = DialogBox(
            "Hello there! Welcome to the world of POKEMON! My name is OAK! People call me the POKEMON PROF! This world is inhabited by creatures called POKEMON! For some people, POKEMON are pets. Others use them for fights. Myself...I study POKEMON as a profession. First, what is your name?",
            on_close=self.next_scene,
        )
        self.scene_objects: dict[str, list[Entity]] = {
            "welcome": [dialog_box],
            "name": [],
        }
        self.scene_id = -1
        self.next_scene()

    def next_scene(self):
        self.scene_id += 1
        self.objects = []
        scene_name = self.scenes[self.scene_id]
        self.objects = self.scene_objects[scene_name]

    def tick(self):
        super().tick()

    def render(self, screen: Surface):
        super().render(screen)

    def key_down(self, key: int):
        super().key_down(key)
