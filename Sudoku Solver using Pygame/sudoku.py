import pygame
import os

class DrawInformation:

    WHITE = (255, 255, 255)

    BLACK = (0, 0, 0)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __init__(self, width: int, height: int, board: list[list]) -> None:
        self.board = board
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption('Sudoku Solver')
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), min(self.width, self.height)//10)


    def update(self, width, height: int) -> None:
        self.width = width
        self.height = height
        self.font = pygame.font.Font(pygame.font.get_default_font(), min(self.width, self.height)//10)




def draw(drawInfo: DrawInformation):
    pygame.display.update()


def draw_board(drawInfo: DrawInformation):
    w = drawInfo.width // 9
    h = drawInfo.height // 9
    drawInfo.surface.fill(drawInfo.WHITE)
    for i in range(9):
        if i % 3 == 0:
            pygame.draw.line(drawInfo.surface, drawInfo.BLACK, (i * w, 0), (i * w, drawInfo.height), 3)
        else:
            pygame.draw.line(drawInfo.surface, drawInfo.BLACK, (i * w, 0), (i * w, drawInfo.height))
    for i in range(9):
        if i % 3 == 0:
            pygame.draw.line(drawInfo.surface, drawInfo.BLACK, (0, i * h), (drawInfo.width, i * h), 3)
        else:
            pygame.draw.line(drawInfo.surface, drawInfo.BLACK, (0, i * h), (drawInfo.width, i * h))
    board = drawInfo.board
    font = drawInfo.font
    fontSize = font.size("1")
    for i in range(9):
        for j in range(9):
            textSurf = font.render(f"{board[i][j]}", False, drawInfo.BLACK)
            textSurf.set_alpha(127)
            drawInfo.surface.blit(textSurf, (j*w+w//2-fontSize[0]//2, i*h+h//2-fontSize[1]//2))
    draw(drawInfo)


def start(drawInfo: DrawInformation):
    solver(drawInfo, 0, 0)
    print_board(drawInfo)

def print_board(drawInfo: DrawInformation) -> None:
    for i in range(9):
        for j in range(9):
            print(drawInfo.board[i][j], end=' ')
        print('')

def check_valid(drawInfo: DrawInformation, row: int, col: int, num: int) -> bool:
    for i in range(9):
        if drawInfo.board[row][i] == num or drawInfo.board[i][col] == num: return False

    startR = row - row % 3
    startC = col - col % 3
    for i in range(3):
        for j in range(3):
            if drawInfo.board[startR + i][startC + j] == num: return False
    return True


def solver(drawInfo: DrawInformation, row: int, col: int) -> bool:
    if row == 8 and col == 9: return True
    if col == 9:
        row += 1
        col = 0
    if drawInfo.board[row][col] != 0:
        return solver(drawInfo, row, col + 1)
    for i in range(1, 10):
        if check_valid(drawInfo, row, col, i):
            drawInfo.board[row][col] = i
            # pygame.time.delay(10)
            draw_board(drawInfo)
            if solver(drawInfo, row, col + 1):
                return True
            drawInfo.board[row][col] = 0
    return False


def get_board():
    os.system('cls')
    print('Please enter your board row by row')
    print('Example: ')
    print('0 0 0 0 0 0 0 0 0')
    print('...')
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    for i in range(9):
        inp = input().split(" ")
        for j in range(len(inp)):
            board[i][j] = int(inp[j])
    return board

def main():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    board = [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ]
    board = get_board()
    drawInfo = DrawInformation(300, 300, list(board))

    pygame.init()
    run = True
    while run:
        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                size = drawInfo.surface.get_size()
                drawInfo.update(size[0], size[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    drawInfo.board = get_board()
                if event.key == pygame.K_s:
                    start(drawInfo)
        draw_board(drawInfo)

if __name__ == "__main__":
    main()

