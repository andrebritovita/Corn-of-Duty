![alt text](https://github.com/andrebritovita/PanickedChicken/blob/master/asset/readme.png?raw=true "Panicked Chicken")![alt text](https://github.com/andrebritovita/Corn-of-Duty/blob/master/asset/Player1Shot.png?raw=true "Panicked Chicken")Corn of Duty ![alt text](https://github.com/andrebritovita/Corn-of-Duty/blob/master/asset/Player1Shot.png?raw=true "Panicked Chicken")![alt text](https://github.com/andrebritovita/PanickedChicken/blob/master/asset/readme.png?raw=true "Panicked Chicken")
===============

Um mini jogo em Python onde você controla uma galinha corajosa que enfrenta uma invasão de pombos assassinos, mas aqui o único fuzil é uma espiga na mão de uma galinha braba.

## 🐔 Sobre o Jogo
Coletando milhos, atirando ou atacando com o próprio corpo, o objetivo é sobreviver até o tempo acabar e passar de fase.

## 🎮 Como Jogar
- Escolha 1 Jogador ou 2 Jogadores no menu principal.
- Use os controles abaixo para mover, atacar e atirar.
- Colete milhos para manter seu arsenal e ganhar pontos.
- Sobreviva até o tempo acabar para avançar para o próximo nível.
- Se perder todo o HEALTH, é Game Over!

## ⌨️ Controles
### Player 1
- Movimento: `Setas ↑ ↓ ← →`
- Atirar milho: `Tecla Num 0`
- Ataque corpo a corpo: `Ctrl Direita`

### Player 2
- Movimento: `W A S D`
- Atirar milho: `Espaço`
- Ataque corpo a corpo: `Ctrl Esquerda`

### Na tela de placar
- `↑ / ↓`: rolar placar (se houver mais de 10 entradas)
- `R`: alternar rolagem automática/manual
- `Esc`: voltar ao menu

## 🛠️ Como Executar
### 1. Requisitos
- Python 3.9+
- Pygame instalado:
```bash
pip install pygame
```
### 2. Rodar jogo
```bash
python main.py
```

## 📁 Estrutura do Projeto
| Tipo                    | Arquivo/Classe                                          |
| ----------------------- | ------------------------------------------------------- |
| Entrada do jogo         | `main.py`, `Game.py`                                    |
| Menu e navegação        | `Menu.py`, `Score.py`                                   |
| Mecânica do jogo        | `Level.py`, `EntityMediator.py`                         |
| Entidades animadas      | `AnimatedPlayer.py`, `AnimatedEnemy.py`                 |
| Entidades estáticas     | `Entity.py`, `Item.py`, `DeadEnemy.py`, `DeadPlayer.py` |
| Fábrica de entidades    | `EntityFactory.py`                                      |
| Sons, imagens e sprites | `asset/` (imagens `.png`, sons `.mp3` e `.wav`)         |
| Banco de dados local    | `DBProxy.py` (SQLite3)                                  |
| Feedback visual         | `TextFeedback.py`                                       |
| Constantes e teclas     | `Const.py`                                              |
| Utilidades              | `utils.py`                                              |

## 🖼️ Recursos Visuais e Áudio
Todos os assets estão na pasta asset/:
| Tipo      | Exemplo de Arquivos                                              |
| --------- | ---------------------------------------------------------------- |
| Fundos    | `BgDayX.png`, `BgNightX.png`                                     |
| Jogadores | `Player1.png`, `Player1Attack.png`, etc.                         |
| Inimigos  | `Enemy1.png`, `EnemyHurt1.png`, `EnemyDead1.png`                 |
| Sons      | `shoot.wav`, `pickup.mp3`, `Level1.mp3`, `Menu.mp3`, `Score.mp3` |

## 🧠 Funcionalidades
| Funcionalidade                           | Status |
| ---------------------------------------- | ------ |
| Modo 1 jogador e 2 jogadores             | ✅      |
| Sprites e controles distintos por player | ✅      |
| Coleta de milho com som                  | ✅      |
| Ataque corpo a corpo com animação        | ✅      |
| Tiro de milho com sprite animado         | ✅      |
| HEALTH gradual com feedback              | ✅      |
| Sistema de score com banco SQLite        | ✅      |
| Placar com rolagem manual e automática   | ✅      |
| Música ambiente em menu, fase e score    | ✅      |
| Efeito Parallax nos fundos               | ✅      |

## 📌 Créditos e Licença
Esse jogo foi desenvolvido como projeto educacional e pode ser adaptado e compartilhado livremente com os devidos créditos.
Feito com amor, milho e Python 🐔💛🐍






