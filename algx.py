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

def base_sudoku_grid():
    matrix = []
    # set matrix size to be [size^3][size^2 * 4]
    # size^3 to represent all of the boxes, columns, and rows
    # size^2 * 4 to represent size of board and the four constraints

    # initialize matrix
    # 324 columns
    for col in range(board_size**3):
        temp_array = []
        # 729 rows
        for row in range((board_size**2)*4):
            # set everything to 0 at first
            temp_array.append(0)
        matrix.append(temp_array)
    # matrix:
    #       row constraint ... col constraint ... box constraint ... cell constraint
    #       123456789 123456789 x 81 x 4
    # r1c1
    # r1c1
    # r1c1
    #...
    # r1c2
    # r1c2
    # ...
    # r1c3
    # ...

    # row constraints ... #col<81
    col_delta = 0
    row_delta = 0
    num_rows = 0
    for row in matrix:
        #for row_constraint in range(81):
        # fill in all of the possible numbers for r1, r2, r3, etc.
        row[col_delta + row_delta] = 1
        row_delta += 1
        if row_delta == 9:
            row_delta = 0
            num_rows += 1
        if num_rows == 9:
            num_rows = 0
            col_delta += 9
        if col_delta == 81:
            break

    # col constraints ... #col>=81 && #col<162
    col_delta = 81
    row_delta = 0
    for row in matrix:
        row[col_delta + row_delta] = 1
        row_delta += 1
        if row_delta == 81:
            row_delta = 0

    # block constraint
    col_delta = 162
    row_delta = 0
    num_rows = 0
    block_delta = 0
    next_block = 0
    for row in matrix:
        row[col_delta + row_delta] = 1
        row_delta += 1
        # move onto next row
        if row_delta == 9:
            row_delta = 0
            num_rows += 1
        if num_rows == 3:
            num_rows = 0
            col_delta += 9
            block_delta += 1
        if block_delta == 3:
            block_delta = 0
            col_delta -= 27
            row_delta = 0
            num_rows = 0
            next_block += 1
        if next_block == 3:
            col_delta += 27
            next_block = 0
        if col_delta == 243:
            break

    # cell constraint
    row_delta = 0
    col_delta = 243
    for row in matrix:
        print row_delta
        row[col_delta + row_delta] = 1
        row_delta += 1
        if col_delta == 324:
            break

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
    base_matrix = base_sudoku_grid()
    print len(base_matrix)
    print len(base_matrix[0])
    print base_matrix[486][216]
    # ny_times_matrix = get_matrix(ny_times_puzzle, universe)
    # our_solution = solve(ny_times_puzzle)
    # print(np.array_equal(our_solution,ny_times_correct))
