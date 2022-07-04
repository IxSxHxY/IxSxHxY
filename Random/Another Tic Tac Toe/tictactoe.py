import os

class tictactoe:
    Player = {
        'sign':'X',
        'win': 1
    }
    AI = {
        'sign':'O',
        'win': -1
    }

    def __init__(self, board:list[list]):
        self.board = board
        self.playerTurn = True

    def printBoard(self):
        for i in self.board:
            print(i)

    def checkMoves(self):
        for i in self.board:
            for j in i:
                if j == '': return True
        return False

    def checkWin(self):
        # If AI wins, return -1
        # If Player wins, return 1
        # If draw, return 0
        for i in self.board:
            if i[0] == i[1] and i[1] == i[2] and i[0] == tictactoe.AI['sign']:
                return tictactoe.AI['win']
            if i[0] == i[1] and i[1] == i[2] and i[0] == tictactoe.Player['sign']:
                return tictactoe.Player['win']

        for i in zip(*self.board):
            if i[0] == i[1] and i[1] == i[2] and i[0] == tictactoe.AI['sign']:
                return tictactoe.AI['win']
            if i[0] == i[1] and i[1] == i[2] and i[0] == tictactoe.Player['sign']:
                return tictactoe.Player['win']

        if (
                self.board[0][0] == self.board[1][1] and
                self.board[1][1] == self.board[2][2] and
                self.board[0][0] == tictactoe.AI['sign']
        ): return tictactoe.AI['win']
        if (
                self.board[0][0] == self.board[1][1] and
                self.board[1][1] == self.board[2][2] and
                self.board[0][0] == tictactoe.Player['sign']
        ): return tictactoe.Player['win']

        if (
                self.board[0][2] == self.board[1][1] and
                self.board[1][1] == self.board[2][0] and
                self.board[0][2] == tictactoe.AI['sign']
        ): return tictactoe.AI['win']

        if (
                self.board[0][2] == self.board[1][1] and
                self.board[1][1] == self.board[2][0] and
                self.board[0][2] == tictactoe.Player['sign']
        ): return tictactoe.Player['win']

        return 0

    def makeMove(self, row:int, col:int):
        if self.board[row][col] == '' and self.playerTurn:
            self.board[row][col] = tictactoe.Player['sign']
            self.playerTurn = not self.playerTurn
        elif self.board[row][col] == '' and not self.playerTurn:
            self.board[row][col] = tictactoe.AI['sign']
            self.playerTurn = not self.playerTurn

    def minimax(self, playerTurn):
        score = -1 if playerTurn else 1
        res = self.checkWin()
        if res == tictactoe.Player['win'] or res == tictactoe.AI['win']: return res
        if not self.checkMoves(): return 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = (
                        tictactoe.Player['sign'] if playerTurn else
                        tictactoe.AI['sign']
                    )
                    score = (
                        max(score, self.minimax(not playerTurn)) if playerTurn else
                        min(score, self.minimax(not playerTurn))
                    )
                    self.board[i][j] = ''
        return score

    def bestMove(self):
        move = [-1, -1]
        score = 1
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = tictactoe.AI['sign']
                    temp = self.minimax(True)
                    self.board[i][j] = ''
                    if temp < score:
                        score = temp
                        move = [i, j]
        return move

    def play(self):
        while self.checkMoves():
            x = y = -1
            self.printBoard()
            while self.playerTurn:
                x, y = [int(i) for i in input('Please enter the position(x y): ').split(' ')]
                self.makeMove(x, y)
            res = self.checkWin()
            if res == tictactoe.Player['win']:
                print('Player Win!!!')
            if res == tictactoe.AI['win']:
                print('AI Win!!!')
            if not self.checkMoves(): break
            os.system('cls')
            x, y = self.bestMove()
            self.makeMove(x, y)
            if not self.checkMoves(): break
            res = self.checkWin()
            if res == tictactoe.Player['win']:
                print('Player Win!!!')
                break
            if res == tictactoe.AI['win']:
                print('AI Win!!!')
                break
            if not self.checkMoves() and self.checkWin() == 0:
                print('Draw')
                break
        self.printBoard()