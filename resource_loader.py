import pygame
import json

class ResourceLoader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ResourceLoader, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.sheets: dict[str, pygame.Surface] = {}
        with open("res/sprite_sheet_data.json") as f:
            self.sheet_data: dict[str, dict] = json.load(f)
        self.sprites: dict[str, dict[int, pygame.Surface]] = {}

    def load_sprite(self, path: str):
        return pygame.image.load(path)

    def load_sprite_sheet(self, sheet_name: str) -> pygame.Surface:
        if sheet_name not in self.sheet_data["sheets"].keys():
            raise KeyError
        if sheet_name in self.sheets:
            return self.sheets[sheet_name]
        
        sprite_sheet = pygame.image.load(self.sheet_data["sheets"][sheet_name])
        self.sheets[sheet_name] = sprite_sheet
        return sprite_sheet

    def extract_sprite_at_position(self, sheet_name, x, y, width, height):
        sheet = self.load_sprite_sheet(sheet_name)
        sprite_rect = pygame.Rect(x, y, width, height)
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), sprite_rect)
        return sprite
    
    def load_sprite_group(self, sprite_type: str) -> dict[int, pygame.Surface]:
        if sprite_type not in self.sheet_data["bounds"].keys():
            raise KeyError
        if sprite_type in self.sprites:
            return self.sprites[sprite_type]
        
        self.sprites[sprite_type] = {}

        try:
            bounds = self.sheet_data["bounds"][sprite_type]
            sheet_name = bounds["sheet"]

            for index in range(bounds["total_sprites"]):
                row = index // bounds["sprites_per_row"]
                col = index % bounds["sprites_per_row"]
                x = bounds["start_x"] + col * (
                    bounds["width"] + bounds["column_gap"]
                )
                y = bounds["start_y"] + row * (
                    bounds["height"] + bounds["row_gap"]
                )
                sprite = self.extract_sprite_at_position(
                    sheet_name, x, y, bounds["width"], bounds["height"]
                )
                self.sprites[sprite_type][index] = sprite
            
            return self.sprites[sprite_type]
        except Exception as e:
            # clear in case anything goes wrong
            self.sprites.pop(sprite_type)
            raise e
