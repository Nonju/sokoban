
import pygame
import math
from enum import Enum

from constants import colors
from utils import KeyPressHandler
from states import GameState

LEVEL_DIR = './levels/'


class MovementDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Tile:
    FLOOR = ' '
    WALL = '#'
    BOX = 'o'
    TARGET = '.'
    PLAYER = '@'

class Game:
    def __init__(self, level=''):
        super().__init__()

        self.state = GameState.PLAY

        self.playerPos = (1, 1) # position x / y # TODO(?): Move to player object
        self.targetPos = [] # List of box target positions [(x,y), (x,y)]
        self.level = self.loadLevel(level) # TODO: Check if should store in separate "level" object

        longestSide = max(len(self.level), *map(len, self.level))
        (w, h) = pygame.display.get_surface().get_size()
        self.tileWidth = math.ceil(min([w,h]) / longestSide)

    def loadLevel(self, level=''):
        print('loadLevel - level', level) # Remove
        if not level:
            raise 'Invalid level path' # TODO: Replace with actual error

        filepath = '{}{}.sokoban'.format(LEVEL_DIR, level)
        with open(filepath, 'r') as f:
            level = f.read()

        tileMap = [list(row) for row in level.split('\n') if row]
        for y in range(len(tileMap)):
            for x in range(len(tileMap[y])):
                char = tileMap[y][x]
                if char == Tile.PLAYER:
                    self.playerPos = (x, y)
                elif char == Tile.TARGET:
                    self.targetPos.append((x, y))
        return tileMap

    def getTile(self, pos):
        x, y = pos
        return self.level[y][x]

    def setTile(self, pos, char=' '):
        self.level[pos[1]][pos[0]] = char

    def validateNext(self, direction, current=None):
        ''' Check if positions x / y are a valid destination '''
        next = self.getNext(direction, current)
        nextChar = self.getTile(next)
        if nextChar == Tile.WALL:
            return False
        elif nextChar == Tile.BOX:
            return self.validateNext(direction, next)
        return True

    def getNext(self, direction, current=None):
        if current is None:
            current = self.playerPos

        if direction == MovementDirection.UP:
            return (current[0], current[1]-1)
        elif direction == MovementDirection.DOWN:
            return (current[0], current[1]+1)
        elif direction == MovementDirection.LEFT:
            return (current[0]-1, current[1])
        elif direction == MovementDirection.RIGHT:
            return (current[0]+1, current[1])


    def swapTiles(self, direction, current, dest):
        ''' Recursively move / push tiles '''
        if self.getTile(dest) == Tile.BOX:
            self.swapTiles(direction, dest, self.getNext(direction, dest))

        tmp = self.getTile(dest)
        if not (current in self.targetPos and dest in self.targetPos):
            if current in self.targetPos:
                tmp = Tile.TARGET
            elif dest in self.targetPos:
                tmp = Tile.FLOOR

        self.setTile(dest, self.getTile(current))
        self.setTile(current, tmp)

    def move(self, direction=None):
        if not direction:
            return

        nextPos = self.getNext(direction)
        if not nextPos or not self.validateNext(direction):
            return

        self.swapTiles(direction, self.playerPos, nextPos)
        self.playerPos = nextPos

    def checkWin(self):
        if all(bool(self.getTile(target) == Tile.BOX) for target in self.targetPos):
            self.state = GameState.WIN

    def update(self, events):

        if KeyPressHandler.up():
            self.move(MovementDirection.UP)
        elif KeyPressHandler.down():
            self.move(MovementDirection.DOWN)
        elif KeyPressHandler.left():
            self.move(MovementDirection.LEFT)
        elif KeyPressHandler.right():
            self.move(MovementDirection.RIGHT)

        self.checkWin()


    def drawTile(self, surface, pos):
        tile = self.getTile(pos)

        color = colors.BROWN
        if tile == Tile.FLOOR:
            color = colors.BROWN
        elif tile == Tile.WALL:
            color = colors.WHITE
        elif tile == Tile.BOX:
            color = colors.BLUE
        elif tile == Tile.TARGET:
            color = colors.GREEN
        elif tile == Tile.PLAYER:
            color = colors.RED

        x = pos[0] * self.tileWidth
        y = pos[1] * self.tileWidth
        pygame.draw.rect(surface, color, pygame.Rect((x, y), (self.tileWidth, self.tileWidth)))

    def draw(self, surface):
        if self.state in [GameState.PLAY, GameState.PAUSE]:
            for y in range(len(self.level)):
                for x in range(len(self.level[y])):
                    self.drawTile(surface, (x, y))
        elif self.state == GameState.WIN:
            # TODO: Display victory screen
            pass

