from tictactoe import *
import unittest

class TestTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testCheckMove(self):
        testCases = []
        testCases.append(
            ([['','',''] for _ in range(3)], True)
        )
        testCases.append(
            ([['X','O','X'] for _ in range(3)], False)
        )
        testCases.append(
            ([['X','O',''] for _ in range(3)], True)
        )
        print('Testing checkMove() function')
        for i in testCases:
            temp = tictactoe(i[0])
            print('Currently testing if this board have any moves')
            temp.printBoard()
            res = temp.checkMoves()
            self.assertEqual(res, i[1], msg=f'The result should be {i[1]}, but it is {res}')
            print('The result is correct which is ', i[1])
        print(f'checkMove() passes all {len(testCases)} test cases\n')

    def testCheckWin(self):
        testCases = []
        testCases.append(
            ([['', '', ''] for _ in range(3)], 0)
        )
        testCases.append(
            ([
                ['X','O',''],
                ['','X',''],
                ['','O','X']
             ], tictactoe.Player['win'])
        )
        testCases.append(
            ([
                ['O','O','O'],
                ['','','X'],
                ['','','X']
            ], tictactoe.AI['win'])
        )
        print('Testing checkWin() function')
        print('** AI=O, If AI wins, then -1 **')
        print('** Player=X, If Player wins, then 1 **')
        for i in testCases:
            temp = tictactoe(i[0])
            print('Currently testing if anyone wins or not')
            temp.printBoard()
            res = temp.checkWin()
            self.assertEqual(res, i[1], msg=f'The result should be {i[1]}, but it is {res}')
            print('The result is correct which is ', i[1])
        print(f'checkMove() passes all {len(testCases)} test cases\n')

    def testMakeMove(self):
        testCases = []
        testCases.append(
            ([['', '', ''] for _ in range(3)], True, 0, 0)
        )
        testCases.append(
            ([
                 ['O', 'O', 'O'],
                 ['', '', 'X'],
                 ['', '', 'X']
             ], False, 0, 0)
        )
        testCases.append(
            ([
                 ['O', 'O', 'O'],
                 ['', '', 'X'],
                 ['', '', 'X']
             ], False, 1, 0)
        )
        testCases.append(
            ([
                 ['O', 'O', 'O'],
                 ['', '', 'X'],
                 ['', '', 'X']
             ], True, 2, 2)
        )
        testCases.append(
            ([
                 ['O', 'O', 'O'],
                 ['', '', 'X'],
                 ['', '', 'X']
             ], False, 0, 0)
        )
        # (board, playerTurn, row, col)
        print('Testing makeMove() function')
        print('** AI=O **')
        print('** Player=X **')
        for board, playerTurn, row, col in testCases:
            temp = tictactoe(board)
            print('Currently testing if the move made is valid or not')
            temp.printBoard()
            temp.playerTurn = playerTurn
            if board[row][col] == '':
                print(f'board[{row}][{col}] should be {(tictactoe.Player["sign"] if playerTurn else tictactoe.Player["sign"])}')
            else:
                print(f'board[{row}][{col}] should not be changed')
            temp.makeMove(row, col)
            board[row][col] = (
                tictactoe.Player['sign'] if board[row][col] != '' and playerTurn else
                tictactoe.AI['sign']
            )


            self.assertEqual(board, temp.board, msg=f'The result should be {board}, but it is {temp.board}')
            print('The result is correct which is ', board)
        print(f'makeMove() passes all {len(testCases)} test cases\n')

    def tearDown(self) -> None:
        pass

if __name__ == '__main__':
    unittest.main()