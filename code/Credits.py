import pygame

from code.Const import WIN_WIDTH, C_WHITE, CREDITS_TEXT_START_Y, CREDITS_TEXT_SPACING
from code.utils import _quit_game  # Importa a função centralizada


class Credits:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 20)

    def show(self, kills: int = 0, corn_collected: int = 0, player_escaped: bool = False):
        self.window.fill((0, 0, 0))
        messages = [
            "🎉 Parabéns, você escapou com vida!" if player_escaped else "😭 Fim de Jogo!",
            "",
            f"🐔 Inimigos abatidos: {kills}",
            f"🌽 Milhos coletados: {corn_collected}",
            "",
            "Pressione ESC para voltar ao Menu.",
            "Pressione Q para Sair."
        ]

        for i, msg in enumerate(messages):
            text_surf = self.font.render(msg, True, C_WHITE)
            rect = text_surf.get_rect(center=(WIN_WIDTH // 2, CREDITS_TEXT_START_Y + i * CREDITS_TEXT_SPACING))
            self.window.blit(text_surf, rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_q:
                        _quit_game()
