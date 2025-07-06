from datetime import datetime
import pygame
from pygame.locals import KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from code.Const import (
    C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE,
    SCORE_TITLE_FONT_SIZE, SCORE_TEXT_FONT_SIZE,
    PLAYER1, WIN_HEIGHT, WIN_WIDTH, C_ORANGE, C_RED
)
from code.DBProxy import DBProxy
from code.utils import _quit_game


class Score:
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
        self.rect = self.surf.get_rect(topleft=(0, 0))

    def save(self, game_mode: str, player_data: dict):
        if pygame.mixer.get_init():
            try:
                pygame.mixer_music.load('./asset/Score.mp3')
                pygame.mixer_music.play(-1)
            except pygame.error:
                print("[AVISO] Erro ao tocar Score.mp3")

        db = DBProxy('DBScore')

        if game_mode == MENU_OPTION[1]:  # 2 JOGADORES
            team_code = ''
            saving_team = True

            while saving_team:
                self.window.blit(self.surf, self.rect)
                self._score_text(SCORE_TITLE_FONT_SIZE, 'YOU WIN!!', C_ORANGE, SCORE_POS['Title'])
                prompt = 'Digite o NOME DA EQUIPE (4 letras):'
                self._score_text(SCORE_TEXT_FONT_SIZE, prompt, C_ORANGE, SCORE_POS['EnterName'])
                self._score_text(SCORE_TEXT_FONT_SIZE, team_code, C_ORANGE, SCORE_POS['Name'])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        _quit_game()
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN and len(team_code) == 4:
                            total_score = sum(p['score'] for p in player_data.values())
                            db.save({
                                'name': 'EQ-' + team_code.upper(),
                                'score': total_score,
                                'date': self._get_formatted_date()
                            })

                            for data in player_data.values():
                                db.save({
                                    'name': data['name'].upper(),
                                    'score': data['score'],
                                    'date': self._get_formatted_date()
                                })

                            self.show()
                            return
                        elif event.key == K_BACKSPACE:
                            team_code = team_code[:-1]
                        elif len(team_code) < 4:
                            team_code += event.unicode.upper()

                pygame.display.flip()

        else:  # 1 JOGADOR
            name_input = ''
            score = player_data[PLAYER1]['score']
            prompt = f'Digite seu apelido (4 letras):'

            while True:
                self.window.blit(self.surf, self.rect)
                self._score_text(SCORE_TITLE_FONT_SIZE, 'YOU WIN!!', C_ORANGE, SCORE_POS['Title'])
                self._score_text(SCORE_TEXT_FONT_SIZE, prompt, C_ORANGE, SCORE_POS['EnterName'])
                self._score_text(SCORE_TEXT_FONT_SIZE, name_input, C_ORANGE, SCORE_POS['Name'])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        _quit_game()
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN and len(name_input) == 4:
                            db.save({
                                'name': name_input.upper(),
                                'score': score,
                                'date': self._get_formatted_date()
                            })
                            self.show()
                            return
                        elif event.key == K_BACKSPACE:
                            name_input = name_input[:-1]
                        elif len(name_input) < 4:
                            name_input += event.unicode.upper()

                pygame.display.flip()

    def show(self):
        if pygame.mixer.get_init():
            try:
                pygame.mixer_music.load('./asset/Score.mp3')
                pygame.mixer_music.play(-1)
            except pygame.error:
                print("[AVISO] Erro ao tocar Score.mp3")

        db = DBProxy('DBScore')
        scores = db.retrieve_all()
        offset = 0
        scroll_speed = 1
        auto_scroll = False if len(scores) > 10 else True
        show_scroll_hint = len(scores) > 10

        running = True
        while running:
            self.window.blit(self.surf, self.rect)
            self._score_text(SCORE_TITLE_FONT_SIZE, 'TOP 10 SCORE', C_RED, (WIN_WIDTH // 2, 40))
            self._score_text(SCORE_TEXT_FONT_SIZE, 'NAME     SCORE        DATE', C_RED, (WIN_WIDTH // 2, 80))

            start_y = 110
            line_height = 25

            for i, (id_, name, score, date) in enumerate(scores):
                y_pos = start_y + i * line_height - offset
                if 100 < y_pos < WIN_HEIGHT - 40:
                    self._score_text(SCORE_TEXT_FONT_SIZE, f'{name:>4}     {score:05d}     {date}', C_RED,
                                     (WIN_WIDTH // 2, y_pos))

            if show_scroll_hint:
                self._score_text(14, "Use ↑ / ↓ para rolar  |  [R] automático", C_RED,
                                 (WIN_WIDTH // 2, WIN_HEIGHT - 25))

            pygame.display.flip()
            pygame.time.delay(50)

            if auto_scroll:
                offset += scroll_speed
                max_offset = max(0, len(scores) * line_height - (WIN_HEIGHT - start_y - 50))
                if offset > max_offset:
                    offset = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        auto_scroll = not auto_scroll
                    elif not auto_scroll:
                        if event.key == pygame.K_DOWN:
                            offset += line_height
                        elif event.key == pygame.K_UP:
                            offset = max(0, offset - line_height)

    def _score_text(self, size: int, text: str, color: tuple, center: tuple):
        font: Font = pygame.font.SysFont("Lucida Sans Typewriter", size)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(center=center)
        self.window.blit(surf, rect)

    @staticmethod
    def _get_formatted_date():
        now = datetime.now()
        return now.strftime("%H:%M - %d/%m/%y")
