import numpy as np


game_board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 4, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 8, 0, 0, 7, 9]]


def possible(y, x, n):
    global game_board
    for i in range(0, 9):
        if game_board[y][i] == n:
            return False
    for i in range(0, 9):
        if game_board[i][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0, 3):
        for j in range(0, 3):
            if game_board[y0+i][x0+j] == n:
                return False

    return True


def solve():
    global game_board
    for y in range(9):
        for x in range(9):
            if game_board[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        game_board[y][x] = n
                        solve()
                        game_board[y][x] = 0
                return
    print(np.matrix(game_board))
    input("MORE?")


solve()
