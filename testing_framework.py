"""
Test different algorithms' run times.
"""
import time
import random

from manual import manually_solve
from backtracking import solve 
from brute_force import brute_force
from dataCheck import get_puzzles

def manual_time(puzzle):
    start = time.time()
    puzzle = manually_solve(puzzle)
    end = time.time()
    return (end - start)

def brute_time(puzzle):
    start = time.time()
    puzzle = brute_force(puzzle, len(puzzle))
    end = time.time()
    return (end - start)

def back_time(puzzle):
    start = time.time()
    solve(puzzle, len(puzzle))
    end = time.time()
    return (end - start)



if __name__ == '__main__':
    lil_puzzle = [[4,3,0,0],
                [1,2,3,0],
                [0,0,2,0],
                [2,1,0,0]]
    # easy_puzzle = [[0,3,4,9,5,6,0,8,0],
    #                      [8,6,5,0,0,7,0,3,9],
    #                      [0,0,9,0,3,0,0,0,2],
    #                      [3,0,0,7,0,5,1,4,0],
    #                      [1,0,0,3,0,8,0,0,5],
    #                      [9,0,6,1,0,0,0,0,0],
    #                      [0,8,0,0,2,9,0,0,7],
    #                      [6,7,0,0,0,0,2,9,0],
    #                      [0,0,0,4,0,0,6,1,0]]
    # hard_puzzle = [[0,0,0,6,0,3,0,0,7],
    #           [3,0,0,0,0,2,9,0,0],
    #           [6,0,0,1,7,0,0,0,0],
    #           [4,0,2,0,9,0,0,1,6],
    #           [0,0,7,0,0,0,4,0,0],
    #           [9,6,0,0,1,0,2,0,5],
    #           [0,0,0,0,2,1,0,0,4],
    #           [0,0,4,9,0,0,0,0,1],
    #           [8,0,0,5,0,6,0,0,0]]
    
    # hard2_puzzle = [[0,0,0,0,0,4,0,8,0],
    #                 [6,0,4,0,0,0,2,0,0],
    #                 [0,0,0,0,9,0,0,0,0],
    #                 [0,0,7,6,0,0,3,0,0],
    #                 [4,8,0,5,0,0,0,7,0],
    #                 [0,0,0,0,0,3,0,0,0],
    #                 [7,0,0,3,0,0,8,0,0],
    #                 [8,0,0,0,0,9,0,5,2],
    #                 [0,1,9,8,0,0,0,0,0]]

    # print("Brute Force takes: {}".format(brute_time(lil_puzzle)))
    print("Easy Puzzle:")
    print("Backtracking takes: {}".format(back_time(easy_puzzle)))
    print("Manual takes: {}".format(manual_time(easy_puzzle)))
    print()

    print("Hard Puzzle:")
    print("Backtracking takes: {}".format(back_time(hard_puzzle)))
    print("Manual takes: {}".format(manual_time(hard_puzzle)))
    print()

    print("Hard Puzzle 2:")
    print("Backtracking takes: {}".format(back_time(hard2_puzzle)))
    print("Manual takes: {}".format(manual_time(hard2_puzzle)))
    print()


    quizzes, solutions = get_puzzles()
    back = 0
    manual = 0
    
    sample = random.sample(range(1000000),1000)
        
    for s in sample:
        puz = quizzes[s]
        back += back_time(puz)
        manual += manual_time(puz)
    print ("Back: {}".format(back))
    print("Manual: {}".format(manual))