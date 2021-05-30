from enum import Enum

class ScreenState(Enum):
    MENU = 0
    LEVELSELECT = 1
    GAME = 2
    HIGHSCORE = 3


class GameState(Enum):
    PLAY = 0
    PAUSE = 1
    WIN = 2
    LOSS = 3

