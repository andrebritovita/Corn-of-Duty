import pygame
from code.Entity import Entity


class TextFeedback(Entity):
    def __init__(self, text, position, color=(255, 255, 0)):
        self.text = text
        self.alpha = 255
        self.timer = 30  # duração em frames
        self.dy = 1  # velocidade para cima

        # Cria fonte e renderiza texto ANTES de chamar super().__init__
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 14)
        rendered_surf = self.font.render(text, True, color).convert_alpha()

        # --- INÍCIO DA ALTERAÇÃO ---
        # Chama o construtor da classe base, passando a surface já renderizada
        super().__init__("Feedback", position, health=1, damage=0, score=0, surface=rendered_surf)
        # --- FIM DA ALTERAÇÃO ---

        # Ajusta o rect ao centro da posição, se necessário, pois Entity.__init__ já cria um rect
        self.rect.center = position

        # As propriedades health, damage, score já são definidas no super().__init__
        # com os valores passados (1, 0, 0).
        # self.name = "Feedback" # Já definido em super().__init__
        # self.health = 1
        # self.damage = 0
        # self.score = 0

        # Som opcional (habilite se quiser)
        # self.sound = pygame.mixer.Sound('./asset/feedback.wav')
        # self.sound.play()

    def move(self, *args, **kwargs):
        self.rect.centery -= self.dy
        self.timer -= 1

        # Reduz alpha para efeito de desaparecimento
        self.alpha = max(0, int(255 * (self.timer / 30)))
        self.surf.set_alpha(self.alpha)

        if self.timer <= 0:
            self.health = 0  # Marca para remoção
