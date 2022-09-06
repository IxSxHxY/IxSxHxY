from tictactoe import *

if __name__ == '__main__':
    board = [['','',''] for _ in range(3)]
    ttt = tictactoe(board)
    ttt.play()