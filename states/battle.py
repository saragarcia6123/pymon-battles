from pygame import Surface
from components.dialog_box import DialogBox
from pokemon_ids import POKE_ID_MAP
from resource_loader import ResourceLoader
from state import State


class Battle(State):

    def __init__(self) -> None:
        super().__init__((255, 255, 255))
        sprites = ResourceLoader().load_sprite_group("pokemon_battle_front")
        self.pikachu_front = sprites[POKE_ID_MAP["pikachu"]-1]
        self.dialog = DialogBox(
            "There would be a battle here but I didn't get anywhere near finishing",
            lambda: None,
        )

    def tick(self):
        super().tick()
        self.dialog.tick()

    def render(self, screen: Surface):
        super().render(screen)
        self.dialog.render(screen)
        screen.blit(self.pikachu_front, (250, 100))

    def key_down(self, key: int):
        super().key_down(key)
        self.dialog.key_down(key)
