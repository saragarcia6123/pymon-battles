import pygame


class SpriteLoader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpriteLoader, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.sprites = {}
        self.pokemon_sprite_sheet = None

        # Layout specifications
        self.battle_sprite_size = 64
        self.pokedex_sprite_size = 32
        self.start_x = 8
        self.start_y = 24
        self.pokemon_per_row = 3
        self.row_gap = 8
        self.section_gap = 8
        self.total_pokemon = 151

    def load_sprite_sheets(self):
        """Load the main sprite sheet"""
        self.pokemon_sprite_sheet = pygame.image.load("res/sprite_sheets/pokemon.png")
        self._extract_all_sprites()

    def _get_pokemon_position(self, pokemon_id):
        """Calculate row and column for a given pokemon ID (1-151)"""
        pokemon_index = pokemon_id - 1  # Convert to 0-based index
        row = pokemon_index // self.pokemon_per_row
        col = pokemon_index % self.pokemon_per_row
        return row, col

    def _extract_battle_sprite(self, pokemon_id, is_back=False):
        """Extract battle front or back sprite for a pokemon"""
        if not self.pokemon_sprite_sheet:
            return None

        row, col = self._get_pokemon_position(pokemon_id)

        # Calculate position
        x = self.start_x + col * (
            self.battle_sprite_size
            + self.section_gap
            + self.battle_sprite_size
            + self.section_gap
        )
        if is_back:
            x += (
                self.battle_sprite_size
                + self.section_gap
                + self.battle_sprite_size
                + self.section_gap
            )  # Skip front + shiny front

        y = self.start_y + row * (self.battle_sprite_size + self.row_gap)

        sprite_rect = pygame.Rect(
            x, y, self.battle_sprite_size, self.battle_sprite_size
        )
        sprite = pygame.Surface(
            (self.battle_sprite_size, self.battle_sprite_size), pygame.SRCALPHA
        )
        sprite.blit(self.pokemon_sprite_sheet, (0, 0), sprite_rect)

        return sprite

    def _extract_pokedex_sprite(self, pokemon_id, top_sprite=True):
        """Extract pokedex sprite (top or bottom) for a pokemon"""
        if not self.pokemon_sprite_sheet:
            return None

        row, col = self._get_pokemon_position(pokemon_id)

        # Pokedex sprites are positioned after the battle sprites
        x = self.start_x + col * (
            self.battle_sprite_size
            + self.section_gap
            + self.battle_sprite_size
            + self.section_gap
        )
        x += (
            self.battle_sprite_size + self.section_gap
        ) * 4  # Skip all battle sprite sections

        y = self.start_y + row * (self.battle_sprite_size + self.row_gap)
        if not top_sprite:
            y += self.pokedex_sprite_size  # Move to bottom pokedex sprite

        sprite_rect = pygame.Rect(
            x, y, self.pokedex_sprite_size, self.pokedex_sprite_size
        )
        sprite = pygame.Surface(
            (self.pokedex_sprite_size, self.pokedex_sprite_size), pygame.SRCALPHA
        )
        sprite.blit(self.pokemon_sprite_sheet, (0, 0), sprite_rect)

        return sprite

    def _extract_all_sprites(self):
        """Extract all Pokemon sprites according to the format"""
        if not self.pokemon_sprite_sheet:
            return

        self.sprites = {}

        # Extract sprites for each Pokemon (1-151)
        for pokemon_id in range(1, self.total_pokemon + 1):
            self.sprites[pokemon_id] = {}

            # Extract battle front sprite
            battle_front = self._extract_battle_sprite(pokemon_id, is_back=False)
            if battle_front:
                self.sprites[pokemon_id]["battle_front"] = battle_front

            # Extract battle back sprite
            battle_back = self._extract_battle_sprite(pokemon_id, is_back=True)
            if battle_back:
                self.sprites[pokemon_id]["battle_back"] = battle_back

            # Extract pokedex sprite (only top sprite as requested)
            pokedex = self._extract_pokedex_sprite(pokemon_id, top_sprite=True)
            if pokedex:
                self.sprites[pokemon_id]["pokedex"] = pokedex

    def get_sprite(self, pokemon_id, sprite_type):
        """Get a specific sprite for a Pokemon

        Args:
            pokemon_id (int): Pokemon ID (1-151)
            sprite_type (str): 'battle_front', 'battle_back', or 'pokedex'

        Returns:
            pygame.Surface: The requested sprite, or None if not found
        """
        if pokemon_id in self.sprites and sprite_type in self.sprites[pokemon_id]:
            return self.sprites[pokemon_id][sprite_type]
        else:
            raise ValueError(f"Failed to get sprite for Pokemon ID {pokemon_id}")

    def get_all_sprites(self, pokemon_id):
        """Get all sprites for a specific Pokemon"""
        return self.sprites.get(pokemon_id, {})

    def get_pokemon_ids(self):
        """Get list of all available Pokemon IDs"""
        return list(self.sprites.keys())

    def _extract_sprite_at_position(self, x, y, size):
        """Helper method to extract sprite at specific coordinates"""
        if not self.pokemon_sprite_sheet:
            return None

        sprite_rect = pygame.Rect(x, y, size, size)
        sprite = pygame.Surface((size, size), pygame.SRCALPHA)
        sprite.blit(self.pokemon_sprite_sheet, (0, 0), sprite_rect)
        return sprite
