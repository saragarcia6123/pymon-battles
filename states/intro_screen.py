import pygame

from components.dialog_box import DialogBox
from components.name_selection import NameSelection
from components.starter_selection import StarterSelection
from entity import Entity
from game import Game
from resource_loader import ResourceLoader
from settings import DIMENSIONS
from state import State
from states.battle import Battle


class IntroScreen(State):

    scenes: dict[int, str] = {
        0: "welcome",
        1: "name",
        2: "greet",
        3: "starter_intro",
        4: "starter",
        5: "confirmation",
        6: "final",
    }

    def __init__(self) -> None:
        super().__init__((255, 255, 255))
        self.oak_sprite = ResourceLoader().load_sprite("res/sprites/oak.png")
        self.oak_sprite_rect = self.oak_sprite.get_rect(
            center=(int(DIMENSIONS[0] / 2), int(DIMENSIONS[1] * 0.3))
        )

        # Create dialogs with proper callbacks
        self.welcome_dialog = DialogBox(
            "Hello there! Welcome to the world of POKEMON! My name is OAK! People call me the POKEMON PROF! This world is inhabited by creatures called POKEMON! For some people, POKEMON are pets. Others use them for fights. Myself...I study POKEMON as a profession. First, what is your name?",
            self.next_scene,
        )

        self.name_selection = NameSelection(on_enter=self.on_name_enter)
        self.starter_selection = StarterSelection(on_enter=self.on_starter_selected)

        # Store selected starter info for later use
        self.selected_starter_id = None
        self.selected_starter_name = None

        self.scene_objects: dict[str, list[Entity]] = {
            "welcome": [self.welcome_dialog],
            "name": [self.name_selection],
            "greet": [],
            "starter_intro": [],
            "starter": [self.starter_selection],
            "confirmation": [],
            "final": [],
        }

        self.scene_id = -1
        self.next_scene()

    def on_name_enter(self, name: str):
        Game().player_name = name

        # Create greet dialog with proper callback
        greet_dialog = DialogBox(f"Right! So your name is {name}!", self.next_scene)
        self.scene_objects["greet"] = [greet_dialog]
        self.next_scene()

    def on_starter_selected(self, starter_index: int):
        # Map starter index to Pokemon IDs (1=Bulbasaur, 4=Charmander, 7=Squirtle)
        starter_ids = [1, 4, 7]
        starter_names = ["BULBASAUR", "CHARMANDER", "SQUIRTLE"]

        self.selected_starter_id = starter_ids[starter_index]
        self.selected_starter_name = starter_names[starter_index]

        # Store the selected starter in the game state
        Game().player_starter = self.selected_starter_id

        # Create confirmation dialog with proper callback
        confirmation_dialog = DialogBox(
            f"So! You want the {self.selected_starter_name}? This Pokemon is really energetic! Are you sure about this choice?",
            self.next_scene,
        )
        self.scene_objects["confirmation"] = [confirmation_dialog]
        self.next_scene()

    def create_final_dialog(self):
        """Create the final dialog after confirmation"""
        final_dialog = DialogBox(
            f"{Game().player_name} received {self.selected_starter_name}! This is your very first Pokemon! You and {self.selected_starter_name} will surely become great partners!",
            self.next_scene,
        )
        self.scene_objects["final"] = [final_dialog]

    def create_starter_intro_dialog(self):
        """Create the starter introduction dialog"""
        starter_intro_dialog = DialogBox(
            f"Now, {Game().player_name}, inside these Poke Balls are Pokemon. When I was young, I was a serious Pokemon Trainer. In my old age, I have only three left, but you can have one. Choose!",
            self.next_scene,
        )
        self.scene_objects["starter_intro"] = [starter_intro_dialog]

    def next_scene(self):
        self.scene_id += 1
        self.objects = []

        if self.scene_id >= len(self.scenes):
            # Transition to battle state
            Game().STATE = Battle()
            return

        scene_name = self.scenes[self.scene_id]

        # Handle special scene setups
        if scene_name == "starter_intro":
            self.create_starter_intro_dialog()
        elif scene_name == "final":
            self.create_final_dialog()

        # Set the current scene objects
        self.objects = self.scene_objects[scene_name]

    def tick(self):
        super().tick()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        screen.blit(self.oak_sprite, self.oak_sprite_rect)

    def key_down(self, key: int):
        super().key_down(key)
