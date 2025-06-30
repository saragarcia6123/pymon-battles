from collections.abc import Callable
import pygame
from entity import Entity
from resources import DEFAULT_FONT
from settings import DIMENSIONS, key_bindings


class DialogBox(Entity):

    text_delay_map = {
        0: 3,
        1: 2,
        2: 1,
    }

    def __init__(self, message: str, on_close: Callable) -> None:
        super().__init__()
        self.objects = []
        self.ticks = 0
        self.letter_state = 0
        self.width = int(DIMENSIONS[0] * 0.9)
        self.height = int(DIMENSIONS[1] * 0.2)
        self.border_gap = int((DIMENSIONS[0] - self.width) / 2)
        self.on_close = on_close
        avg_char_width = DEFAULT_FONT.size("A")[0]
        self.letters_per_line = self.width // avg_char_width
        self.message = message
        self.current_page = 0  # Track which page of 3 lines we're on
        self.lines_per_page = 3
        self.all_lines = []  # Store all processed lines
        self.typing_complete = False  # Track if current page finished typing

        # Calculate dialog box position
        self.dialog_x = self.border_gap
        self.dialog_y = DIMENSIONS[1] - self.height - self.border_gap

        self.set_text_object()

    def split_message(self, message: str) -> list[str]:
        lines = []
        current_line = ""
        char_count = 0

        for word in message.split(" "):
            space = 1 if current_line else 0
            total_len = len(word) + space

            # stop if word wouldn't fit
            if char_count + total_len > self.letter_state:
                break

            # check if wrap to new line
            if len(current_line) + total_len > self.letters_per_line:
                # check if the word would fit
                if char_count + len(word) > self.letter_state:
                    break

                lines.append(current_line)
                current_line = word
                char_count += len(word)
            else:
                current_line += (" " if current_line else "") + word
                char_count += total_len

        if current_line:
            lines.append(current_line)

        return lines

    def get_full_message_lines(self) -> list[str]:
        """Get all lines of the complete message for pagination"""
        lines = []
        current_line = ""

        for word in self.message.split(" "):
            space = 1 if current_line else 0
            total_len = len(word) + space

            # check if wrap to new line
            if len(current_line) + total_len > self.letters_per_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line += (" " if current_line else "") + word

        if current_line:
            lines.append(current_line)

        return lines

    def get_current_page_lines(self) -> list[str]:
        """Get the lines for the current page (up to 3 lines)"""
        if not self.all_lines:
            self.all_lines = self.get_full_message_lines()

        start_idx = self.current_page * self.lines_per_page
        end_idx = start_idx + self.lines_per_page
        return self.all_lines[start_idx:end_idx]

    def is_current_page_complete(self) -> bool:
        """Check if all characters for current page have been revealed"""
        current_page_lines = self.get_current_page_lines()
        total_chars_in_page = sum(len(line) for line in current_page_lines)

        # Account for spaces between lines in character counting
        if len(current_page_lines) > 1:
            total_chars_in_page += len(current_page_lines) - 1

        return self.letter_state >= total_chars_in_page

    def has_more_pages(self) -> bool:
        """Check if there are more pages to show"""
        if not self.all_lines:
            self.all_lines = self.get_full_message_lines()

        total_pages = (
            len(self.all_lines) + self.lines_per_page - 1
        ) // self.lines_per_page
        return self.current_page < total_pages - 1

    def key_down(self, key: int):
        if key == key_bindings["a"]:
            if self.is_current_page_complete():
                if self.has_more_pages():
                    # Move to next page
                    self.current_page += 1
                    self.letter_state = 0  # Reset typing animation
                    self.typing_complete = False
                    self.set_text_object()
                else:
                    self.on_close()
            else:
                # Skip typing animation and show full current page
                current_page_lines = self.get_current_page_lines()
                self.letter_state = sum(len(line) for line in current_page_lines)
                if len(current_page_lines) > 1:
                    self.letter_state += len(current_page_lines) - 1
                self.set_text_object()

    def set_text_object(self):
        # Get current page lines and create a temporary message for letter-by-letter reveal
        current_page_lines = self.get_current_page_lines()
        current_page_message = " ".join(current_page_lines)

        visible_message = current_page_message[: self.letter_state]
        self.lines = self.split_message(visible_message)

        # Only show up to 3 lines
        self.lines = self.lines[: self.lines_per_page]

        self.text_surfaces = [
            DEFAULT_FONT.render(line, True, (0, 0, 0)) for line in self.lines
        ]

        # Positioning with more padding
        start_x = self.border_gap + 20  # More padding from left edge
        start_y = (
            DIMENSIONS[1] - self.height - self.border_gap + 20
        )  # More padding from top inside box

        self.text_positions = []
        line_height = DEFAULT_FONT.get_height() + 4

        for i, surface in enumerate(self.text_surfaces):
            rect = surface.get_rect()
            rect.left = start_x
            rect.top = start_y + i * line_height
            self.text_positions.append(rect)

    def tick(self):
        if not self.is_current_page_complete():
            self.ticks += 1
            from states.settings_menu import current_settings

            delay = self.text_delay_map[current_settings["text-speed"]]
            if self.ticks % delay == 0:
                self.letter_state += 1
                self.set_text_object()

    def render(self, screen: pygame.Surface):
        # Draw white background
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.dialog_x, self.dialog_y, self.width, self.height),
        )

        # Draw black border
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.dialog_x, self.dialog_y, self.width, self.height),
            2,
        )

        # Draw text on top
        for surface, rect in zip(self.text_surfaces, self.text_positions):
            screen.blit(surface, rect)

        # Draw '...' indicator when more pages are ready
        if self.is_current_page_complete() and self.has_more_pages():
            dots_text = DEFAULT_FONT.render("...", True, (0, 0, 0))
            dots_rect = dots_text.get_rect()
            # Position in bottom right with padding
            dots_rect.right = self.dialog_x + self.width - 10
            dots_rect.bottom = self.dialog_y + self.height - 10
            screen.blit(dots_text, dots_rect)
