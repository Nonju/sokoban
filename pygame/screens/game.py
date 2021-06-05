
import pygame
import math
import os
from enum import Enum

from constants import colors
from utils import KeyPressHandler
from states import GameState

LEVEL_DIR = './levels/'


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Tile:
    FLOOR = ' '
    WALL = '#'
    BOX = 'o'
    TARGET = '.'
    PLAYER = '@'
    SPACER = '-'

class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, pos, direction):
        super().__init__()
        self.image = pygame.transform.rotate(image, 90 * direction.value)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Game:
    def __init__(self, surface, level=''):
        super().__init__()

        self.surface = surface
        self.state = GameState.PLAY

        self.playerPos = (1, 1) # position x / y # TODO(?): Move to player object
        self.targetPos = [] # List of box target positions [(x,y), (x,y)]
        self.level = self.loadLevel(level) # TODO: Check if should store in separate "level" object

        longestSide = max(len(self.level), *map(len, self.level))
        (w, h) = pygame.display.get_surface().get_size()
        self.tileWidth = math.ceil(min([w,h]) / longestSide)
        self.offset = self.tileWidth * 2

        self.wallImage = pygame.image.load(os.path.join(os.path.dirname(__file__), '../assets','wall.png')).convert_alpha()
        self.wallImage = pygame.transform.scale(self.wallImage, (self.tileWidth, self.tileWidth))

        self.imageGroup = pygame.sprite.Group()

    def loadLevel(self, level=''):
        print('loadLevel - level', level) # Remove
        if not level:
            raise 'Invalid level path' # TODO: Replace with actual error

        filepath = '{}{}.sokoban'.format(LEVEL_DIR, level)
        with open(filepath, 'r') as f:
            level = f.read()

        tileMap = [list(row) for row in level.split('\n') if row]
        for y in range(len(tileMap)):
            hitWall = False
            for x in range(len(tileMap[y])):
                char = tileMap[y][x]
                if not hitWall and char == Tile.FLOOR:
                    tileMap[y][x] = ''
                    continue
                elif char == Tile.WALL:
                    hitWall = True

                if char == Tile.PLAYER:
                    self.playerPos = (x, y)
                elif char == Tile.TARGET:
                    self.targetPos.append((x, y))
        return tileMap

    def getTile(self, pos):
        x, y = pos
        try: return self.level[y][x]
        except: return ''

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

        if direction == Direction.UP:
            return (current[0], current[1]-1)
        elif direction == Direction.DOWN:
            return (current[0], current[1]+1)
        elif direction == Direction.LEFT:
            return (current[0]-1, current[1])
        elif direction == Direction.RIGHT:
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
            self.move(Direction.UP)
        elif KeyPressHandler.down():
            self.move(Direction.DOWN)
        elif KeyPressHandler.left():
            self.move(Direction.LEFT)
        elif KeyPressHandler.right():
            self.move(Direction.RIGHT)

        self.checkWin()


    def drawTile(self, pos):
        tile = self.getTile(pos)
        if not tile:
            return
        x, y = pos

        color = colors.DARKBROWN
        if tile == Tile.FLOOR:
            color = colors.BROWN
        #  elif tile == Tile.WALL:
            #  color = colors.WHITE
            #  color = colors.BLACK
        elif tile == Tile.BOX:
            color = colors.BLUE
        elif tile == Tile.TARGET:
            color = colors.GREEN
        elif tile == Tile.PLAYER:
            color = colors.RED

        posX = x * self.tileWidth + self.offset
        posY = y * self.tileWidth + self.offset
        pygame.draw.rect(self.surface, color, pygame.Rect((posX, posY), (self.tileWidth, self.tileWidth)))

        if tile == Tile.WALL:
            #  self.wallImage.get_rect().move((x,y))
            #  self.surface.blit(self.wallImage, (self.tileWidth, self.tileWidth))
            def notWall(pos):
                return self.getTile(pos) not in [Tile.WALL, Tile.SPACER, '']

            if notWall((x, y-1)):
                self.imageGroup.add(MySprite(self.wallImage, (posX, posY), Direction.UP))
            if notWall((x, y+1)):
                self.imageGroup.add(MySprite(self.wallImage, (posX, posY), Direction.DOWN))
            if notWall((x-1, y)):
                self.imageGroup.add(MySprite(self.wallImage, (posX, posY), Direction.RIGHT))
            if notWall((x+1, y)):
                self.imageGroup.add(MySprite(self.wallImage, (posX, posY), Direction.LEFT))


    def draw(self):
        self.surface.fill(colors.DARKBROWN)
        self.imageGroup.empty()

        if self.state in [GameState.PLAY, GameState.PAUSE]:
            for y in range(len(self.level)):
                for x in range(len(self.level[y])):
                    self.drawTile((x, y))
                self.imageGroup.draw(self.surface)
        elif self.state == GameState.WIN:
            # TODO: Display victory screen
            pass

