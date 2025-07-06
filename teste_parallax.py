import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Tamanho da tela
WIN_WIDTH, WIN_HEIGHT = 576, 324
tela = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Teste de Parallax")

# Velocidades para cada camada
velocidades = [1, 2, 3, 4, 5]

# Carrega imagens
camadas = []
for i in range(5):
    imagem = pygame.image.load(f'./asset/bgDay{i}.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (WIN_WIDTH, WIN_HEIGHT))
    # Cria dois blocos para cada imagem
    camada = {
        "img1": imagem.copy(),
        "img2": imagem.copy(),
        "x1": 0,
        "x2": WIN_WIDTH,
        "speed": velocidades[i]
    }
    camadas.append(camada)

clock = pygame.time.Clock()

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Atualiza posição das camadas
    for camada in camadas:
        camada["x1"] -= camada["speed"]
        camada["x2"] -= camada["speed"]

        # Reposiciona se saiu da tela
        if camada["x1"] <= -WIN_WIDTH:
            camada["x1"] = camada["x2"] + WIN_WIDTH
        if camada["x2"] <= -WIN_WIDTH:
            camada["x2"] = camada["x1"] + WIN_WIDTH

    # Desenha camadas
    for camada in camadas:
        tela.blit(camada["img1"], (camada["x1"], 0))
        tela.blit(camada["img2"], (camada["x2"], 0))

    pygame.display.update()
    clock.tick(60)
