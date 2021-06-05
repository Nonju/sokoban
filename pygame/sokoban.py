import pygame
from pygame.locals import *

import sys

from constants import colors
from events import *
from states import ScreenState
from screens import menu, levelselect, game
from utils import KeyPressHandler

pygame.init()

FPS = 30
FramePerSec = pygame.time.Clock()


# Screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(colors.BROWN)
pygame.display.set_caption('Sokoban')


def main():
    currentState = ScreenState.MENU
    Menu = menu.Menu(DISPLAYSURF)
    LevelSelect = None
    Game = None

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == GOTOLEVELSELECT:
                LevelSelect = levelselect.LevelSelect(DISPLAYSURF)
                currentState = ScreenState.LEVELSELECT
            elif event.type == GOTOGAME:
                if bool(event.new):
                    Game = game.Game(DISPLAYSURF, level=event.level)
                currentState = ScreenState.GAME

        if currentState == ScreenState.MENU:
            Menu.update(events)
            Menu.draw()
        elif currentState == ScreenState.LEVELSELECT:
            LevelSelect.update(events)
            LevelSelect.draw()
        elif currentState == ScreenState.GAME:
            Game.update(events)
            Game.draw()
        else: break

        KeyPressHandler.update(events)

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()

