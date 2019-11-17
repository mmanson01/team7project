# human solution
# techniques taken from: https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php

import numpy as np
import math

from tester import test_correctness
from backtracking import solve

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

def sole_candidate(puzzle):
    """Compiles list of possible candidates, assigns digit if only one option"""
    n = len(puzzle)
    for i in range(n):
        for j in range(n):
            box = [i,j]
            if (type(puzzle[i][j]) is int and puzzle[i][j] == 0) or (type(puzzle[i][j]) is not int):
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
                row_poss = [i for i in range(len(puzzle[row])) if type(puzzle[row][i]) is not int and set(puzzle[row][i]) == set(puzzle[row][col])]
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

def naked_singles(puzzle):
    """Takes away possibilities from rows/cols by observing interactions"""
    box_size = int(math.sqrt(len(puzzle)))
    for i in range(box_size):
        for j in range(box_size):
            #have entered the box level
            for digit in range(1, len(puzzle) + 1):
                if digit not in check_box(puzzle, [i*box_size, j*box_size]):
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
    added_on = True
    count = 0
    puzzle = puzzle.tolist()
    while added_on:
        orig_puzzle = np.copy(np_puzzle(puzzle))
        puzzle = sole_candidate(puzzle) 
        puzzle = unique_candidate(puzzle)
        puzzle = naked_subset(puzzle)
        puzzle = naked_singles(puzzle)
        puzzle = final_sweep(puzzle)
        if np.array_equal(orig_puzzle, np_puzzle(puzzle)):
            added_on = False
        count += 1
        
    #applies backtracking algorithm to unsolved puzzles
    size = len(puzzle)
    unsolved = np_puzzle(puzzle)
    if (not (check_completion(unsolved) == 0)):
        solve(unsolved, size)
        return unsolved
        
    #returns solved puzzle
    return np_puzzle(puzzle)
   

def check_completion(puzzle):
    zeroes = 0
    for row in puzzle:
        zeroes += np.sum(row==0)
    return zeroes
