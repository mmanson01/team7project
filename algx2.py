#!/usr/bin/env python

import numpy as np
import math
updates = {}
covered_cols = {}
B = {}
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

def print_solution():
    """Print the solution - selected rows."""
    print "SOLUTION", updates
    for k in B:
            for node in B[k]:
                print node[1],
            print

def choose_col():
    cols = [c for c in covered_cols if not covered_cols[c]]
    if not cols:
        raise CoverError("all columns are covered") # Some columns can have no rows.
    tmp = dict([(c,0) for c in cols])
    for (r,c) in A:
        if c in cols:
            tmp[c] = tmp[c] + 1
    min_c = cols[0]
    for c in cols:
        if tmp[c] < tmp[min_c]:
            min_c = c
    return min_c

def search(k):
    if not A: #Aisempty
        for c in covered_cols:
            if not covered_cols[c]: # blind alley
                return
    c = choose_col()
    # Choose rows such that A[r,c]=1.
    rows = [node[0] for node in A if node[1]==c]
    if not rows: # blind alley
        return
    for r in rows:
        box = [] # a place for temporaly removed rows # Include r in the partial solution.
        B[k] = [node for node in A if node[0]==r]
        # Remove row r from A.
        for node in B[k]:
            box.append(node)
            A.remove(node)
            updates[k] = updates.get(k,0) + 1
        # Choose columns j such that A[r,j]==1 (c is included). cols = [node[1] for node in B[k]]
        for j in cols:
            covered_cols[j] = True
            # Choose rows i such
            rows2 = [node[0] for node in A if node[1]==j]
            tmp = [node for node in A if node[0] in rows2]
            for node in tmp:
                box.append(node)
                A.remove(node)
                updates[k] = updates.get(k,0) + 1
        search(k+1)
        # Restore deleted rows.
        for node in box:
            A.append(node)
        del box
        del B[k]
        # Uncover columns.
        for j in cols:
            covered_cols[j] = False
    return

if __name__ == '__main__':
    small_puzzle = np.array([[3, 0, 4, 2],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [2, 0, 0, 3]])
    small_puzzle_answer = np.array([[3, 1, 4, 2],
                                    [4, 2, 3, 1],
                                    [1, 3, 2, 4],
                                    [2, 4, 1, 3]])

    base_matrix = base_sudoku_grid()
    complete_matrix = add_original_puzzle(small_puzzle, base_matrix)
    A = np.array(complete_matrix)
    for (r, c) in A: covered_cols[c] = False
    search(0)
    print_solution()
