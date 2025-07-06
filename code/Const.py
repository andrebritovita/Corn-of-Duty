import pygame

# ------------------- Cores -------------------
C_WHITE = (255, 255, 255)
C_YELLOW = (255, 255, 128)
C_GREEN = (0, 255, 0)
C_RED = (255, 0, 0)
C_ORANGE = (255, 128, 0)
C_CYAN = (0, 255, 255)

# ------------------- Eventos customizados -------------------
EVENT_ENEMY = pygame.USEREVENT + 1
EVENT_ITEM = pygame.USEREVENT + 2
EVENT_TIMEOUT = pygame.USEREVENT + 3

# ------------------- Identificadores -------------------
BG_DAY = 'bgDay'
BG_NIGHT = 'bgNight'
PLAYER1 = 'Player1'
PLAYER2 = 'Player2'
SHOT = 'PlayerShot'

# ------------------- Teclas de controle -------------------
PLAYER_KEY_UP = {PLAYER1: pygame.K_UP, PLAYER2: pygame.K_w}
PLAYER_KEY_DOWN = {PLAYER1: pygame.K_DOWN, PLAYER2: pygame.K_s}
PLAYER_KEY_LEFT = {PLAYER1: pygame.K_LEFT, PLAYER2: pygame.K_a}
PLAYER_KEY_RIGHT = {PLAYER1: pygame.K_RIGHT, PLAYER2: pygame.K_d}
PLAYER_KEY_SHOOT = {PLAYER1: pygame.K_KP0, PLAYER2: pygame.K_SPACE}
PLAYER_KEY_ATTACK = {PLAYER1: pygame.K_RCTRL, PLAYER2: pygame.K_LCTRL}

# ------------------- Velocidade -------------------
ENTITY_SPEED = {
    **{f'{BG_DAY}{i}': i + 1 for i in range(5)},  # bgDay0: 1, bgDay1: 2, bgDay2: 3, bgDay3: 4, bgDay4: 5
    **{f'{BG_NIGHT}{i}': i + 1 for i in range(7)},  # bgNight0: 1, bgNight1: 2, ..., bgNight6: 7
    PLAYER1: 2,
    PLAYER2: 2,
    SHOT: 6,
    'Enemy1': 2,
    'Enemy2': 3,
}

# ------------------- Vida -------------------
ENTITY_HEALTH = {
    **{f'{BG_DAY}{i}': 999 for i in range(5)},
    **{f'{BG_NIGHT}{i}': 999 for i in range(7)},
    PLAYER1: 100,
    PLAYER2: 100,
    'ChickenDie': 1,
    SHOT: 1,
    'Enemy1': 50,
    'Enemy2': 50,
    'EnemyHurt1': 1,
    'EnemyHurt2': 1,
    'EnemyDead1': 1,
    'EnemyDead2': 1,
}

# ------------------- Dano -------------------
ENTITY_DAMAGE = {
    **{f'{BG_DAY}{i}': 0 for i in range(5)},
    **{f'{BG_NIGHT}{i}': 0 for i in range(7)},
    PLAYER1: 50,
    PLAYER2: 50,
    'ChickenDie': 0,
    SHOT: 50,
    'Enemy1': 15,
    'Enemy2': 25,
    'EnemyHurt1': 0,
    'EnemyHurt2': 0,
    'EnemyDead1': 0,
    'EnemyDead2': 0,
}

# ------------------- Pontuação -------------------
ENTITY_SCORE = {
    **{f'{BG_DAY}{i}': 0 for i in range(5)},
    **{f'{BG_NIGHT}{i}': 0 for i in range(7)},
    PLAYER1: 0,
    PLAYER2: 0,
    'ChickenDie': 0,
    SHOT: 0,
    'Enemy1': 100,
    'Enemy2': 150,
    'EnemyHurt1': 0,
    'EnemyHurt2': 0,
    'EnemyDead1': 0,
    'EnemyDead2': 0,
    'Corn': 10,
}

# ------------------- Delay de tiro -------------------
ENTITY_SHOT_DELAY = {
    PLAYER1: 20,
    PLAYER2: 15
}

# ------------------- Menu -------------------
MENU_OPTION = (
    '1 JOGADOR',
    '2 JOGADORES',
    'PLACAR',
    'CONTROLES',
    'SAIR'
)

# ------------------- Timers -------------------
SPAWN_ENEMY_TIME = 3000
SPAWN_ITEM_TIME = 5000
TIMEOUT_STEP = 100
TIMEOUT_LEVEL = 40000

# ------------------- Tamanho da janela -------------------
WIN_WIDTH = 576
WIN_HEIGHT = 324

# ------------------- Placar -------------------
SCORE_POS = {
    'Title': (WIN_WIDTH // 2, 50),
    'EnterName': (WIN_WIDTH // 2, 100),
    'Name': (WIN_WIDTH // 2, 130),
    'Label': (WIN_WIDTH // 2, 160),

    # Espaçamento vertical maior para os registros
    **{i: (WIN_WIDTH // 2, 190 + i * 30) for i in range(10)}
}

# ------------------- Novas Constantes -------------------
FRAME_DELAY = 5
HURT_SPRITE_DURATION_FRAMES = 10
ATTACK_SPRITE_DURATION_FRAMES = 10
DEAD_ENTITY_TIMER = 15
DEAD_PLAYER_TIMER = 30
FEEDBACK_DURATION_FRAMES = 30
FEEDBACK_MOVE_SPEED = 1
CREDITS_TEXT_START_Y = 80
CREDITS_TEXT_SPACING = 30
SCORE_TITLE_FONT_SIZE = 48
SCORE_TEXT_FONT_SIZE = 20
INVINCIBILITY_DURATION_FRAMES = 60
ATTACK_MOVE_FACTOR = 2
