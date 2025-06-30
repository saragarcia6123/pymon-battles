from collections.abc import Callable
from typing import Literal
import pygame

from resources import DEFAULT_FONT, TITLE_FONT
from state import State
from settings import DIMENSIONS, key_bindings


type SettingsKey = Literal["text-speed", "difficulty"]

current_settings: dict[SettingsKey, int] = {
    "text-speed": 1,  # NORMAL
    "difficulty": 1,  # MEDIUM
}


class SettingsMenu(State):

    game_settings: dict[SettingsKey, list[str]] = {
        "text-speed": ["SLOW", "NORMAL", "FAST"],
        "difficulty": ["EASY", "MEDIUM", "HARD"],
    }

    def __init__(
        self, prev_state: State | None, on_back: Callable[[State | None], None]
    ) -> None:
        super().__init__((20, 20, 50))
        self.selected = 0
        self.prev_state = prev_state
        self.on_back = on_back

        self.background = pygame.image.load("res/backgrounds/start_menu.png")
        self.background_rect = self.background.get_rect(
            center=(int(DIMENSIONS[0] / 2), int(DIMENSIONS[1] / 2))
        )

        self.init_title()
        self.init_settings()
        self.update_options()

    def init_title(self):
        self.title_object = TITLE_FONT.render("Settings", True, (255, 255, 0))
        self.title_rect = self.title_object.get_rect()  # Store the rect
        self.title_rect.centerx = int(DIMENSIONS[0] / 2)
        self.title_rect.centery = int(DIMENSIONS[1] * 0.25)

    def init_settings(
        self,
        offset: int = DIMENSIONS[1] - 250,
        gap: int = 80,
    ):
        self.setting_labels: list[pygame.Surface] = []
        self.setting_values: list[pygame.Surface] = []
        self.setting_arrows_left: list[pygame.Surface] = []
        self.setting_arrows_right: list[pygame.Surface] = []

        # Store all the rectangles
        self.setting_label_rects: list[pygame.Rect] = []
        self.setting_value_rects: list[pygame.Rect] = []
        self.setting_arrow_left_rects: list[pygame.Rect] = []
        self.setting_arrow_right_rects: list[pygame.Rect] = []

        setting_keys: list[SettingsKey] = list(self.game_settings.keys())

        for i, key in enumerate(setting_keys):
            # Create label (left side)
            label_text = key.replace("-", " ").title()
            label_object = DEFAULT_FONT.render(label_text, True, (255, 255, 255))
            label_rect = label_object.get_rect()
            label_rect.centerx = int(DIMENSIONS[0] * 0.35)
            label_rect.centery = offset + i * gap
            self.setting_labels.append(label_object)
            self.setting_label_rects.append(label_rect)  # Store rect

            # Create value display (center)
            current_value = current_settings[key]
            value_text = self.game_settings[key][current_value]
            value_object = DEFAULT_FONT.render(value_text, True, (255, 255, 255))
            value_rect = value_object.get_rect()
            value_rect.centerx = int(DIMENSIONS[0] * 0.65)
            value_rect.centery = offset + i * gap
            self.setting_values.append(value_object)
            self.setting_value_rects.append(value_rect)  # Store rect

            # Create arrows
            left_arrow = DEFAULT_FONT.render("<", True, (255, 255, 255))
            left_rect = left_arrow.get_rect()
            left_rect.centerx = int(DIMENSIONS[0] * 0.55)
            left_rect.centery = offset + i * gap
            self.setting_arrows_left.append(left_arrow)
            self.setting_arrow_left_rects.append(left_rect)  # Store rect

            right_arrow = DEFAULT_FONT.render(">", True, (255, 255, 255))
            right_rect = right_arrow.get_rect()
            right_rect.centerx = int(DIMENSIONS[0] * 0.75)
            right_rect.centery = offset + i * gap
            self.setting_arrows_right.append(right_arrow)
            self.setting_arrow_right_rects.append(right_rect)  # Store rect

    def update_options(self):
        # Update alpha for all elements based on selection
        for i in range(len(self.setting_labels)):
            alpha = 255 if i == self.selected else 150
            self.setting_labels[i].set_alpha(alpha)
            self.setting_values[i].set_alpha(alpha)
            self.setting_arrows_left[i].set_alpha(alpha)
            self.setting_arrows_right[i].set_alpha(alpha)

    def update_setting_value(self, setting_key: SettingsKey):
        """Update the display text for a specific setting"""
        setting_keys = list(self.game_settings.keys())
        index = setting_keys.index(setting_key)

        current_value = current_settings[setting_key]
        value_text = self.game_settings[setting_key][current_value]

        # Recreate the value surface with updated text
        self.setting_values[index] = DEFAULT_FONT.render(
            value_text, True, (255, 255, 255)
        )
        # Keep the same positioned rect (no need to recreate positioning)
        # The rect is already stored and positioned correctly

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.blit(self.background, self.background_rect)
        # Use stored positioned rect for title
        screen.blit(self.title_object, self.title_rect)

        # Render all setting elements using stored positioned rects
        for i in range(len(self.setting_labels)):
            screen.blit(self.setting_labels[i], self.setting_label_rects[i])
            screen.blit(self.setting_values[i], self.setting_value_rects[i])
            screen.blit(self.setting_arrows_left[i], self.setting_arrow_left_rects[i])
            screen.blit(self.setting_arrows_right[i], self.setting_arrow_right_rects[i])

    def key_down(self, key: int):
        super().key_down(key)
        if key == key_bindings["b"]:
            self.on_back(self.prev_state)
        if key == key_bindings["up"]:
            self.selected = (self.selected - 1) % len(self.game_settings)
            self.update_options()
        if key == key_bindings["down"]:
            self.selected = (self.selected + 1) % len(self.game_settings)
            self.update_options()
        if key == key_bindings["left"]:
            self.change_setting(-1)
        if key == key_bindings["right"]:
            self.change_setting(1)

    def change_setting(self, direction: int):
        """Change the current setting value in the given direction"""
        setting_keys = list(self.game_settings.keys())
        current_key = setting_keys[self.selected]

        current_value = current_settings[current_key]
        max_value = len(self.game_settings[current_key]) - 1

        # Calculate new value with wrapping
        new_value = (current_value + direction) % (max_value + 1)
        current_settings[current_key] = new_value

        # Update the display
        self.update_setting_value(current_key)
        self.update_options()
