import os
class tictactoe():
    def __init__(self):
        self.board = [
            ['_','_','_'],
            ['_','_','_'],
            ['_','_','_']
        ]
        self.player, self.opponent = 'O', 'X'
        self.play()

    # checkWinner checks is there a winner or not
    def checkWinner(self):
        for i in self.board:
            if i[0] == i[1] and i[1] == i[2]:
                if i[0] == self.player:
                    # -10 cause this maximizer is for opponent
                    return -10
                elif i[0] == self.opponent:
                    # 10 cause this maximizer is for opponent
                    return 10
        for i in zip(*self.board):
            if i[0] == i[1] and i[1] == i[2]:
                if i[0] == self.player:
                    # -10 cause this maximizer is for opponent
                    return -10
                elif i[0] == self.opponent:
                    # 10 cause this maximizer is for opponent
                    return 10

        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == self.player:
                # -10 cause this maximizer is for opponent
                return -10
            elif self.board[0][0] == self.opponent:
                # 10 cause this maximizer is for opponent
                return 10

        if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == self.player:
                # -10 cause this maximizer is for opponent
                return -10
            elif self.board[0][2] == self.opponent:
                # 10 cause this maximizer is for opponent
                return 10
        # If winner not yet decided
        return 0


    # checkMove checks if there are any move can be made
    def checkMove(self):
        for i in self.board:
            for j in i:
                if j == '_':
                    return True
        return False

    # Get the score for each possibility
    def minimax(self, player):
        score = self.checkWinner()
        if score == 10 or score == -10:
            return score
        if not self.checkMove():
            return 0
        if player: # Player's move
            best = 1000

            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '_':
                        self.board[i][j] = self.player
                        best = min(best, self.minimax(not player))
                        self.board[i][j] = '_' # Restore
            return best
        else: # Opponent's move
            best = -1000

            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '_':
                        self.board[i][j] = self.opponent
                        best = max(best, self.minimax(not player))
                        self.board[i][j] = '_' # Restore
            return best

    def findBestMove(self):
        best = -1000
        pair = [-1, -1]

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '_':
                    self.board[i][j] = self.opponent # opponent makes its move
                    score = self.minimax(player=True) # After opponent move, so now player move
                    self.board[i][j] = '_' # Restore
                    if score > best:
                        best = score
                        pair[0], pair[1] = i, j
        return pair

    def play(self):
        while self.checkMove() and self.checkWinner() == 0:
            os.system('cls')
            for i in self.board:
                print(i)
            row = input('Choose your row(0-2):')
            col = input('Choose your col(0-2):')
            try:
                row = int(row)
                col = int(col)
                if ((row < 0 or row > 2)
                    or (col < 0 or col > 2)
                    or self.board[row][col] == self.player
                    or self.board[row][col] == self.opponent
                ):
                    raise
                # Check the possible errors
            except:
                while ((row < 0 or row > 2)
                    or (col < 0 or col > 2)
                    or self.board[row][col] == self.player
                    or self.board[row][col] == self.opponent
                ):
                    os.system('cls')
                    for i in self.board:
                        print(i)
                    row = input('Choose your row(0-2):')
                    col = input('Choose your col(0-2):')
                    try:
                        row = int(row)
                        col = int(col)
                    except ValueError:
                        continue
            self.board[row][col] = self.player
            optMove = self.findBestMove()
            self.board[optMove[0]][optMove[1]] = self.opponent
        res = self.checkWinner()
        for i in self.board:
            print(i)
        if res == -10:
            print('Player wins')
        elif res == 10:
            print('Opponent wins')
        else:
            print('Draw')


if __name__ == '__main__':
    tictactoe()