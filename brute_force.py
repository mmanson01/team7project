"""
Brute force method
"""
from tester import test_correctness
import random
import numpy as np

def brute_force(p,n):
    solved = False
    k = 0
    while not solved:
        print(k)
        k += 1
        orig_puzzle = np.copy(p)
        for i in range(len(p)):
            for j in range(len(p)):
                if p[i][j] == 0:
                    p[i][j] = random.choice(range(1,n+1))
        if k < 10:
            print(p)
        if test_correctness(np.array(p),4) == True:
            solved=True
        else:
            p = np.copy(orig_puzzle)
    return p

if __name__ == '__main__':
    puzzle = [[0,3,4,9,5,6,0,8,0],
                [8,6,5,0,0,7,0,3,9],
                [0,0,9,0,3,0,0,0,2],
                [3,0,0,7,0,5,1,4,0],
                [1,0,0,3,0,8,0,0,5],
                [9,0,6,1,0,0,0,0,0],
                [0,8,0,0,2,9,0,0,7],
                [6,7,0,0,0,0,2,9,0],
                [0,0,0,4,0,0,6,1,0]]
    lil_puzzle = [[4,3,0,0],
                          [1,2,3,0],
                          [0,0,2,0],
                          [2,1,0,0]]
    print(brute_force(puzzle,9))