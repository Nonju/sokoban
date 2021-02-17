# -*- coding: utf-8 -*-

import os

LEVEL_DIR = './levels/'

STATE = 'MENU' # MENU, LOAD, GAME, QUIT
MAP_FILE = '' # path to current map file
MAP = [[]] # 2D list (list of rows)

FLOOR = ' '
WALL = '#'
BOX = 'o'
TARGET = '.'
PLAYER = '@'
PLAYER_POS = (1, 1) # position x / y
TARGET_POS = [] # List of box target positions [(x,y), (x,y)]

def clear():
    os.system('clear')

MESSAGE = ''
def setMessage(msg=''):
    global MESSAGE
    MESSAGE = msg

def renderMessage(msg=''):
    if not MESSAGE: return
    print('*' * (len(MESSAGE) + 4))
    print('* {} *'.format(MESSAGE))
    print('*' * (len(MESSAGE) + 4))

class InvalidInput(Exception):
    def __init__(self, message='Ogiltig input'):
        self.message = message
        super().__init__(self.message)

class IllegalMove(Exception):
    def __init__(self, message='Ogiltigt move'):
        self.message = message
        super().__init__(self.message)

################ MENU ###############

def getLevelList():
    files = os.listdir(LEVEL_DIR)
    files = filter(lambda f: f.endswith('.sokoban'), files)
    return [f.split('.sokoban')[0] for f in files]


def renderMenu():
    ''' Re-render menu-screen '''
    global STATE, MAP_FILE
    levels = getLevelList()
    print('----- SOKOBAN: The movie: The Game -----')
    for i in range(len(levels)):
        print('{}. {}'.format(i, levels[i]))
    print('Q - Avsluta')
    selection = input(u'Välj bana: ')

    if selection.lower() == 'q':
        STATE = 'QUIT'
        return

    try:
        selection = int(selection)
    except:
        setMessage(u'Input måste vara en siffra')
        return

    if selection < 0 or selection >= len(levels):
        setMessage(u'Input måste motsvara ett av de givna valen')
        return

    #  loadMap(selection=selection)
    MAP_FILE = '{}{}.sokoban'.format(LEVEL_DIR, levels[selection])
    STATE = 'LOAD'
    setMessage()


################ LOAD ###############

def reset():
    global PLAYER_POS, TARGET_POS
    PLAYER_POS = (0, 0)
    TARGET_POS = []

def loadMap():
    global STATE, MAP, PLAYER_POS, TARGET_POS
    reset()

    level = ''
    with open(MAP_FILE) as f:
        level = f.read()
    MAP = [list(row) for row in level.split('\n') if row]

    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            char = MAP[y][x]
            if char == PLAYER:
                PLAYER_POS = (x, y)
            elif char == TARGET:
                TARGET_POS.append((x, y))

    STATE = 'GAME'


################ GAME ###############

def renderMap():
    print('*' * 15)
    for key, control in CONTROLS.items():
        print(u'* {} - {}'.format(key.upper(), control.get('title', '')))
    print('*' * 15)
    for row in MAP:
        print(''.join(row))
    print() # Spacing

def restart():
    global STATE
    STATE = 'LOAD'

def gotoMenu():
    global STATE
    STATE = 'MENU'

CONTROLS = dict(
    w=dict(title=u'Upp', x=0, y=-1),
    s=dict(title=u'Ned', x=0, y=1),
    a=dict(title=u'Vänster', x=-1, y=0),
    d=dict(title=u'Höger', x=1, y=0),
    r=dict(title=u'Restart', f=restart),
    m=dict(title=u'Gå till meny', f=gotoMenu),
)

def getNext(move, current=None):
    if current is None:
        current = PLAYER_POS
    return (current[0]+move['x'], current[1]+move['y'])

def getTile(pos=(0, 0)):
    return MAP[pos[1]][pos[0]]

def setTile(pos=(0, 0), char=' '):
    MAP[pos[1]][pos[0]] = char

def validateNext(move, current=None):
    ''' Check if positions x / y are a valid destination '''
    next = getNext(move, current)
    nextChar = getTile(next)
    if nextChar == WALL:
        raise IllegalMove()
    elif nextChar == BOX:
        return validateNext(move, next)

def swapTiles(move, current, dest):
    ''' Recursively move / push tiles '''
    if getTile(dest) == BOX:
        swapTiles(move, dest, getNext(move, dest))

    tmp = getTile(dest)
    if not (current in TARGET_POS and dest in TARGET_POS):
        if current in TARGET_POS:
            tmp = TARGET
        elif dest in TARGET_POS:
            tmp = FLOOR

    setTile(dest, getTile(current))
    setTile(current, tmp)

def move():
    ''' Read user input and react '''
    global PLAYER_POS

    move = input(u'Vart vill du gå? ')
    if move.lower() not in CONTROLS.keys():
        raise IllegalMove()
    move = CONTROLS[move]
    if move.get('f'):
        return move['f']()

    current = PLAYER_POS
    next = getNext(move)
    validateNext(move)
    swapTiles(move, current, next)

    PLAYER_POS = next

def checkGameState():
    ''' Checks if game is over '''
    global STATE
    ## TODO
    # Check if player has lost (by checking if a box is stuck in an immovable spot)

    if all(bool(getTile(target) == BOX) for target in TARGET_POS):
        clear()
        setMessage('WOOO - Du vann!')
        renderMessage()
        renderMap()
        input('Klicka på Enter för att komma vidare till menyn!')
        STATE = 'MENU'

def renderGame():
    ''' Re-render game-screen '''
    renderMap()
    try:
        move()
    except (IllegalMove, InvalidInput) as e:
        # Handle all types of excpetions that might occur in `move`
        setMessage(str(e))
        return

    # Check if player has won
    checkGameState()

    # Clear banner message
    setMessage()



def main():
    while True:
        clear()
        renderMessage()
        if STATE == 'MENU':
            renderMenu()
        elif STATE == 'LOAD':
            loadMap()
        elif STATE == 'GAME':
            renderGame()
        elif STATE == 'QUIT':
            break

if __name__ == '__main__':
    main()

