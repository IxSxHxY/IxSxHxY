# Version:

- Python 3.10.7
- Pygame 2.1.2

# Concept:

We don’t have an optimal method to solve the sudoku, so instead, we are going to try all the possibilities.

Here we will introduce backtracking. What is backtracking?

Backtracking is a computational algorithm that will go through all the outcomes so that we can get the optimal answers.

Demo: 
<img src="https://github.com/IxSxHxY/Tutorial/blob/main/Sudoku%20Solver%20using%20Pygame/Sudoku%20Solver.gif?raw=true">


Algorithms

1. We will use recursion to loop through `row` and `col`. If we reached the base case, we will get `True` as a response that we don’t need to continue doing backtracking
    
    The base case will be `row == 8 and col == 9`, which both of them reach the last row and column. (`column == 9` because `board[row][8]` might be empty)
    
    What if `board[row][column] != 0`? Then we need to skip this column
    
    Since we use `col+1` as the next case, it will reach `board[row][9]`, so If `col == 9`, we go to the next row.
        
2. For backtracking, we are going to try all the input for the empty position. However, it might be too much cases. Now we need to eliminate some impossible candidates. 
    
    As we all know, in sudoku, the same number cannot be appeared in the same row, same column, and same 3x3 space, So we need to check these.
    
3. Now we completed the checking function. Let’s get to the part where we will try all the possible candidates.
    
    Possible candidates is in the range of [1, 9]. So we just try all of them. After we tried, don’t forget to initialize `board[row][col]` because it might affect the other cases.
    
    But how do we know the sudoku is solved? Look at the base case, if we reach the base case, the problem solved. It will return `True` as the result. So if `solver(board, row, col+1) == True`, we solved the problem.
