from typing import Literal
import pygame

from settings import DIMENSIONS
from state import State

type StateType = Literal["start", "settings", "intro"]


class Game:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Game, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self) -> None:
        self.screen = pygame.display.set_mode(DIMENSIONS)
        self.clock = pygame.time.Clock()

        self.STATE: State | None = None
        self.running = False
        self.ticks = 0
        self.timer = 0
        self.player_name = "RED"
        self.player_starter: int = 0

    def start(self):
        if self.running:
            return
        self.running = True

    def stop(self):
        if not self.running:
            return
        self.running = False

    def tick(self):
        self.ticks += 1
        if self.ticks % 60 == 0:
            self.timer += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN and self.STATE:
                self.STATE.key_down(event.key)
        if self.STATE:
            self.STATE.tick()

    def render(self):
        self.screen.fill("black")
        if self.STATE:
            self.STATE.render(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def change_state(self, state: StateType):
        match state:
            case "start":
                from states.start_menu import StartMenu

                self.STATE = StartMenu()
            case "settings":
                from states.settings_menu import SettingsMenu

                self.STATE = SettingsMenu(prev_state=self.STATE, on_back=self.set_state)
            case "intro":
                from states.intro_screen import IntroScreen

                self.STATE = IntroScreen()

    def set_state(self, state: State | None):
        if state:
            self.STATE = state
