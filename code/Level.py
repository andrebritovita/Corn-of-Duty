import random
import pygame
from pygame import Surface
from pygame.font import Font

from code.AnimatedPlayer import AnimatedPlayer
from code.Background import Background
from code.Const import (
    C_WHITE, WIN_HEIGHT,
    EVENT_ENEMY, EVENT_TIMEOUT, TIMEOUT_STEP,
    EVENT_ITEM, SPAWN_ITEM_TIME,
    PLAYER1, PLAYER2, TIMEOUT_LEVEL, SPAWN_ENEMY_TIME,
    C_RED,
    PLAYER_KEY_SHOOT, WIN_WIDTH
)
from code.Credits import Credits
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.TextFeedback import TextFeedback
from code.utils import _quit_game


class Level:
    def __init__(self, window: Surface, name: str, player_data: dict):
        self.window = window
        self.name = name
        self.timeout = TIMEOUT_LEVEL
        self.entity_list: list[Entity] = []
        self.player_data = player_data

        bg_list = EntityFactory.get_entity(self.name + 'Bg')
        if bg_list:
            self.entity_list.extend(bg_list)

        if PLAYER1 in self.player_data:
            player1 = EntityFactory.get_entity(PLAYER1)
            if player1:
                player1.score = self.player_data[PLAYER1]['score']
                player1.kills = self.player_data[PLAYER1]['kills']
                player1.corn_collected = self.player_data[PLAYER1]['corn_collected']
                self.entity_list.append(player1)

        if PLAYER2 in self.player_data:
            player2 = EntityFactory.get_entity(PLAYER2)
            if player2:
                player2.score = self.player_data[PLAYER2]['score']
                player2.kills = self.player_data[PLAYER2]['kills']
                player2.corn_collected = self.player_data[PLAYER2]['corn_collected']
                self.entity_list.append(player2)

        # Ajuste do tempo de spawn dos inimigos para Level2 (mais difícil)
        enemy_spawn_time = SPAWN_ENEMY_TIME if self.name == 'Level1' else int(SPAWN_ENEMY_TIME * 0.6)
        pygame.time.set_timer(EVENT_ENEMY, enemy_spawn_time)
        pygame.time.set_timer(EVENT_ITEM, SPAWN_ITEM_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def run(self):
        music_file = './asset/Level1.mp3' if self.name == 'Level1' else './asset/Level2.mp3'
        if pygame.mixer.get_init():
            try:
                pygame.mixer_music.load(music_file)
                pygame.mixer_music.set_volume(0.2)
                pygame.mixer_music.play(-1)
            except pygame.error:
                print(f"[AVISO] Música {music_file} não pôde ser carregada.")
        clock = pygame.time.Clock()
        running = True
        level_succeeded = False
        survivors = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _quit_game()

                elif event.type == pygame.KEYDOWN:
                    for ent in self.entity_list:
                        if isinstance(ent, AnimatedPlayer):
                            if event.key == PLAYER_KEY_SHOOT[ent.name] and ent.corn_count > 0:
                                shot = ent.shoot()
                                if shot:
                                    self.entity_list.append(shot)

                elif event.type == EVENT_ENEMY:
                    enemy = EntityFactory.get_entity(random.choice(["Enemy1", "Enemy2"]))
                    if enemy:
                        self.entity_list.append(enemy)

                elif event.type == EVENT_ITEM:
                    item = EntityFactory.get_entity("Corn")
                    if item:
                        self.entity_list.append(item)

                elif event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP
                    if self.timeout <= 0:
                        level_succeeded = True
                        running = False

            for ent in self.entity_list:
                if isinstance(ent, AnimatedPlayer):
                    ent.move(pygame.key.get_pressed())
                else:
                    ent.move()

            collisions = EntityMediator.verify_collision(self.entity_list)
            for c in collisions:
                if isinstance(c, TextFeedback):
                    self.entity_list.append(c)

            EntityMediator.verify_health(self.entity_list)
            self.entity_list[:] = [e for e in self.entity_list if e.health > 0]

            survivors = EntityMediator.get_players_from_list(self.entity_list)
            if not survivors:
                running = False

            self.window.fill((0, 0, 0))
            for ent in self.entity_list:
                if isinstance(ent, Background):
                    ent.draw(self.window)
            for ent in self.entity_list:
                if not isinstance(ent, Background):
                    self.window.blit(ent.surf, ent.rect)

            self.show_hud(clock)
            pygame.display.flip()
            clock.tick(60)

        if level_succeeded:
            font = pygame.font.SysFont("Lucida Sans Typewriter", 24)
            self.window.fill((0, 0, 0))
            mensagem_texto = (
                "Parabéns! Você passou para a Fase II!"
                if self.name == 'Level1'
                else "Parabéns! Você completou o jogo!"
            )
            mensagem = font.render(mensagem_texto, True, (255, 255, 0))
            mensagem_rect = mensagem.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 30))
            self.window.blit(mensagem, mensagem_rect)
            dica = font.render("Pressione ENTER para continuar...", True, (255, 255, 255))
            dica_rect = dica.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 10))
            self.window.blit(dica, dica_rect)
            pygame.display.flip()

            esperando = True
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        _quit_game()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        esperando = False

            for ent in self.entity_list:
                if isinstance(ent, AnimatedPlayer):
                    self.player_data[ent.name]['score'] = ent.score
                    self.player_data[ent.name]['kills'] = ent.kills
                    self.player_data[ent.name]['corn_collected'] = ent.corn_collected
            return True
        else:
            credits_screen = Credits(self.window)
            if survivors:
                survivor_player = survivors[0]
                credits_screen.show(
                    kills=survivor_player.kills,
                    corn_collected=survivor_player.corn_collected,
                    player_escaped=True
                )
            else:
                credits_screen.show(player_escaped=False)
            return False

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        surf = font.render(text, True, text_color).convert_alpha()
        rect = surf.get_rect(topleft=text_pos)
        self.window.blit(surf, rect)

    def show_hud(self, clock):
        self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
        self.level_text(14, f'FPS: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
        if PLAYER2 in self.player_data:
            self.level_text(12, 'Controles:', C_WHITE, (WIN_WIDTH - 160, WIN_HEIGHT - 65))
            self.level_text(12, 'P1: atira com [Num 0]', C_WHITE, (WIN_WIDTH - 160, WIN_HEIGHT - 50))
            self.level_text(12, 'P2: atira com [Espaço]', C_WHITE, (WIN_WIDTH - 160, WIN_HEIGHT - 35))

        player_offset = 0
        for ent in self.entity_list:
            if isinstance(ent, AnimatedPlayer):
                nome = self.player_data[ent.name].get('name', ent.name)
                hud = f'{nome} - HP: {ent.health} | Score: {ent.score} | Milhos: {ent.corn_count}'
                self.level_text(14, hud, C_RED, (10, 30 + player_offset * 20))
                player_offset += 1
