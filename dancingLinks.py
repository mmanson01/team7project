import numpy as np
import time

header = None
solution = []

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
            end_of_block_col = int(elem_index + np.sqrt(board_size) - (elem_index%np.sqrt(board_size)))
            end_of_block_row = int(row_index_forced + np.sqrt(board_size) - (row_index_forced%np.sqrt(board_size)))
            # print "ENDO OF BLOCK: ", elem_index, row_index_forced, end_of_block_row
            if elem_index%np.sqrt(board_size) == 0:
                if row_index_forced%np.sqrt(board_size) != 0:
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
          
class dancingLink:
    left = None
    right = None
    up = None
    down = None
    myCol = None
    
    def __init__(self, column = None):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.myCol = column   
    
    def hookDown(self, nextLink):
        nextLink.down = self.down
        nextLink.down.up = nextLink
        nextLink.up = self
        self.down = nextLink
        return nextLink
    
    def hookRight(self, nextLink):
        nextLink.right = self.right
        nextLink.right.left = nextLink
        nextLink.left = self
        self.right = nextLink
        return nextLink
    
    def separateLeftRight(self):
        self.left.right = self.right
        self.right.left = self.left
    
    def connectLeftRight(self):
        self.left.right = self
        self.right.left = self
        
    def separateUpDown(self):
        self.up.down = self.down
        self.down.up = self.up
    
    def connectUpDown(self):
        self.up.down = self
        self.down.up = self
    
class columnLink(dancingLink):
    weight = 0
    position = None
    
    def __init__(self, pos):
        super().__init__()
        self.weight = 0
        self.position = pos
        self.myCol = self
    
    def cover(self):
        self.separateLeftRight()
        i = self.down
        seenOuter = []
        while (i not in seenOuter):
            j = self.right
            seen = []
            while (j not in seen):
                #print("Self column: " + str(self.position))
                #print("This column: " + str(j.position))
                j.separateUpDown()
                j.myCol.weight = j.myCol.weight - 1
                seen.append(j)
                j = j.right
            seenOuter.append(i)
            i = i.down
        header.weight = header.weight - 1
            
    def uncover(self):
        i = self.up
        seenOuter = []
        while (i not in seenOuter):
            j = self.left
            seen = []
            while (j not in seen):
                j.myCol.weight = j.myCol.weight + 1
                j.connectUpDown
                seen.append(j)
                j = j.left
            seenOuter.append(i)
            i = i.up
        self.connectLeftRight
        header.weight = header.weight + 1
    
def solverFunc(level):
    if header == None:
        return solution
    if header.right.position == header.position or header.weight <= 0:
        return solution
    else:
        thisCol = header.right
        selectedCol = header.right
        minOnes = float("inf")
        while thisCol != header:
            if thisCol.weight < minOnes:
                minOnes = thisCol.weight
                selectedCol = thisCol
            thisCol = thisCol.right
        
        selectedCol.cover()
        
        row = selectedCol.down
        while row != selectedCol:
            solution.append(row)
            coverMe = row.right
            seen = []
            while coverMe not in seen:
                coverMe.myCol.cover()
                seen.append(coverMe)
                coverMe = coverMe.right
            print("Header weight: " + str(header.weight))
            print("Recursion level: " + str(level + 1))
            solverFunc(level + 1)
            if header.right.position == header.position or header.weight <= 0:
                break
            row = solution.pop()
            thisCol = row.myCol
            
            unCoverMe = row.left
            while unCoverMe != row:
                unCoverMe.myCol.uncover()
                unCoverMe = unCoverMe.left
            
        selectedCol.uncover()
    

def listGrid(puzzle, ourMat):
    rows = len(ourMat)
    cols = len(ourMat[0])
    thisheader = columnLink("header")
    allCols = []
    
    for i in range(cols):
        newCol = columnLink(str(i))
        allCols.append(newCol)
        thisheader = thisheader.hookRight(newCol)
    thisheader = thisheader.right.myCol
    
    for i in range(rows):
        previous = None
        for j in range(cols):
            if (ourMat[i][j] == 1):
                thisCol = allCols[j]
                newLink = dancingLink(thisCol)
                if previous == None:
                    previous = newLink
                thisCol.up.hookDown(newLink)
                previous = previous.hookRight(newLink)
                thisCol.weight = thisCol.weight + 1
    
    thisheader.weight = cols
    
    return thisheader
        
def benchmarker(puzzle):
    dimension = len(puzzle)
    ourMat = buildMat(dimension, puzzle)
    ourMat = puzzleSpecific(ourMat, puzzle)
    header = listGrid(puzzle, ourMat)
    start = time.time()
    populateSolutions = solverFunc(0)
    end = time.time()
    return [start, end]

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
    dimension = 9

    ourMat = buildMat(dimension, ny_times_puzzle)
    ourMat = puzzleSpecific(ourMat, ny_times_puzzle)
    header = listGrid(ny_times_puzzle, ourMat)
    populateSolutions = solverFunc(0)