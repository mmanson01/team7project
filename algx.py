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
board_size = 4
board_rows = board_size**3
board_cols = (board_size**2)*4
# board_size = 9
# board_rows = board_size**3
# board_cols = (board_size**2)*4

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
        if row_delta == board_size:
            row_delta = 0
            num_rows += 1
        if num_rows == board_size:
            num_rows = 0
            col_delta += board_size
        if col_delta == board_size**2:
            break

    # col constraints ... #col>=81 && #col<162
    col_delta = board_size**2
    row_delta = 0
    for row in matrix:
        row[col_delta + row_delta] = 1
        row_delta += 1
        if row_delta == board_size**2:
            row_delta = 0

    # block constraint
    # TODO: THIS DOESN'T WORK
    col_delta = (board_size**2) * 2
    row_delta = 0
    num_rows = 0
    block_delta = 0
    next_block = 0
    for row in matrix:
        row[col_delta + row_delta] = 1
        row_delta += 1
        # move onto next row
        if row_delta == board_size:
            row_delta = 0
            num_rows += 1
        if num_rows == int(math.sqrt(board_size)):
            num_rows = 0
            col_delta += board_size
            block_delta += 1
        if block_delta == int(math.sqrt(board_size)):
            block_delta = 0
            col_delta -= int(math.sqrt(board_size)**3)
            row_delta = 0
            num_rows = 0
            next_block += 1
        if next_block == int(math.sqrt(board_size)):
            col_delta += int(math.sqrt(board_size)**3)
            next_block = 0

    # cell constraint
    row_delta = 0
    # col_delta = (math.sqrt(board_size)**3) * board_size
    col_delta = (board_size**2) * 3
    next_row = 0
    for row in matrix:
        row[col_delta] = 1
        next_row += 1
        if next_row == board_size:
            col_delta += 1
            next_row = 0


    return matrix

def add_original_puzzle(puzzle, matrix):
    already_changed = []
    # 9 elems per rxcx
    matrix_row_index = 0
    matrix_col_index = 0
    starting_row = 0
    for row in puzzle:
        elems_in_row = set(row)
        for elem in row:
            print "OG elem: ", elem
            # no element, but mark the other elems in the row as  0
            if elem == 0:
                row_index = starting_row
                col_index = 0
                for sub_elem in elems_in_row:
                    if sub_elem == 0:
                        pass
                    print "ELEM: ", sub_elem
                    matrix[row_index+sub_elem-1][col_index+sub_elem-1] = 0
            # there is already an element in this space
            if elem != 0:
                print "elem: ", elem
                # index for elem to keep 1 is elem - 1
                index_elem = elem - 1

                # adjust row constraints
                # 729 rows so we would do num_rows / row_index for starting matrix rows
                # starting_row += matrix_row_index
                print "STARTING ROW: ", matrix_row_index, matrix_col_index

                for index in range(9):
                    print index, " ", index_elem
                    x = matrix_row_index + index
                    y = matrix_col_index + index
                    print "index + index_elem: ", index, index_elem
                    print "x + y: ", x, y
                    if index != index_elem:
                        if (x,y) not in already_changed:
                            # temp_matrix_col_index = matrix_col_index
                            matrix[x][y] = 0
                    else:
                        print "index_elem: ",  index_elem
                        print "x y : ", x, y
                        print "BEFORE: ", matrix[x][y]
                        matrix[x][y] = 1
                        print "AFTER: ", matrix[x][y]
                        already_changed.append((x,y))
                # adjust col constraints

                # adjust block constraints

                # adjust cell constraints

            matrix_row_index += 9
        matrix_col_index += 9
        if matrix_row_index == 324 or matrix_col_index == 324:
            break
        # matrix_row_index += 81
        starting_row += 9
    return matrix

def puzzleSpecific(matrix, puzzle):
    dimension = len(puzzle[0])
    for rowIndex in range(len(puzzle)):
        row = puzzle[rowIndex]
        for column in range(len(row)):
            if row[column] != 0:
                thisNum = row[column] - 1

                # #row column changes
                # rcSpacer = dimension * rowIndex
                # for i in range(dimension):
                #     matrix[rcSpacer + i][column + 3 * (dimension ** 2)] = 0
                #     if i == thisNum:
                #         matrix[rcSpacer + i][column + 3 * (dimension ** 2)] = 1
                # for i in range(dimension):
                #     if i != thisNum:
                #         matrix[(rcSpacer + i) + (dimension * i)][(i * column) + 3 * (dimension ** 2)] = 0
                #
                #row contradiction changes
                # for index in dimension .. [0,9)
                for i in range(dimension):
                    #
                    matrix[(dimension * (i + (dimension * rowIndex))) + thisNum][column + thisNum] = 0
                    if i == rowIndex:
                        for j in range(dimension):
                            matrix[(dimension * (i + (dimension * rowIndex))) + j][column + j] = 0
                        matrix[(dimension * (i + (dimension * rowIndex))) + thisNum][column + thisNum] = 1

                # #column contradiction changes
                # for i in range(dimension):
                #     matrix[thisNum + ((dimension ** 2) * i)][thisNum + (column * dimension) + 2 * (dimension ** 2)] = 0
                #     if i == rowIndex:
                #         for j in range(dimension):
                #             matrix[j + ((dimension ** 2) * i)][i + (column * dimension) + 2 * (dimension ** 2)] = 0
                #         matrix[thisNum + ((dimension ** 2) * i)][thisNum + (column * dimension) + 2 * (dimension ** 2)] = 1

                #box contradiction changes
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
    # print len(base_matrix)
    # print len(base_matrix[0])
    # print base_matrix[486][216]
    # complete_matrix = puzzleSpecific(base_matrix, ny_times_puzzle)
    # complete_matrix = add_original_puzzle(ny_times_puzzle, base_matrix)
    # for row in range(324):
    #     print row, complete_matrix[row][0:45]
    for row in range(64):
        print row, base_matrix[row][48:]

    # print(complete_matrix[0][0:9])
    # ny_times_matrix = get_matrix(ny_times_puzzle, universe)
    # our_solution = solve(ny_times_puzzle)
    # print(np.array_equal(our_solution,ny_times_correct))
