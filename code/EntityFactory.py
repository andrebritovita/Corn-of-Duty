from code.AnimatedEnemy import AnimatedEnemy
from code.AnimatedPlayer import AnimatedPlayer
from code.Background import Background
from code.DeadEnemy import DeadEnemy
from code.DeadPlayer import DeadPlayer
from code.Item import Item
from code.PlayerShot import PlayerShot
from code.TextFeedback import TextFeedback
from code.Const import WIN_WIDTH, WIN_HEIGHT, BG_NIGHT, BG_DAY, PLAYER1, PLAYER2, ENTITY_SPEED


class EntityFactory:
    __entity_map = {
        # Jogadores
        PLAYER1: lambda: AnimatedPlayer(PLAYER1, (10, WIN_HEIGHT // 2 - 30), frames_count=4),
        PLAYER2: lambda: AnimatedPlayer(PLAYER2, (10, WIN_HEIGHT // 2 + 30), frames_count=4),

        # Inimigos
        'Enemy1': lambda: AnimatedEnemy('Enemy1'),
        'Enemy2': lambda: AnimatedEnemy('Enemy2'),

        # Itens
        'Corn': lambda: Item('Corn', sprite_name='Player1Shot'),  # Usando Player1Shot como sprite para o milho

        # Fundos
        'Level1Bg': lambda: [Background(f'{BG_DAY}{i}', (0, 0), ENTITY_SPEED[f'{BG_DAY}{i}']) for i in range(5)],
        'Level2Bg': lambda: [Background(f'{BG_NIGHT}{i}', (0, 0), ENTITY_SPEED[f'{BG_NIGHT}{i}']) for i in range(7)],

        # Entidades mortas
        'EnemyDead1': lambda: DeadEnemy('EnemyDead1', (0, 0)),
        'EnemyDead2': lambda: DeadEnemy('EnemyDead2', (0, 0)),
        'Player1Die': lambda: DeadPlayer((0, 0), player_name='Player1'),
        'Player2Die': lambda: DeadPlayer((0, 0), player_name='Player2'),

        # Feedback de texto (não precisa de sprite de arquivo)
        'TextFeedback': lambda: TextFeedback(text='', position=(0, 0))
    }

    @staticmethod
    def get_entity(name: str):
        constructor = EntityFactory.__entity_map.get(name)
        if constructor:
            return constructor()
        return None
