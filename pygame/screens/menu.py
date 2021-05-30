
import pygame

from constants import colors
from events import GOTOLEVELSELECT
from utils import KeyPressHandler

class Menu:
    def __init__(self):
        super().__init__()
        self.newGameEvent = pygame.event.Event(GOTOLEVELSELECT)

        self.active = 0 # Active option
        self.options = [
            dict(title=u'Spela!', click=self.newGame),
            dict(title=u'Highscore', click=self.gotoHighscore),
            dict(title=u'Avsluta', click=self.quit)
        ]

        self.headerFont = pygame.font.SysFont(pygame.font.get_default_font(), self.getHeaderFontSize())
        self.headerSurf = self.headerFont.render('SOKOBAN!', False, colors.WHITE)

        self.activeFont = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        self.inactiveFont = pygame.font.SysFont(pygame.font.get_default_font(), 30)

    def getHeaderFontSize(self):
        _, h = pygame.display.get_surface().get_size()
        return int(h * 0.15)

    def newGame(self):
        pygame.event.post(self.newGameEvent)

    def gotoHighscore(self):
        pass

    def quit(self):
        e = pygame.event.Event(pygame.locals.QUIT)
        pygame.event.post(e)

    def update(self, events):

        # Handle movement
        if KeyPressHandler.up():
            self.active = max(self.active-1, 0)
        elif KeyPressHandler.down():
            self.active = min(self.active+1, len(self.options)-1)
        elif KeyPressHandler.enter():
            self.options[self.active]['click']()

    def draw(self, surface):
        surface.fill(colors.CORNFLOWERBLUE) # Should this be placed in __init__ instead?

        y = 0

        # Draw header
        surface.blit(self.headerSurf, (0, y))
        y += self.getHeaderFontSize()

        # Draw menu options
        for index, option in enumerate(self.options):

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
            textSurface = font.render(option['title'], False, colors.ACTIVETEXT if active else colors.INACTIVETEXT)
            surface.blit(textSurface, (0, y))
            y += 40 if active else 30



