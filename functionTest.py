from sudoku_generator import *

board = generate_sudoku(9, 10)
for row in range(len(board)):
    for col in range(len(board[0])):
        print(board[row][col], end=" ")
    print()
