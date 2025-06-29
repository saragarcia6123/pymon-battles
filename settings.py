import pygame


available_settings = {
    "Text Speed": ["Slow", "Normal", "Fast"],
    "Difficulty": ["Easy", "Medium", "Hard"],
}

current_settings = {
    key: options_list[1] for key, options_list in available_settings.items()
}

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
