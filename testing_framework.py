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
from dancingLinks import benchmarker

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

def dancing_time(puzzle):
    times = benchmarker(puzzle)
    end = times[1]
    start = times[0]
    return (end - start)

if __name__ == '__main__':
    # ## Test 4x4 Puzzles ##
    #puzzles = get_4_puzzles()
    #back = 0
    #brute = 0
    #manual = 0
    #dancing = 0

    #for p in puzzles:
        #brute += brute_time(p)
        #back += back_time(p)
        #manual += manual_time(p)
        #dancing += dancing_time(p)

    #print("Testing 4x4 Puzzle Efficiencies for 10 puzzles:")
    # print("Brute Force: {}".format(brute))
    # print("Backtracking: {}".format(back))
    # print("Manual: {}".format(manual))
    #print("Dancing: {}".format(dancing))

    ## Test 9x9 Puzzles ##
    quizzes, solutions = get_puzzles()
    back = 0
    manual = 0
    dancing = 0
    trial = 0
    
    sample = random.sample(range(1000000),1000)
    print("Starting trials")   
    for s in sample:
        #print("Trial number: " + str(trial))
        puz = quizzes[s]
        #back += back_time(puz)
        # manual += manual_time(puz)
        dancing += dancing_time(puz)
        #trial += 1
    
    #print("Testing 9x9 Puzzle Efficiencies for 1000 puzzles:")
    #print ("Backtracking: {}".format(back))
    #print("Manual: {}".format(manual))
    print("Dancing: {}".format(dancing))