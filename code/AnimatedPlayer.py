import pygame
from code.Entity import Entity
from code.Const import (
    WIN_WIDTH, WIN_HEIGHT, ENTITY_SHOT_DELAY, ENTITY_SPEED,
    PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, PLAYER_KEY_RIGHT,
    ENTITY_HEALTH, PLAYER_KEY_ATTACK, INVINCIBILITY_DURATION_FRAMES, ATTACK_MOVE_FACTOR, FRAME_DELAY,
    HURT_SPRITE_DURATION_FRAMES, ATTACK_SPRITE_DURATION_FRAMES
)
from code.PlayerShot import PlayerShot


class AnimatedPlayer(Entity):
    def __init__(self, name: str, position: tuple = (10, WIN_HEIGHT // 2), frames_count=4):
        super().__init__(name, position)
        self.health = ENTITY_HEALTH.get(name, 100)
        self.enemies_killed = 0
        self.current_frame = 0
        self.frame_delay = FRAME_DELAY
        self.frame_counter = 0
        self.corn_count = 20
        self.kills = 0
        self.corn_collected = 0
        self.shot_timer = 0
        self.hurt_timer = 0
        self.attack_timer = 0
        self.invincibility_timer = 0

        self.normal_frames = self.__load_frames_from_sheet(f'{name}', frames_count)
        self.attack_frames = self.__load_frames_from_sheet(f'{name}Attack', frames_count=4)
        self.damage_frames = self.__load_frames_from_sheet(f'{name}Damage', frames_count=4)

        self.frames = self.normal_frames
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.last_dmg = None

    @staticmethod
    def __load_frames_from_sheet(sprite_name: str, frames_count: int):
        frames = []
        try:
            sheet = pygame.image.load(f'./asset/{sprite_name}.png').convert_alpha()
            frame_width = sheet.get_width() // frames_count
            frame_height = sheet.get_height()
            for i in range(frames_count):
                frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frames.append(frame)
        except pygame.error as e:
            print(f'[AVISO] Não foi possível carregar sprite {sprite_name}.png: {e}. Usando Surface padrão.')
            frames = [pygame.Surface((50, 50), pygame.SRCALPHA)]
        return frames

    def move(self, pressed_keys):
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0:
                self.frames = self.normal_frames
                self.current_frame = 0

        if self.attack_timer > 0:
            self.attack_timer -= 1
            self.rect.centerx += ENTITY_SPEED[self.name] * ATTACK_MOVE_FACTOR
            if self.attack_timer == 0:
                self.frames = self.normal_frames
                self.current_frame = 0

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        if pressed_keys[PLAYER_KEY_UP[self.name]]:
            self.rect.move_ip(0, -ENTITY_SPEED[self.name])
        if pressed_keys[PLAYER_KEY_DOWN[self.name]]:
            self.rect.move_ip(0, ENTITY_SPEED[self.name])
        if pressed_keys[PLAYER_KEY_LEFT[self.name]]:
            self.rect.move_ip(-ENTITY_SPEED[self.name], 0)
        if pressed_keys[PLAYER_KEY_RIGHT[self.name]]:
            self.rect.move_ip(ENTITY_SPEED[self.name], 0)

        if pressed_keys[PLAYER_KEY_ATTACK[self.name]]:
            self.attack()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_WIDTH / 2:
            self.rect.right = WIN_WIDTH / 2
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            if self.frames:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.surf = self.frames[self.current_frame]

        if self.shot_timer > 0:
            self.shot_timer -= 1

    def shoot(self):
        if self.shot_timer == 0 and self.corn_count > 0:
            self.corn_count -= 1
            self.shot_timer = ENTITY_SHOT_DELAY.get(self.name, 20)
            if pygame.mixer.get_init():
                try:
                    shoot_sound = pygame.mixer.Sound("./asset/shoot.wav")
                    shoot_sound.play()
                except pygame.error:
                    print("[AVISO] Erro ao tocar shoot.wav")
            return PlayerShot(name='PlayerShot', position=(self.rect.centerx, self.rect.centery),
                              player_name=self.name)
        return None

    def take_damage(self, amount):
        if self.invincibility_timer == 0:
            self.health -= amount
            self.last_dmg = 'Enemy'
            self.hurt_timer = HURT_SPRITE_DURATION_FRAMES
            self.invincibility_timer = INVINCIBILITY_DURATION_FRAMES
            self.frames = self.damage_frames
            self.current_frame = 0

    def attack(self):
        if self.attack_timer == 0:
            self.attack_timer = ATTACK_SPRITE_DURATION_FRAMES
            self.frames = self.attack_frames
            self.current_frame = 0
            return True
        return False
