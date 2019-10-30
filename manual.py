#!/usr/bin/env python
# human solution
# begin by combing through grid and seeing if there are any actual possibilities
import numpy as np
import math

def check_row(puzzle, box):
    return [elem for elem in puzzle[box[0]] if elem != 0]

def check_col(puzzle, box):
    return [elem[box[1]] for elem in puzzle if elem[box[1]] != 0]

def check_box(puzzle, box):
    box_size = int(math.sqrt(len(puzzle)))
    i = box[0] // box_size
    j = box[1] // box_size
    temp_box = puzzle[i*box_size:i*box_size + box_size]
    elements = []
    for row in temp_box:
        for elem in row[j*box_size: j*box_size + box_size]:
            elements.append(elem)
    return elements

def easy_adds(puzzle):
    n = len(puzzle)
    added_on = False
    for i in range(n):
        for j in range(n):
            box = [i,j]
            if puzzle[i][j] == 0:
                violations = []
                violations.extend(check_row(puzzle, box))
                violations.extend(check_col(puzzle, box))
                violations.extend(check_box(puzzle, box))
                possibilities = list(set(range(1, n+1)).difference(set(violations)))
                if len(possibilities) == 1:
                    puzzle[i][j] = possibilities[0]
                    added_on = True
    return puzzle, added_on

def manually_solve(puzzle):
    added_on = True
    count = 0
    while added_on:
        puzzle, added_on = easy_adds(puzzle)
        count += 1
        print(count)
    return puzzle

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
    our_solution = manually_solve(ny_times_puzzle)
    print(np.array_equal(our_solution,ny_times_correct))
