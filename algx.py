#!/usr/bin/env python
# algorithm x solution
# if matrix A has no columns, current partial solution is valid solution. terminate.
# else: choose a column c (deterministiaclly)
# choose a row r such that A(r,c)=1 (nondeterministically)
# include row r in the partial solution
# for each column j such that A(r,j)=1
    # for each row i such that A(i,j)=1
        #delete row i from matrix A
    # delete column j from matrix A
# repeat alg recrusively on reduced matrix A

import numpy as np
import math
board_size = 9

# constraints:
# 1) values 1-9 have to be in every row, column, box
# 2) number can't repeat in row, column, or box
# 3) every cell has to have a value
# total of 324 contsratings (81*4) == columns
# 729 rows in matrix (9^3)

def base_sudoku_grid(){
    matrix = []
    # set matrix size to be [size^3][size^2 * 4]
    # size^3 to represent all of the boxes, columns, and rows
    # size^2 * 4 to represent size of board and the four constraints

    # initialize matrix
    for row in range(board_size**3):
        temp_array = []
        for col in range((board_size**2)*4)):
            temp_array.append(-1)
        matrix.append(temp_array)

    base = 0
    # go through row-column constraints
    for

}

def get_matrix(ny_times_puzzle, universe):
    matrix = []


    return matrix

if __name__ == '__main__':
    ny_times_correct = np.array([[2,3,4,9,5,6,7,8,1],
                         [8,6,5,2,1,7,4,3,9],
                         [7,1,9,8,3,4,5,6,2],
                         [3,2,8,7,9,5,1,4,6],
                         [1,4,7,3,6,8,9,2,5],
                         [9,5,6,1,4,2,8,7,3],
                         [4,8,1,6,2,9,3,5,7],
                         [6,7,3,5,8,1,2,9,4],
                         [5,9,2,4,7,3,6,1,8]])
    ny_times_puzzle = np.array([[0,3,4,9,5,6,0,8,0],
                         [8,6,5,0,0,7,0,3,9],
                         [0,0,9,0,3,0,0,0,2],
                         [3,0,0,7,0,5,1,4,0],
                         [1,0,0,3,0,8,0,0,5],
                         [9,0,6,1,0,0,0,0,0],
                         [0,8,0,0,2,9,0,0,7],
                         [6,7,0,0,0,0,2,9,0],
                         [0,0,0,4,0,0,6,1,0]])
    universe = [1,2,3,4,5,6,7,8,9]
    ny_times_matrix = get_matrix(ny_times_puzzle, universe)
    our_solution = solve(ny_times_puzzle)
    print(np.array_equal(our_solution,ny_times_correct))
