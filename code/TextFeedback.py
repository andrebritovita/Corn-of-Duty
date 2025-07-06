import pygame
from code.Entity import Entity


class TextFeedback(Entity):
    def __init__(self, text, position, color=(255, 255, 0)):
        self.text = text
        self.alpha = 255
        self.timer = 30
        self.dy = 1

        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 14)
        rendered_surf = self.font.render(text, True, color).convert_alpha()
        super().__init__("Feedback", position, health=1, damage=0, score=0, surface=rendered_surf)
        self.rect.center = position

    def move(self, *args, **kwargs):
        self.rect.centery -= self.dy
        self.timer -= 1

        self.alpha = max(0, int(255 * (self.timer / 30)))
        self.surf.set_alpha(self.alpha)

        if self.timer <= 0:
            self.health = 0
