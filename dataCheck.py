# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 12:17:25 2019

@author: Justin
"""

import numpy as np

def get_puzzles():
    sudoku = "sudoku.csv"
    quizzes = np.zeros((1000000, 81), np.int32)
    solutions = np.zeros((1000000, 81), np.int32)
    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:]):
        quiz, solution = line.split(",")
        for j, q_s in enumerate(zip(quiz, solution)):
            q, s = q_s
            quizzes[i, j] = q
            solutions[i, j] = s
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    return quizzes, solutions

def get_4_puzzles():
    return (
        [
            np.array([[3,2,1,4],[4,1,2,3],[1,4,3,2],[2,3,4,1]]),
            np.array([[4,1,2,3],[2,3,4,1], [3,4,1,2], [1,2,3,4]]),
            np.array([[2,3,4,1], [4,1,2,3],[3,4,1,2], [1,2,3,4]]),
            np.array([[1,3,4,2], [4,2,1,3], [3,1,2,4], [2,4,3,1]]),
            np.array([[3,1,4,2], [4,2,3,1], [2,4,1,3], [1,3,2,4]])
        ]
    )