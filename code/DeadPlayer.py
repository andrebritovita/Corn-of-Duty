from code.Entity import Entity
from code.Const import DEAD_PLAYER_TIMER


class DeadPlayer(Entity):
    def __init__(self, position: tuple, player_name: str = "Player1"):
        sprite_name = f'{player_name}Die'
        super().__init__(sprite_name, position, health=1, damage=0, score=0)
        self.timer = DEAD_PLAYER_TIMER

    def move(self, *args, **kwargs):
        self.timer -= 1
        if self.timer <= 0:
            self.health = 0
