from code.Entity import Entity
from code.Const import DEAD_ENTITY_TIMER


class DeadEnemy(Entity):
    def __init__(self, sprite_name: str, position: tuple):
        super().__init__(sprite_name, position)
        self.timer = DEAD_ENTITY_TIMER

    def move(self, *args, **kwargs):
        self.timer -= 1
        if self.timer <= 0:
            self.health = 0
