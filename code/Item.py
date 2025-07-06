import random
from code.Const import ENTITY_SPEED, WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity


class Item(Entity):
    def __init__(self, name: str, position: tuple = None, sprite_name: str = None):
        if position is None:
            position = (WIN_WIDTH + 10, random.randint(30, WIN_HEIGHT - 30))
        super().__init__(name, position, health=1, damage=0, score=0, sprite_name=sprite_name)

    def move(self, *args, **kwargs):
        self.rect.centerx -= ENTITY_SPEED.get(self.name, 2)
