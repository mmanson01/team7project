# purely backtracking algorithm

import numpy as np
import math
from tester import test_correctness

location = (0,0)

def print_grid(grid, n): 
    for i in range(n): 
        for j in range(n): 
            print grid[i][j], 
        print ('')
        
def empty(grid, n):
    for i in range(n):
        for j in range(n):
            if (grid[i][j] == 0):
                return (i,j)
    return False
                
def in_column(grid, column, num, n):
    for i in range(n): 
        if(grid[i][column] == num): 
            return True
    return False

def in_row(grid,row,num, n): 
    for i in range(n): 
        if(grid[row][i] == num): 
            return True
    return False
    
def in_box(grid,row, column, num, n):
    sqrtn = int(math.sqrt(n))
    for i in range(sqrtn): 
        for j in range(sqrtn): 
            if(grid[i+row][j+column] == num): 
                return True
    return False
    
def solve(problem, n):
    
    position = empty(problem, n)
    if (position == False):
        return True
    row = position[0]
    column = position[1]
    
    for x in range(1,n+1):
        if (not in_row(problem, row, x, n) and not in_column(problem, column, x, n) and not in_box(problem,row - row%int(math.sqrt(n)),column - column%int(math.sqrt(n)),x, n)):
            problem[row][column] = x
            if (solve(problem, n)):
                return True
            problem[row][column] = 0
    return False

if __name__ == "__main__":
     problem = np.array([[0,0,0,2,6,0,7,0,1],
                         [6,8,0,0,7,0,0,9,0],
                         [1,9,0,0,0,4,5,0,0],
                         [8,2,0,1,0,0,0,4,0],
                         [0,0,4,6,0,2,9,0,0],
                         [0,5,0,0,0,3,0,2,8],
                         [0,0,9,3,0,0,0,7,4],
                         [0,4,0,0,5,0,0,3,6],
                         [7,0,3,0,1,8,0,0,0]])

     solve(problem, 9)
     print_grid(problem, 9)
     print test_correctness(problem,9)
     
     problem2 = np.array([[4,3,0,0],
                          [1,2,3,0],
                          [0,0,2,0],
                          [2,1,0,0]])
    
     solve(problem2, 4)
     print_grid(problem2, 4)
     print test_correctness(problem2,4)
                                             
     solution = np.array([[4,3,5,2,6,9,7,8,1],
                         [6,8,2,5,7,1,4,9,3],
                         [1,9,7,8,3,4,5,6,2],
                         [8,2,6,1,9,5,3,4,7],
                         [3,7,4,6,8,2,9,1,5],
                         [9,5,1,7,4,3,6,2,8],
                         [5,1,9,3,2,6,8,7,4],
                         [2,4,8,9,5,7,1,3,6],
                         [7,6,3,4,1,8,2,5,9]])
     #print_grid(solution)
                         
                    
                         