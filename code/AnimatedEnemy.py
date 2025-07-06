import pygame
import random
from code.Entity import Entity
from code.Const import (
    ENTITY_SPEED, WIN_WIDTH, WIN_HEIGHT,
    ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE, FRAME_DELAY, HURT_SPRITE_DURATION_FRAMES
)


class AnimatedEnemy(Entity):
    def __init__(self, name: str, position=None, frames_count=6, flip=True):
        if position is None:
            position = (WIN_WIDTH + 10, random.randint(30, WIN_HEIGHT - 30))

        super().__init__(name, position)

        self.original_name = name
        self.flip = flip
        self.frames_count = frames_count
        self.frames = self.load_frames(self.original_name)
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

        self.current_frame = 0
        self.frame_delay = FRAME_DELAY
        self.frame_counter = 0

        self.health = ENTITY_HEALTH.get(self.original_name, 30)
        self.damage = ENTITY_DAMAGE.get(self.original_name, 15)
        self.score = ENTITY_SCORE.get(self.original_name, 150)
        self.last_dmg = None
        self.last_dmg_time = 0
        self.hurt_timer = 0

    def load_frames(self, sprite_base_name):
        """Carrega os frames do sprite sheet e aplica flip se necessário"""
        try:
            sheet = pygame.image.load(f'./asset/{sprite_base_name}.png').convert_alpha()
        except FileNotFoundError:
            print(f"[ERRO] Arquivo ./asset/{sprite_base_name}.png não encontrado!")
            raise

        frame_width = sheet.get_width() // self.frames_count
        frame_height = sheet.get_height()
        frames = []

        for i in range(self.frames_count):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            if self.flip:
                frame = pygame.transform.flip(frame, True, False)
            frames.append(frame)

        return frames

    def take_damage(self, amount):
        self.health -= amount
        self.last_dmg_time = pygame.time.get_ticks()

        if self.health > 0:
            # Troca para sprite ferido ex: EnemyHurt1 ou EnemyHurt2
            hurt_sprite = self.original_name.replace('Enemy', 'EnemyHurt')
            self.frames = self.load_frames(hurt_sprite)
            self.current_frame = 0  # Reinicia o frame para iniciar a animação de ferido
            self.hurt_timer = HURT_SPRITE_DURATION_FRAMES  # Define a duração do sprite de ferido
        else:
            # Troca para sprite morto ex: EnemyDead1 ou EnemyDead2
            dead_sprite = self.original_name.replace('Enemy', 'EnemyDead')
            self.frames = self.load_frames(dead_sprite)
            self.current_frame = 0  # Reinicia o frame para iniciar a animação de morto

    def move(self):
        self.rect.centerx -= ENTITY_SPEED.get(self.original_name, 2)

        # Gerencia o timer do sprite de ferido
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0:
                # Volta para os frames normais após o timer de ferido
                self.frames = self.load_frames(self.original_name)
                self.current_frame = 0

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.surf = self.frames[self.current_frame]
            self.frame_counter = 0

    @staticmethod
    def shoot():
        return None  # Futuro comportamento
