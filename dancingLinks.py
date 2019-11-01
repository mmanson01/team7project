import numpy as np

def buildMat(dimension, puzzle):
    #vertical matDim is dimension ^ 3
    rows = dimension ** 3
    #horizontal matDim is (dimension ** 2) * 4
    cols = (dimension ** 2) * 4
    ourMat = np.zeros((rows, cols))

    #build it based on general version first

    for i in range(cols / 4):
        for j in range(rows):
            counter = j // dimension    #using floor division just to ensure behavior
            if counter == i:
                ourMat[j][i] = 1
            if j % dimension == i % dimension:
                #there needs to be one more condition here
                if j // 9 == i:
                    ourMat[j][i + cols/4] = 1
                    ourMat[j][i + 2 * (cols/4)] = 1
                    ourMat[j][i + 3 * (cols/4)] = 1
    #built general matrix, now i need to go back through
    #and change values to reflect our specific puzzle
    return ourMat

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
    dancingLinks(puzzle, ourMat)