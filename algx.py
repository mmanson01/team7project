#!/usr/bin/env python

import numpy as np
import math
board_size = 4
board_rows = board_size**3
board_cols = (board_size**2)*4
partial_solution = {}
cover_row_dict = {}
deleted_cols = {}
main_matrix = []
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
    col_starting_column = (board_size ** 2)
    cell_starting_column = (board_size**2) * 3
    block_starting_column = (board_size**2) * 2
    row_index_forced = 0
    for row in puzzle:
        col_index_overall = 0
        elems_in_row = set(row)
        # part of row constraint
        elem_index = 0
        for elem in row:
            elems_in_col = set(puzzle[:,col_index_overall])
            end_of_block_col = int(elem_index + math.sqrt(board_size) - (elem_index%math.sqrt(board_size)))
            end_of_block_row = int(row_index_forced + math.sqrt(board_size) - (row_index_forced%math.sqrt(board_size)))
            # print "ENDO OF BLOCK: ", elem_index, row_index_forced, end_of_block_row
            if elem_index%math.sqrt(board_size) == 0:
                if row_index_forced%math.sqrt(board_size) != 0:
                    temp_row_index = row_index_forced - 1
                else:
                    temp_row_index = row_index_forced
                elems_in_block = np.unique(puzzle[temp_row_index:end_of_block_row, elem_index:end_of_block_col])

            # no element, but mark the other elems in the row as  0
            if elem == 0:
                row_index = starting_row
                col_index = matrix_col_index
                for sub_elem in elems_in_row:
                    if sub_elem != 0:
                        matrix[row_index+sub_elem-1][col_index+sub_elem-1] = 0
                for sub_elem in elems_in_block:
                    if sub_elem != 0:
                        x = starting_row + sub_elem - 1
                        rootSize = np.sqrt(board_size)
                        rowIndent = int(((matrix_col_index / board_size) // rootSize) * rootSize)
                        puzzleCol = elem_index
                        colIndent = int(puzzleCol // rootSize)
                        blockIndent = board_size * (rowIndent + colIndent)
                        y = block_starting_column + sub_elem + blockIndent - 1
                        matrix[x][y] = 0
                # # no element, but mark the other elems in the col as 0
                # for sub_elem in elems_in_col:
                #     c_index = col_starting_column + (elem_index*board_size)
                #     if sub_elem != 0:
                #         matrix[row_index+sub_elem-1][c_index+sub_elem-1] = 0

            # there is already an element in this space
            if elem != 0:
                # index for elem to keep 1 is elem - 1
                index_elem = elem - 1

                # adjust row constraints
                for index in range(board_size):
                    x = matrix_row_index + index
                    y = matrix_col_index + index
                    if index != index_elem:
                        if (x,y) not in already_changed:
                            # temp_matrix_col_index = matrix_col_index
                            matrix[x][y] = 0
                    else:
                        matrix[x][y] = 1
                        already_changed.append((x,y))

                # adjust col constraints
                for index in range(board_size):
                    x = matrix_row_index + index
                    y = col_starting_column + index + (board_size * list(row).index(elem))
                    if index != index_elem:
                        if (x,y) not in already_changed:
                            matrix[x][y] = 0
                    else:
                        matrix[x][y] = 1
                        already_changed.append((x,y))
                for i in range(board_size):
                    x = (i * (board_size ** 2)) + index_elem + (board_size * list(row).index(elem))
                    y = col_starting_column + index_elem + (board_size * list(row).index(elem))
                    if x != (matrix_row_index + index_elem):
                        matrix[x][y] = 0

                # adjust block constraints
                for index in range(board_size):
                    x = matrix_row_index + index
                    rootSize = np.sqrt(board_size)
                    rowIndent = int(((matrix_col_index / board_size) // rootSize) * rootSize)
                    puzzleCol = list(row).index(elem)
                    colIndent = int(puzzleCol // rootSize)
                    blockIndent = board_size * (rowIndent + colIndent)
                    y = block_starting_column + index + blockIndent
                    if index != index_elem:
                        if (x,y) not in already_changed:
                            matrix[x][y] = 0
                    else:
                        matrix[x][y] = 1
                        already_changed.append((x,y))


                # adjust cell constraints
                for index in range(board_size):
                    # only need to check if cell has something or not
                    # if cell has an element, then set the rest of the elements
                    # in that cel lblock to 0
                    x = matrix_row_index + index
                    y = cell_starting_column
                    if index != index_elem:
                        if (x,y) not in already_changed:
                            matrix[x][y] = 0
                    else:
                        already_changed.append((x,y))


            matrix_row_index += board_size
            starting_row += board_size
            cell_starting_column += 1
            elem_index += 1
        matrix_col_index += board_size
        row_index_forced += 1
    return matrix

def solve(matrix):
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
    # print "LENGTH", len(matrix)
    print "BEGINNING FUNCTION", len(matrix[0])
    if len(matrix[0]) == 0:
        print "EXIT 1"
        return

    print "ELSE"
    min_count = -1
    # find column with min 1s
    min_ones_index = -1
    for col in range(len(matrix[0])):
        one_count = np.count_nonzero(matrix[:,col])
        if one_count < min_count or min_count==-1:
            if one_count != 0 :
                min_ones_index = col
                min_count = np.count_nonzero(matrix[:,col])
    if min_count == -1:
        min_count = 0
        min_ones_index = 0
    print "MIN: ", min_count, min_ones_index
    print matrix[:,0]
    # if the column with the least 1's has no 1's, terminate
    if min_count == 0:
        print "EXIT 2"
        # return partial_solution
        return
    row_index = 0
    for row in matrix:
        # find the first row in the column were elem==1
        if row[min_ones_index] == 1:
            # include row r in the partial solution
            # partial_solution[row_index] = np.where(row == 1)[0]
            partial_solution[row_index] = row
            new_matrix = cover_row(matrix, row)
            # return new_matrix
            solve(new_matrix)
            print "ROW INDEX", row_index
            # print "LEN Matrix", len(matrix)
            # remove row from solution
            partial_solution.pop(row_index, None)
            # uncover row
            print "LEN", len(matrix[0])
            print row
            print matrix[row_index]
            matrix = uncover_row(matrix, matrix[row_index])
            print "HERE3"
            # reset mins_ones_index
        row_index += 1
    # return partial_solution


def cover_row(matrix, row):
    col_index = 0
    for col in row:
        # for each col such that M[row][col] == 1
        if col == 1:
            row_index = 0
            for rowL in matrix:
                # for each rowL such that M[rowL][col] == 1
                if rowL[col_index] == 1:
                    # cover row...aka add to cover_row
                    # cover_row_dict[row_index] = rowL
                    if row_index not in cover_row_dict.keys():
                        cover_row_dict[row_index] = []
                    cover_row_dict[row_index].append(rowL)
                    # delete rowL from matrix
                    matrix = np.delete(matrix, row_index, axis=0)

                else:
                    row_index += 1
            # delete col from matrix
            if col_index not in deleted_cols.keys():
                deleted_cols[col_index] = []
            deleted_cols[col_index].append(matrix[:,col_index])
            matrix = np.delete(matrix, col_index, axis=1)
        col_index += 1
    return matrix


def uncover_row(matrix, row):
    col_index = 0
    for col in row:
        # for each col such that M[row][col] == 1
        if col == 1:
            row_index = 0
            for rowL in matrix:
                # for each rowL such that M[rowL][col] == 1
                if rowL[col_index] == 1:
                    # add row back to matrix
                    print "row_index", row_index
                    print cover_row_dict[10]
                    matrix = np.insert(matrix, row_index, cover_row_dict[row_index][-1], axis=0)
                    # uncover the row...aka remove from cover_row
                    cover_row_dict[row_index] = cover_row_dict[row_index][:-1]
                    # cover_row_dict.pop(row_index, None)

                else:
                    row_index += 1
            # add back col to matrix
            print "MATRIX LEN: ", len(matrix)
            print "COMPARE ", len(deleted_cols[col_index][-1])
            matrix = np.insert(matrix, col_index, deleted_cols[col_index][-1], axis=1)
            deleted_cols.pop(col_index, None)
        col_index += 1
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
    small_puzzle = np.array([[3, 0, 4, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [2, 0, 0, 3]])
    small_puzzle_answer = np.array([[3, 1, 4, 2],
                                    [4, 2, 3, 1],
                                    [1, 3, 2, 4],
                                    [2, 4, 1, 3]])

    base_matrix = base_sudoku_grid()
    # for row in range(64):
    #     print base_matrix[row]
    # print len(base_matrix)
    # print len(base_matrix[0])
    # print base_matrix[486][216]
    # complete_matrix = puzzleSpecific(base_matrix, ny_times_puzzle)
    complete_matrix = add_original_puzzle(small_puzzle, base_matrix)
    numpy_complete_matrix = np.array(complete_matrix)
    # keep so we can add back columns and rows
    main_matrix = numpy_complete_matrix
    # first_row = []
    # for cols in range(board_cols):
    #     first_row.append(-1)
    # partial_solution = np.array(first_row)
    # partial_solution = {}
    # for row in range(324):
    #     print row, base_matrix[row][243:300]
    # for row in range(64):
    #     print row, complete_matrix[row][0:50]
    solve(numpy_complete_matrix)
    print partial_solution
