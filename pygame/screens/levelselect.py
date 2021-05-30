
import pygame
import os

from constants import colors
from events import GOTOGAME
from utils import KeyPressHandler

LEVEL_DIR = './levels/'

class LevelSelect:
    def __init__(self):
        super().__init__()

        self.active = 0 # Active level selection
        self.levels = self.listLevels()

        self.headerFont = pygame.font.SysFont(pygame.font.get_default_font(), self.getHeaderFontSize())
        self.headerSurf = self.headerFont.render('Välj nivå!', False, colors.WHITE)

        self.activeFont = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        self.inactiveFont = pygame.font.SysFont(pygame.font.get_default_font(), 30)

    def getHeaderFontSize(self):
        _, h = pygame.display.get_surface().get_size()
        return int(h * 0.15)

    def listLevels(self):
        files = os.listdir(LEVEL_DIR)
        files = filter(lambda f: f.endswith('.sokoban'), files)
        return [f.split('.sokoban')[0] for f in files]

    def startGame(self, level):
        e = pygame.event.Event(GOTOGAME, new=True, level=level)
        pygame.event.post(e)


    def update(self, events):

        # Handle movement
        if KeyPressHandler.up():
            self.active = max(self.active-1, 0)
        elif KeyPressHandler.down():
            self.active = min(self.active+1, len(self.levels)-1)
        elif KeyPressHandler.enter():
            level = self.levels[self.active]
            self.startGame(level)


    def draw(self, surface):
        surface.fill(colors.CORNFLOWERBLUE)

        y = 0

        # Draw header
        surface.blit(self.headerSurf, (0, y))
        y += self.getHeaderFontSize()

        # Draw menu options
        for index, level in enumerate(self.levels):

            # TODO: Use this to calculate center
            #  w, h = pygame.display.get_surface().get_size()
            '''
                ## TODO:
                # Center text using this method

                # draw text
                font = pygame.font.Font(None, 25)
                text = font.render("You win!", True, BLACK)
                text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                screen.blit(text, text_rect)
            '''

            active = index == self.active
            font = self.activeFont if active else self.inactiveFont
            textSurface = font.render(level, False, colors.ACTIVETEXT if active else colors.INACTIVETEXT)
            surface.blit(textSurface, (0, y))
            y += 40 if active else 30

