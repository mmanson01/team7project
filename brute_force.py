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
        # print(k)
        k += 1
        orig_puzzle = np.copy(p)
        for i in range(len(p)):
            for j in range(len(p)):
                if p[i][j] == 0:
                    p[i][j] = random.choice(range(1,n+1))
        if test_correctness(np.array(p),n) == True:
            solved=True
        else:
            p = np.copy(orig_puzzle)
    return p, k