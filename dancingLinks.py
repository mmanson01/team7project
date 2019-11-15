import numpy as np

def buildMat(board_size, puzzle):
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
        if num_rows == int(np.sqrt(board_size)):
            num_rows = 0
            col_delta += board_size
            block_delta += 1
        if block_delta == int(np.sqrt(board_size)):
            block_delta = 0
            col_delta -= int(np.sqrt(board_size)**3)
            row_delta = 0
            num_rows = 0
            next_block += 1
        if next_block == int(np.sqrt(board_size)):
            col_delta += int(np.sqrt(board_size)**3)
            next_block = 0

    # cell constraint
    row_delta = 0
    # col_delta = (np.sqrt(board_size)**3) * board_size
    col_delta = (board_size**2) * 3
    next_row = 0
    for row in matrix:
        row[col_delta] = 1
        next_row += 1
        if next_row == board_size:
            col_delta += 1
            next_row = 0

    return matrix

def puzzleSpecific(matrix, puzzle):
    board_size = len(puzzle)
    already_changed = []
    # 9 elems per rxcx
    matrix_row_index = 0
    matrix_col_index = 0
    starting_row = 0
    col_starting_column = (board_size ** 2)
    block_starting_column = (board_size ** 2) * 2
    cell_starting_column = (board_size**2) * 3
    for row in puzzle:
        elems_in_row = set(row)
        # part of row constraint
        for elem in row:
            # no element, but mark the other elems in the row as  0
            if elem == 0:
                row_index = starting_row
                col_index = matrix_col_index
                for sub_elem in elems_in_row:
                    if sub_elem != 0:
                        matrix[row_index+sub_elem-1][col_index+sub_elem-1] = 0
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
                #for i in range(board_size ** 3):
                #    print(matrix[i][col_starting_column:col_starting_column + board_size**2])
                #print("hi")
                # adjust block constraints
                for index in range(board_size):
                    x = matrix_row_index + index
                    y = block_starting_column + index
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
        matrix_col_index += board_size
        # if matrix_row_index == 324 or matrix_col_index == 324:
        #     break
        # matrix_row_index += 81
        # starting_row += board_size
    return matrix
          


def dancingLinks(puzzle, ourMat):
    dimension = len(puzzle[0])
    
    rows = len(ourMat[0])  #need to change this to ourMat's current dimensions
    cols = len(ourMat)
    
    minOnes = float("inf")
    colLeastOnes = -1
    #this following for loop is actually where things get
    #super inefficient
    #this is why knuth implements a "sparse matrix" and is
    #our next big step after getting this alg running at all
    for i in range(cols):
        thisColOnes = 0
        for j in range(rows):
            if ourMat[j][i] == 1:
                thisColOnes = thisColOnes + 1
        if thisColOnes < minOnes:
            minOnes = thisColOnes
            colLeastOnes = i
    oneRowsinCol = []
    for i in range(rows):
        if ourMat[i][colLeastOnes] == 1:
            oneRowsinCol.append(i)
    whichRow = np.random.randint(0, len(oneRowsinCol))
    #this is where my understanding trails off for now
    #but essentially you use the deterministic, lowest 1s
    #column and the non-deterministic row that intersects
    #with that column and holds a 1 to delete those rows
    #and columns and recurse until you reach a final state
    #space, will read more this weekend and finish this

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
    
    puzzle = np.array([[1,0,3,0],
                      [0,0,0,2],
                      [4,0,0,0],
                      [0,1,0,3]])
    dimension = 4

    ourMat = buildMat(dimension, puzzle)
    ourMat = puzzleSpecific(ourMat, puzzle)
    dancingLinks(puzzle, ourMat)