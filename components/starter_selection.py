from collections.abc import Callable
import pygame

from entity import Entity
from game import Game
from resource_loader import ResourceLoader
from settings import DIMENSIONS, key_bindings


class StarterSelection(Entity):

    def __init__(self, on_enter: Callable[[int], None]) -> None:
        super().__init__()
        self.on_enter = on_enter
        self.selected = 1
        sprites = ResourceLoader().load_sprite_group("pokemon_battle_front")
        self.starter_sprites = [sprites[i-1] for i in [1, 4, 7]]
        self.sprite_width = 64
        self.sprite_height = 64

        if self.starter_sprites[0]:
            # Calculate positions for centered horizontal layout
            self.sprite_width = (
                self.starter_sprites[0].get_width() if self.starter_sprites else 100
            )
            self.sprite_height = (
                self.starter_sprites[0].get_height() if self.starter_sprites else 100
            )

        # Spacing between sprites
        self.sprite_spacing = 100

        # Total width needed for all sprites and spacing
        total_width = (
            len(self.starter_sprites) * self.sprite_width
            + (len(self.starter_sprites) - 1) * self.sprite_spacing
        )

        # Center horizontally on screen
        start_x = (DIMENSIONS[0] - total_width) // 2
        center_y = DIMENSIONS[1] // 2

        # Store sprite positions
        self.sprite_positions = []
        for i in range(len(self.starter_sprites)):
            x = start_x + i * (self.sprite_width + self.sprite_spacing)
            y = center_y - self.sprite_height // 2
            self.sprite_positions.append((x, y))

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)

        # Draw each starter sprite
        for i, (sprite, position) in enumerate(
            zip(self.starter_sprites, self.sprite_positions)
        ):
            if i == self.selected:
                sprite.set_alpha(255)
            else:
                # Non-selected sprites: reduced saturation (more grayscale)
                sprite.set_alpha(100)
            screen.blit(sprite, position)

    def key_down(self, key: int):
        super().key_down(key)
        if key == key_bindings["left"]:
            self.selected = (self.selected - 1) % len(self.starter_sprites)
        if key == key_bindings["right"]:
            self.selected = (self.selected + 1) % len(self.starter_sprites)
        if key == key_bindings["a"]:
            self.on_enter(self.selected)
