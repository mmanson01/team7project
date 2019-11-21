"""
Test different algorithms' run times.
"""
import time
import random
import numpy as np

from manual import manually_solve
from backtracking import solve 
from brute_force import brute_force
from dataCheck import get_puzzles, get_4_puzzles

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
    ## Test 4x4 Puzzles ##
    puzzles = get_4_puzzles()
    back = 0
    brute = 0
    manual = 0

    for p in puzzles:
        back += back_time(p)
        brute += brute_time(p)
        manual += manual_time(p)

    print("Testing 4x4 Puzzle Efficiencies for 10 puzzles:")
    print("Brute Force: {}".format(brute))
    print("Backtracking: {}".format(back))
    print("Manual: {}".format(manual))

    ## Test 9x9 Puzzles ##
    quizzes, solutions = get_puzzles()
    back = 0
    manual = 0
    
    sample = random.sample(range(1000000),1000)
        
    for s in sample:
        puz = quizzes[s]
        back += back_time(puz)
        manual += manual_time(puz)
    
    print("Testing 9x9 Puzzle Efficiencies for 1000 puzzles:")
    print ("Backtracking: {}".format(back))
    print("Manual: {}".format(manual))