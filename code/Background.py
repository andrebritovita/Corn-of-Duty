from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Entity import Entity
import pygame


class Background(Entity):
    def __init__(self, name: str, position: tuple, speed: int):
        super().__init__(name, position)
        self.health = 999_999
        self.speed = speed

        self.image = pygame.image.load(f'./asset/{name}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIN_WIDTH, WIN_HEIGHT))

        self.x1 = 0
        self.x2 = WIN_WIDTH

    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -WIN_WIDTH:
            self.x1 = self.x2 + WIN_WIDTH
        if self.x2 <= -WIN_WIDTH:
            self.x2 = self.x1 + WIN_WIDTH

    def draw(self, window):
        window.blit(self.image, (self.x1, 0))
        window.blit(self.image, (self.x2, 0))
