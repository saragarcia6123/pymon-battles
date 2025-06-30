import pygame
from typing import Callable
from entity import Entity
from game import Game
from resources import DEFAULT_FONT
from settings import DIMENSIONS, key_bindings


class NameSelection(Entity):

    def __init__(self, on_enter: Callable[[str], None]) -> None:
        super().__init__()
        self.on_enter = on_enter
        self.name = ""
        self.max_name_length = 10
        self.current_row = 0
        self.current_col = 0

        # Keyboard layout - A-Z with 10 per row, plus OK
        self.keyboard = [
            ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
            ["U", "V", "W", "X", "Y", "Z", "OK"],
        ]

        # Dialog dimensions (same as DialogBox)
        self.width = int(DIMENSIONS[0] * 0.9)
        self.height = int(DIMENSIONS[1] * 0.2)
        self.border_gap = int((DIMENSIONS[0] - self.width) / 2)

        # Name display dimensions
        self.name_height = 60
        self.name_gap = self.border_gap

        # Prompt text dimensions
        self.prompt_height = 40
        self.prompt_gap = 10

        # Calculate positions
        self.dialog_x = self.border_gap
        self.dialog_y = DIMENSIONS[1] - self.height - self.border_gap

        self.name_x = self.border_gap
        self.name_y = self.dialog_y - self.name_height - self.name_gap

        self.prompt_x = self.border_gap
        self.prompt_y = self.name_y - self.prompt_height - self.prompt_gap

    def key_down(self, key: int):
        if key == key_bindings["a"]:
            current_char = self.keyboard[self.current_row][self.current_col]
            if current_char == "OK":
                # Call the callback with the current name
                self.on_enter(self.name)
            else:
                # Select character if not over limit
                if len(self.name) < self.max_name_length:
                    self.name += current_char

        elif key == key_bindings["b"]:
            # Delete character if name has characters
            if len(self.name) > 0:
                self.name = self.name[:-1]

        elif key == key_bindings["up"]:
            if self.current_row > 0:
                self.current_row -= 1
                self.current_col = min(
                    self.current_col, len(self.keyboard[self.current_row]) - 1
                )

        elif key == key_bindings["down"]:
            if self.current_row < len(self.keyboard) - 1:
                self.current_row += 1
                self.current_col = min(
                    self.current_col, len(self.keyboard[self.current_row]) - 1
                )

        elif key == key_bindings["left"]:
            if self.current_col > 0:
                self.current_col -= 1

        elif key == key_bindings["right"]:
            max_col = len(self.keyboard[self.current_row]) - 1
            if self.current_col < max_col:
                self.current_col += 1

    def get_name_display(self) -> str:
        """Get the name with underscores for remaining slots"""
        display_name = self.name
        remaining_slots = self.max_name_length - len(self.name)
        display_name += "_" * remaining_slots
        return display_name

    def render(self, screen: pygame.Surface):
        # Draw prompt text background
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.prompt_x, self.prompt_y, self.width, self.prompt_height),
        )

        # Draw prompt text border
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.prompt_x, self.prompt_y, self.width, self.prompt_height),
            2,
        )

        # Draw prompt text (centered)
        prompt_surface = DEFAULT_FONT.render("Enter your name", True, (0, 0, 0))
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.center = (
            self.prompt_x + self.width // 2,
            self.prompt_y + self.prompt_height // 2,
        )
        screen.blit(prompt_surface, prompt_rect)

        # Draw name display background
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.name_x, self.name_y, self.width, self.name_height),
        )

        # Draw name display border
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.name_x, self.name_y, self.width, self.name_height),
            2,
        )

        # Draw name text (centered)
        name_display = self.get_name_display()
        name_surface = DEFAULT_FONT.render(name_display, True, (0, 0, 0))
        name_rect = name_surface.get_rect()
        name_rect.center = (
            self.name_x + self.width // 2,
            self.name_y + self.name_height // 2,
        )
        screen.blit(name_surface, name_rect)

        # Draw keyboard background
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.dialog_x, self.dialog_y, self.width, self.height),
        )

        # Draw keyboard border
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.dialog_x, self.dialog_y, self.width, self.height),
            2,
        )

        # Calculate keyboard layout
        char_width = DEFAULT_FONT.size("A")[0]
        char_height = DEFAULT_FONT.get_height()

        # Space between characters
        total_chars_per_row = 10
        total_char_width = total_chars_per_row * char_width
        spacing = (self.width - 40 - total_char_width) // (
            total_chars_per_row - 1
        )  # 40 for padding

        start_x = self.dialog_x + 20
        start_y = self.dialog_y + 20

        # Draw keyboard characters
        for row_idx, row in enumerate(self.keyboard):
            y_pos = start_y + row_idx * (char_height + 10)

            # Center the row
            row_width = len(row) * char_width + (len(row) - 1) * spacing
            row_start_x = (
                start_x
                + (total_char_width + (total_chars_per_row - 1) * spacing - row_width)
                // 2
            )

            for col_idx, char in enumerate(row):
                x_pos = row_start_x + col_idx * (char_width + spacing)

                # Highlight selected character
                if self.current_row == row_idx and self.current_col == col_idx:
                    highlight_rect = pygame.Rect(
                        x_pos - 5, y_pos - 2, char_width + 10, char_height + 4
                    )
                    pygame.draw.rect(screen, (200, 200, 200), highlight_rect)

                char_surface = DEFAULT_FONT.render(char, True, (0, 0, 0))
                screen.blit(char_surface, (x_pos, y_pos))
