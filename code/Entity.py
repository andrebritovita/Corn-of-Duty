from abc import ABC, abstractmethod
import pygame.image
import pygame
from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):
    def __init__(self, name: str, position: tuple,
                 health: int = None, damage: int = None, score: int = None,
                 surface: pygame.Surface = None, sprite_name: str = None):
        self.name = name

        asset_name = sprite_name if sprite_name else name

        if surface:
            self.surf = surface
        else:
            try:
                self.surf = pygame.image.load(f'./asset/{asset_name}.png').convert_alpha()
            except pygame.error as e:
                print(f"[AVISO] Não foi possível carregar sprite {asset_name}.png: {e}. Usando Surface padrão.")
                self.surf = pygame.Surface((1, 1), pygame.SRCALPHA)

        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.health = health if health is not None else ENTITY_HEALTH.get(self.name, 1)
        self.damage = damage if damage is not None else ENTITY_DAMAGE.get(self.name, 0)
        self.score = score if score is not None else ENTITY_SCORE.get(self.name, 0)
        self.last_dmg = None  # Adicionado para resolver o erro de atributo

    @abstractmethod
    def move(self, *args, **kwargs):
        pass
