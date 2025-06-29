from typing import Literal
import pygame

from state import State

type StateType = Literal["start", "settings", "intro"]


class Game:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Game, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    WIDTH = 500
    HEIGHT = 500

    settings_options = {
        "Text Speed": ["Slow", "Normal", "Fast"],
        "Difficulty": ["Easy", "Medium", "Hard"],
    }

    settings = {key: options_list[1] for key, options_list in settings_options.items()}

    def init(self) -> None:

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.STATE: State | None = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True

    def stop(self):
        if not self.running:
            return
        self.running = False

    def tick(self):
        if not self.STATE:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN:
                self.STATE.key_down(event.key)
        self.STATE.tick()

    def render(self):
        if not self.STATE:
            return
        self.screen.fill("black")
        self.STATE.render(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def change_state(self, state: StateType):
        match state:
            case "start":
                from states.start_screen import StartScreen

                self.STATE = StartScreen()
            case "settings":
                from states.settings_screen import SettingsScreen

                self.STATE = SettingsScreen()
            case "intro":
                from states.intro_screen import IntroScreen

                self.STATE = IntroScreen()
