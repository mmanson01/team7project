import numpy as np

def buildMat(board_size, puzzle):
#    #vertical matDim is dimension ^ 3
#    rows = dimension ** 3
#    #horizontal matDim is (dimension ** 2) * 4
#    cols = (dimension ** 2) * 4
#    ourMat = np.zeros((rows, cols))
#
#    #build it based on general version first
#
#    for i in range(cols / 4):
#        for j in range(rows):
#            counter = j // dimension    #using floor division just to ensure behavior
#            if counter == i:
#                ourMat[j][i] = 1
#            if j % dimension == i % dimension:
#                #there needs to be one more condition here
#                if j // 9 == i:
#                    ourMat[j][i + cols/4] = 1
#                    ourMat[j][i + 2 * (cols/4)] = 1
#                    ourMat[j][i + 3 * (cols/4)] = 1
#    #built general matrix, now i need to go back through
#    #and change values to reflect our specific puzzle
#    return ourMat

#for now, using mallory's code since it works to set up the full standard matrix
#may return to this later, but for now we have min. viable so i'll move forward

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
        row[col_delta + row_delta] = 1
        row_delta += 1
        if col_delta == 324:
            break
        if row_delta == 81:
            break

    #at this point, the base matrix is built, now to edit it for the puzzle specific one
    return matrix

def puzzleSpecific(matrix, puzzle):
    dimension = len(puzzle[0])
    for rowIndex in range(len(puzzle)):
        row = puzzle[rowIndex]
        for column in range(len(row)):
            if row[column] != 0:
                thisNum = row[column] - 1

                #row column changes
                rcSpacer = dimension * rowIndex
                for i in range(dimension):
                    matrix[rcSpacer + i][column + 3 * (dimension ** 2)] = 0
                    if i == thisNum:
                        matrix[rcSpacer + i][column + 3 * (dimension ** 2)] = 1
                for i in range(dimension):
                    if i != thisNum:
                        matrix[(rcSpacer + i) + (dimension * i)][(i * column) + 3 * (dimension ** 2)] = 0
                
                #row contradiction changes
                for i in range(dimension):
                    matrix[(dimension * (i + (dimension * rowIndex))) + thisNum][column + thisNum] = 0
                    if i == rowIndex:
                        for j in range(dimension):
                            matrix[(dimension * (i + (dimension * rowIndex))) + j][column + j] = 0
                        matrix[(dimension * (i + (dimension * rowIndex))) + thisNum][column + thisNum] = 1

                #column contradiction changes
                for i in range(dimension):
                    matrix[thisNum + ((dimension ** 2) * i)][thisNum + (column * dimension) + 2 * (dimension ** 2)] = 0
                    if i == rowIndex:
                        for j in range(dimension):
                            matrix[j + ((dimension ** 2) * i)][i + (column * dimension) + 2 * (dimension ** 2)] = 0
                        matrix[thisNum + ((dimension ** 2) * i)][thisNum + (column * dimension) + 2 * (dimension ** 2)] = 1

                #box contradiction changes
          


def dancingLinks(puzzle, ourMat):
    dimension = len(puzzle[0])
    
    rows = dimension ** 3   #need to change this to ourMat's current dimensions
    cols = (dimension ** 2) * 4
    
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

    ourMat = buildMat(dimension, puzzle)
    ourMat = puzzleSpecific(ourMat, puzzle)
    dancingLinks(puzzle, ourMat)