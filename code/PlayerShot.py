from code.Entity import Entity
from code.Const import ENTITY_SPEED, WIN_WIDTH


class PlayerShot(Entity):
    def __init__(self, name: str, position: tuple, player_name: str = None):
        sprite_to_load = f'{player_name}Shot' if player_name else name
        super().__init__(name, position, sprite_name=sprite_to_load)
        self.player_name = player_name  # Adicionado: armazena o nome do jogador

    def move(self, *args, **kwargs):
        self.rect.centerx += ENTITY_SPEED.get(self.name, 10)
        if self.rect.left > WIN_WIDTH:
            self.health = 0
