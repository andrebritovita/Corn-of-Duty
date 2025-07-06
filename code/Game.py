import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, PLAYER1, PLAYER2
from code.Level import Level
from code.Menu import Menu
from code.Score import Score
from code.utils import _quit_game  # Importa a função centralizada


class Game:
    def __init__(self):
        pygame.init()
        self.audio_enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Não foi possível inicializar o mixer de áudio. O jogo continuará sem áudio.")
            self.audio_enabled = False
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Galinha Desesperada")
        self.score_screen = Score(self.window)
        self.menu_screen = Menu(self.window, self.audio_enabled)

    def run(self):
        while True:
            menu_option = self.menu_screen.run()
            match menu_option:
                case '1 JOGADOR':
                    name1 = self.get_player_name('Player 1')
                    self.run_levels({PLAYER1: {'score': 0, 'kills': 0, 'corn_collected': 0, 'name': name1}},
                                    self.score_screen, mode='1 JOGADOR')
                case '2 JOGADORES':
                    name1 = self.get_player_name('Player 1')
                    name2 = self.get_player_name('Player 2')
                    self.run_levels({
                        PLAYER1: {'score': 0, 'kills': 0, 'corn_collected': 0, 'name': name1},
                        PLAYER2: {'score': 0, 'kills': 0, 'corn_collected': 0, 'name': name2}
                    }, self.score_screen, mode='2 JOGADORES')
                case 'PLACAR':
                    self.score_screen.show()
                case 'CONTROLES':
                    self.show_controls()
                case 'SAIR':
                    _quit_game()

    def run_levels(self, player_data: dict, score_screen, mode: str):
        game_over = False
        for level_name in ['Level1', 'Level2']:
            if game_over:
                break
            level = Level(self.window, level_name, player_data)
            level_succeeded = level.run()
            if not level_succeeded:
                game_over = True
        score_screen.save(mode, player_data)

    def show_controls(self):
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)
        font = pygame.font.SysFont("Lucida Sans Typewriter", 18)
        running = True

        while running:
            self.window.fill((0, 0, 0))
            self.window.blit(font.render("TECLAS DE CONTROLE", True, (255, 255, 0)), (160, 30))

            controles = [
                "Player 1:",
                "- Movimento: Setas ↑ ↓ ← →",
                "- Atirar: Tecla Num 0",
                "- Atacar: Ctrl Direita",
                "",
                "Player 2:",
                "- Movimento: W A S D",
                "- Atirar: Espaço",
                "- Atacar: Ctrl Esquerda",
                "",
                "Pressione ESC para voltar..."
            ]

            for i, linha in enumerate(controles):
                self.window.blit(font.render(linha, True, (255, 255, 255)), (80, 70 + i * 25))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _quit_game()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            pygame.display.flip()

    def get_player_name(self, player_id):
        name = ''
        font = pygame.font.SysFont("Lucida Sans Typewriter", 20)
        clock = pygame.time.Clock()
        while True:
            self.window.fill((0, 0, 0))
            prompt = f'Digite o nome do {player_id} (máx 8 letras):'
            text = font.render(prompt, True, (255, 255, 255))
            prompt_rect = text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 30))
            self.window.blit(text, prompt_rect)

            name_surface = font.render(name, True, (255, 255, 0))
            name_rect = name_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 10))
            self.window.blit(name_surface, name_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0:
                        return name[:8]
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 8:
                        name += event.unicode.upper()

            pygame.display.flip()
            clock.tick(30)
