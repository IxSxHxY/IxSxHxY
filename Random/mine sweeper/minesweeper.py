import random as rand
import pygame
import sys, os
from tkinter import *
from tkinter import messagebox


WIDTH, HEIGHT = 10, 10
# Width = number of tiles per row = j in second for  loop
# Height = number of row = i in first for loop

TILE_SIZE = 40 # Here tile_h = tile_w for tile size

TILE_OFFSET = (100, 50) # widthOff, heightOff

IMAGES = {
    'tile': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'tile.png')), (TILE_SIZE, TILE_SIZE)),
    'bomb': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bomb.png')), (TILE_SIZE - 10, TILE_SIZE - 10)),
    'flag': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'flag.png')), (TILE_SIZE - 10, TILE_SIZE - 10))
}
# We use transform.scale(pygame.image.load(), (width, height)) to change the scale of the images

SCREEN_SIZE = (2 * TILE_OFFSET[0] + WIDTH * TILE_SIZE, 2 * TILE_OFFSET[1] + HEIGHT * TILE_SIZE)
# 2*TILE_OFFSET to center the tiles
# Example: O=offset, T=tiles
# OOO     OOOO
# OTT -\  OTTO
# OTT -/  OTTO
#         OOOO

pygame.font.init() # initialize font

FONT = pygame.font.Font(os.path.join('assets', 'mine-sweeper.ttf'), TILE_SIZE // 2)
# Font(file, fontsize)

DIR = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
    [1, 1],
    [-1, -1],
    [-1, 1],
    [1, -1]
] # To check 8 directions from a tile

MAX_BOMBS = (HEIGHT * WIDTH) // 6
FOUND_BOMBS = 0
USED_FLAGS = 0

TILES = None
# To store the number of bombs around and the position of bombs

TILE_STATUS = None
# To store the status of all the tiles, whether it is opened, closed, or labelled as bomb

TILE_COND = {
    'flag': -1,
    'opened': 1,
    'closed': 0
}

GAME_COND = {
    'win' : 1,
    'lose': -1,
    'playing': 0,
    'stop': -2
}

GAME_STAT = GAME_COND['playing']


SCREEN = pygame.display.set_mode(SCREEN_SIZE)
# set_mode((width, height))


BACKGROUND = (255, 255, 122)

"""
This feature is currently not in use because it is broke the game
def user_input():
    global WIDTH, HEIGHT, TILE_SIZE, MAX_BOMBS, SCREEN_SIZE
    WIDTH = int(input('Please input the width:\nwidth = '))
    while WIDTH <= 0:
        print("WIDTH shouldn't be less or equal to 0\n")
        WIDTH = int(input('Please input the width:\nwidth = '))

    HEIGHT = int(input('Please input the height:\nheight = '))
    while HEIGHT <= 0:
        print("HEIGHT shouldn't be less or equal to 0\n")
        HEIGHT = int(input('Please input the height:\nheight = '))

    TILE_SIZE = int(input('Please input the size for a tile:\nsize = '))
    while TILE_SIZE <= 0:
        print("Tile size shouldn't be less or equal to 0\n")
        TILE_SIZE = int(input('Please input the size for a tile:\nsize = '))
    MAX_BOMBS = (HEIGHT * WIDTH) // 5
    SCREEN_SIZE = (2 * TILE_OFFSET[0] + WIDTH * TILE_SIZE, 2 * TILE_OFFSET[1] + HEIGHT * TILE_SIZE)
    IMAGES = {
        'tile': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'tile.png')), (TILE_SIZE, TILE_SIZE)),
        'bomb': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bomb.png')),
                                       (TILE_SIZE - 10, TILE_SIZE - 10)),
        'flag': pygame.transform.scale(pygame.image.load(os.path.join('assets', 'flag.png')),
                                       (TILE_SIZE - 10, TILE_SIZE - 10))
    }
"""


def generate_tiles():
    # Generate the tiles
    global HEIGHT, WIDTH, MAX_BOMBS
    tiles = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    bombs_pos = set()
    for _ in range(MAX_BOMBS):
        pos = (rand.randint(0, HEIGHT - 1), rand.randint(0, WIDTH - 1))
        while pos in bombs_pos:
            pos = (rand.randint(0, HEIGHT - 1), rand.randint(0, WIDTH - 1))
            # randint(0, n) generated a number in the range of [0, n]
        tiles[pos[0]][pos[1]] = -1
        # -1 = bomb
        bombs_pos.add(pos)

    def check_bomb(x, y):
        bomb = 0
        for i, j in DIR:
            dx = x + i
            dy = y + j
            if dx < 0 or dy < 0 or dx >= WIDTH or dy >= HEIGHT: continue
            if tiles[dy][dx] == -1: bomb += 1
        return bomb

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if tiles[i][j] == -1: continue
            tiles[i][j] = check_bomb(j, i)
            
    return tiles

def drawMap():
    # This function draw the tiles
    global TILE_OFFSET, TILES, TILE_SIZE, SCREEN
    textSurf = FONT.render('Press r to restart', True, (255, 0, 0))
    # To put text, you need to render an image so that
    # it can be put on the screen
    # font.render(text, antialias, color)
    textSurf.set_alpha(127)
    # Make the background transparent
    SCREEN.blit(textSurf, (0, 0))
    # We use screen.blit(image, (w, h)) to put the image here

    for i, row in enumerate(TILES):
        for j, tile in enumerate(row):
            # j is for row, which is width
            # i is for column, which is height
            SCREEN.blit(IMAGES['tile'],
                        (TILE_OFFSET[0] + j * TILE_SIZE, TILE_OFFSET[1] + i * TILE_SIZE)
                        )
            # If you cannot understand the position, see the examples below
            # To generate the first row
            # (wOff + 0 * tile_w, hOff + 0 * tile_h) = (wOff, hOff)
            # (wOff + 1 * tile_w, hOff + 0 * tile_h) = (wOff + tile_w, hOff)
            # (wOff + 1 * tile_w, hOff + 0 * tile_h) = (wOff + 2 * tile_w, hOff)
            # ...


def restart():
    # This function initialize all the variables and restart the game
    global TILES, TILE_STATUS, GAME_STAT, GAME_COND, FOUND_BOMBS, USED_FLAGS
    TILES = generate_tiles()
    TILE_STATUS = [[TILE_COND['closed'] for _ in range(WIDTH)] for _ in range(HEIGHT)]
    GAME_STAT = GAME_COND['playing']
    FOUND_BOMBS = 0
    USED_FLAGS = 0

def show_all():
    global SCREEN, HEIGHT, WIDTH, TILE_SIZE, TILE_OFFSET, FONT, SCREEN_SIZE, GAME_STAT
    SCREEN.fill(BACKGROUND)
    drawMap()

    for x in range(HEIGHT):
        for y in range(WIDTH):
            if TILES[x][y] == -1:
                # If this tile hidden a bomb
                SCREEN.blit(IMAGES['bomb'],
                            (TILE_OFFSET[0] + y * TILE_SIZE + TILE_SIZE // 5,
                             TILE_OFFSET[1] + x * TILE_SIZE + TILE_SIZE // 7)
                            )
                # The position here is same as drawing the tile
                continue
            text_surf = FONT.render(f'{TILES[x][y]}', True, (0, 0, 0))
            # Since TILES stored the number of bombs around, just use it
            text_surf.set_alpha(127)
            SCREEN.blit(text_surf,
                        (TILE_OFFSET[0] + y * TILE_SIZE + TILE_SIZE // 4 + 1,
                         TILE_OFFSET[1] + x * TILE_SIZE + TILE_SIZE // 5)
                        )


    pygame.display.flip()
    # We use this function to update the screen

    if GAME_STAT == GAME_COND['win']:
        Tk().wm_withdraw()
        messagebox.showinfo('', 'Congratulation!!!! You win')
        GAME_STAT = GAME_COND['stop']


    if GAME_STAT == GAME_COND['lose']:
        Tk().wm_withdraw()
        messagebox.showinfo('', 'Congratulation!!!! You lose')
        GAME_STAT = GAME_COND['stop']
    # Here we use tkinter popup screen to show the message



def draw_game():
    global SCREEN, TILE_STATUS, TILES, FONT, IMAGES, TILE_SIZE, TILE_OFFSET
    SCREEN.fill(BACKGROUND)
    drawMap()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if TILE_STATUS[i][j] == TILE_COND['opened'] and TILES[i][j] == -1:
                # If the one we clicked is bomb
                SCREEN.blit(IMAGES['bomb'],
                            (TILE_OFFSET[0] + j * TILE_SIZE + TILE_SIZE // 5, TILE_OFFSET[1] + i * TILE_SIZE + TILE_SIZE // 7)
                            )
                continue
            if TILE_STATUS[i][j] == TILE_COND['flag']:
                # This one draw the flag
                SCREEN.blit(IMAGES['flag'],
                            (TILE_OFFSET[0] + j * TILE_SIZE + TILE_SIZE // 5,
                            TILE_OFFSET[1] + i * TILE_SIZE + TILE_SIZE // 7)
                )
                continue
            if TILE_STATUS[i][j] == TILE_COND['opened']:
                # If the one we clicked is not bomb, just normal tile
                text_surf = FONT.render(f'{TILES[i][j]}', True, (0, 0, 0))
                text_surf.set_alpha(127)
                SCREEN.blit(text_surf,
                            (TILE_OFFSET[0] + j * TILE_SIZE + TILE_SIZE // 4 + 1, TILE_OFFSET[1] + i * TILE_SIZE + TILE_SIZE // 5)
                            )
    pygame.display.flip()

def open_tile(pos):
    global GAME_STAT, TILE_OFFSET, TILE_SIZE, TILES, TILE_STATUS, GAME_COND
    i = (pos[1] - TILE_OFFSET[1]) // TILE_SIZE # i = Height for array index
    j = (pos[0] - TILE_OFFSET[0]) // TILE_SIZE # j = width for array index
    # print(pos)
    # print(i, j)
    if (
            i < 0 or j < 0
            or i >= len(TILES) or j >= len(TILES[0]) or
            TILE_STATUS[i][j] != TILE_COND['closed'] # We can only open a closed tile
    ): return

    # print(TILES[i][j], i, j)
    if TILES[i][j] == -1:
        # If we clicked a bomb, we lose
        GAME_STAT = GAME_COND['lose']
        return
    def bfs(i, j):
        # This function is to open the tiles around the one we clicked
        queue = []
        queue.append((i, j))
        TILE_STATUS[i][j] = TILE_COND['opened']
        if TILES[i][j] != 0: return
        # We will only open the tiles around if the tile
        # we clicked is 0, same goes with the tiles around
        # which are also 0.

        while queue:
            ti, tj = queue.pop(0)
            if TILES[ti][tj] != 0: continue
            # We will not proceed anymore given the reason mentioned above.

            for x, y in DIR:
                di = ti+x
                dj = tj+y
                if (
                        di < 0 or dj < 0 or
                        di >= len(TILES) or dj >= len(TILES[0]) or
                        TILE_STATUS[di][dj] != TILE_COND['closed'] or
                        TILES[di][dj] == -1 # We are not going to open a bomb
                ): continue
                TILE_STATUS[di][dj] = TILE_COND['opened']
                queue.append((di, dj))
    bfs(i, j)

def place_flag(pos):
    global GAME_STAT, TILE_OFFSET, TILE_SIZE, TILES, TILE_STATUS, FOUND_BOMBS, USED_FLAGS, MAX_BOMBS
    i = (pos[1] - TILE_OFFSET[1]) // TILE_SIZE # i = Height for array index
    j = (pos[0] - TILE_OFFSET[0]) // TILE_SIZE # j = width for array index

    if (
            i < 0 or j < 0 or
            i >= len(TILES) or j >= len(TILES[0]) or
            TILE_STATUS[i][j] == TILE_COND['opened'] # We won't label a opened tile
    ): return

    # print('place_flag', MAX_BOMBS, USED_FLAGS, FOUND_BOMBS)
    if TILE_STATUS[i][j] == TILE_COND['flag']:
        # If the tile was labelled as bomb before, then we undo it
        TILE_STATUS[i][j] = TILE_COND['closed']
        USED_FLAGS -= 1
        if TILES[i][j] == -1:
            # If that flag is correct, then undo it will
            # decrease the number of bombs founded correctly
            FOUND_BOMBS -= 1
    else:
        if USED_FLAGS >= MAX_BOMBS: return
        USED_FLAGS += 1
        TILE_STATUS[i][j] = TILE_COND['flag']
        if TILES[i][j] == -1:
            FOUND_BOMBS += 1

    if FOUND_BOMBS == MAX_BOMBS:
        GAME_STAT = GAME_COND['win']


if __name__ == "__main__":
    #user_input()
    pygame.init()
    TILES = generate_tiles()
    TILE_STATUS = [[TILE_COND['closed'] for _ in range(WIDTH)] for _ in range(HEIGHT)]
    # for i in TILES:
    #     print(i)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif GAME_STAT == GAME_COND['playing'] and event.type == pygame.MOUSEBUTTONDOWN:
                # We only allowed the player to click when the game is playing
                # print("User pressed a mouse button")
                # print(event.button)
                if event.button == 1: # Left click
                    open_tile(pygame.mouse.get_pos())
                elif event.button == 3: # Right click
                    place_flag(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()

        if GAME_STAT == GAME_COND['win'] or GAME_STAT == GAME_COND['lose'] or GAME_STAT == GAME_COND['stop']:
            show_all() # If we win, lose or stop after the popup
        else:
            draw_game() # Otherwise, continue the game