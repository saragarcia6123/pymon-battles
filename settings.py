import pygame


text_speed = 1

key_bindings: dict[str, int] = {
    "a": pygame.K_x,
    "b": pygame.K_z,
    "start": pygame.K_RETURN,
    "select": pygame.K_BACKSPACE,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "toggle_fullscreen": pygame.K_ESCAPE,
}
