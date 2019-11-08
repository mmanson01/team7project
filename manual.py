# human solution
# techniques taken from: https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php

import numpy as np
import math

from tester import test_correctness

def check_row(puzzle, box):
    """Returns all elements in the given row"""
    return [elem for elem in puzzle[box[0]] if elem != 0 and type(elem) is int]

def check_col(puzzle, box):
    """Returns all elements in the given column"""
    return [elem[box[1]] for elem in puzzle if elem[box[1]] != 0 and type(elem[box[1]]) is int]

def check_box(puzzle, box):
    """Returns all elements in the given block"""
    box_size = int(math.sqrt(len(puzzle)))
    i = box[0] // box_size
    j = box[1] // box_size
    temp_box = puzzle[i*box_size:i*box_size + box_size]
    elements = []
    for row in temp_box:
        for elem in row[j*box_size: j*box_size + box_size]:
            if elem != 0 and type(elem) is int:
                elements.append(elem)
    return elements

def sole_candidate(puzzle, box):
    """Compiles list of possible candidates, assigns digit if only one option"""
    n = len(puzzle)
    violations = []
    violations.extend(check_row(puzzle, box))
    violations.extend(check_col(puzzle, box))
    violations.extend(check_box(puzzle, box))
    possibilities = list(set(range(1, n+1)).difference(set(violations)))
    if len(possibilities) == 1:
        puzzle[box[0]][box[1]] = possibilities[0]
    else:
        puzzle[box[0]][box[1]] = possibilities
    return puzzle

def unique_candidate(puzzle):
    """Checks block interactions to assign any unique candidates"""
    n = len(puzzle)    
    box_size = int(math.sqrt(n))
    for i in range(box_size):
        for j in range(box_size):
            for digit in range(1,n+1):
                row_count = [k for k in range(i*box_size, (i+1)*box_size) if digit not in check_row(puzzle, [k,0])]
                col_count = [l for l in range(j*box_size, (j+1)*box_size) if digit not in check_col(puzzle, [0,l])]
                #unique candidate
                possible = []
                for row in row_count:
                    for col in col_count:
                        if (puzzle[row][col] == 0 or type(puzzle[row][col]) is list) and digit not in check_box(puzzle, [row, col]):
                            possible.append([row,col])
                if len(possible) == 1:
                    puzzle[possible[0][0]][possible[0][1]] = digit                 
    return puzzle

def final_sweep(puzzle):
    """Final check to ensure techniques for removing candidates didn't expose new sole candidates"""
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if type(puzzle[row][col]) is not int and len(puzzle[row][col]) == 1:
                puzzle[row][col] = puzzle[row][col][0]
    return puzzle

def np_puzzle(puzzle):
    """Restore puzzle to digits and 0s for checking for change"""
    zero_puzzle = [[elem if type(elem) is int else 0 for elem in row] for row in puzzle]
    return np.array(zero_puzzle)


def naked_subset(puzzle):
    """Removes candidates if those candidates must be assigned to boxes in that column/row"""
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if type(puzzle[row][col]) is not int:
                # find naked subsets and delete its integers from rest of row
                row_poss = [i for i in puzzle[row] if type(i) is not int and set(i) == set(puzzle[row][col])]
                if len(row_poss) == len(puzzle[row][col]):
                    delete = [j for j in range(len(puzzle)) if j not in row_poss and type(puzzle[row][j]) is not int]
                    for elem in delete:
                        for digit in puzzle[row][col]:
                            if digit in puzzle[row][elem]:
                                puzzle[row][elem].remove(digit)
                # find naked subsets and delete its integers from rest of column
                col_poss = [i for i in range(len(puzzle)) if type(puzzle[i][col]) is not int and set(puzzle[i][col]) == set(puzzle[row][col])]
                if len(col_poss) == len(puzzle[row][col]):
                    delete = [j for j in range(len(puzzle)) if j not in col_poss and type(puzzle[j][col]) is not int]
                    for elem in delete:
                        for digit in puzzle[row][col]:
                            if digit in puzzle[elem][col]:
                                puzzle[elem][col].remove(digit)
    return puzzle

def naked_ish(puzzle):
    """Takes away possibilities from rows/cols by observing interactions"""
    box_size = int(math.sqrt(len(puzzle)))
    for i in range(box_size):
        for j in range(box_size):
            #have entered the box level
            for digit in range(1, len(puzzle) + 1):
                if digit not in check_box(puzzle, [i*box_size, j*box_size]):
                    # row_count = [k for k in range(i*box_size, (i+1)*box_size) if digit not in check_row(puzzle, [k,0])]
                    # col_count = [l for l in range(j*box_size, (j+1)*box_size) if digit not in check_col(puzzle, [0,l])]
                    # we want every row and col that this digit could realistically be in
                        # ergo, it must be an entry in that column
                    row_count = []
                    for row in range(i*box_size, (i+1)*box_size):
                        fits = False
                        for col in range(j*box_size, (j+1)*box_size):
                            if type(puzzle[row][col]) is not int and digit in puzzle[row][col]:
                                fits = True
                        if fits:
                            row_count.append(row)
                    col_count = []
                    for col in range(j*box_size, (j+1)*box_size):
                        fits = False
                        for row in range(i*box_size, (i+1)*box_size):
                            if type(puzzle[row][col]) is not int and digit in puzzle[row][col]:
                                fits = True
                        if fits:
                            col_count.append(col)
                    
                    print("Box",i,j)
                    print(digit, row_count, col_count)
                    if len(row_count) == 1:
                        row = row_count[0]
                        for col in range(len(puzzle)):
                            if col not in range(j*box_size, (j+1)*box_size) and type(puzzle[row][col]) is not int:
                                if digit in puzzle[row][col]:
                                    puzzle[row][col].remove(digit)
                    if len(col_count) == 1:
                        col = col_count[0]
                        for row in range(len(puzzle)):
                            if row not in range(i*box_size, (i+1)*box_size) and type(puzzle[row][col]) is not int:
                                if digit in puzzle[row][col]:
                                    puzzle[row][col].remove(digit)
    return puzzle

def manually_solve(puzzle):
    """Compilation of techniques to run until puzzle is complete"""
    n = len(puzzle)
    added_on = True
    count = 0
    while added_on:
        orig_puzzle = np.copy(np_puzzle(puzzle))
        # methods for a single box
        for i in range(n):
            for j in range(n):
                box = [i,j]                
                if puzzle[i][j] == 0 or type(puzzle[i][j]) is not int:
                    puzzle = sole_candidate(puzzle, box) 
        # print("Round {}, sole done: {}".format(count, puzzle))
        # methods that use the whole grid
        puzzle = unique_candidate(puzzle)
        # print("Round {}, unique done: {}".format(count, puzzle))
        # final check to see if the methods changed added on a digit
        puzzle = naked_ish(puzzle)
        puzzle = final_sweep(puzzle)
        if np.array_equal(orig_puzzle, np_puzzle(puzzle)):
            added_on = False
        count += 1
    return puzzle

def check_completion(puzzle):
    zeroes = 0
    for row in puzzle:
        zeroes += np.sum(row==0)
    return zeroes

if __name__ == '__main__':
    ny_times_correct = [[2,3,4,9,5,6,7,8,1],
                         [8,6,5,2,1,7,4,3,9],
                         [7,1,9,8,3,4,5,6,2],
                         [3,2,8,7,9,5,1,4,6],
                         [1,4,7,3,6,8,9,2,5],
                         [9,5,6,1,4,2,8,7,3],
                         [4,8,1,6,2,9,3,5,7],
                         [6,7,3,5,8,1,2,9,4],
                         [5,9,2,4,7,3,6,1,8]]
    ny_times_puzzle = [[0,3,4,9,5,6,0,8,0],
                         [8,6,5,0,0,7,0,3,9],
                         [0,0,9,0,3,0,0,0,2],
                         [3,0,0,7,0,5,1,4,0],
                         [1,0,0,3,0,8,0,0,5],
                         [9,0,6,1,0,0,0,0,0],
                         [0,8,0,0,2,9,0,0,7],
                         [6,7,0,0,0,0,2,9,0],
                         [0,0,0,4,0,0,6,1,0]]
    our_solution = manually_solve(ny_times_puzzle)
    print(np.array_equal(our_solution,ny_times_correct))

    #medium puzzle
    medium = [
        [0,0,9,0,0,0,4,0,0],
        [0,0,0,0,1,7,0,8,0],
        [0,0,0,0,0,2,0,9,7],
        [0,8,2,5,0,0,0,0,0],
        [0,3,7,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,4,6],
        [0,5,0,6,9,3,0,7,0],
        [0,0,0,8,0,0,0,0,0],
        [0,0,0,0,7,0,6,0,0]
    ]
    for row in manually_solve(medium):
        for elem in row:
            print(elem)
    

    medium_manual = np_puzzle(manually_solve(medium))
    print(medium_manual)
    print(check_completion(medium_manual))
    print(test_correctness(medium_manual,9))

    # #sammy's puzzle
    # puzzle = [[0,0,0,6,0,3,0,0,7],
    #           [3,0,0,0,0,2,9,0,0],
    #           [6,0,0,1,7,0,0,0,0],
    #           [4,0,2,0,9,0,0,1,6],
    #           [0,0,7,0,0,0,4,0,0],
    #           [9,6,0,0,1,0,2,0,5],
    #           [0,0,0,0,2,1,0,0,4],
    #           [0,0,4,9,0,0,0,0,1],
    #           [8,0,0,5,0,6,0,0,0]]
    # version = np_puzzle(manually_solve(puzzle))
    # print(version)
    # print(check_completion(version))
