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
            np.array([[0,2,0,0], [0,0,2,3], [0,4,0,0], [0,0,0,1]]),
            np.array([[4,0,0,0], [2,0,0,1], [0,0,0,2], [1,0,3,0]]),
            np.array([[0,0,0,1], [4,1,0,0], [3,0,0,0], [0,2,0,0]]),
            np.array([[0,0,4,0], [0,2,0,3], [0,0,0,4], [0,0,3,0]]),
            np.array([[3,0,0,0], [0,2,0,0], [0,0,0,3], [0,0,0,4]]),
            np.array([[0,0,2,4], [0,0,0,0], [3,1,0,0], [0,0,0,0]]),
            np.array([[0,1,0,4], [0,0,0,1], [0,4,0,0], [0,3,0,2]]),
            np.array([[0,1,2,4], [0,0,0,0], [1,0,4,0], [0,0,0,0]]),
            np.array([[0,1,2,0], [2,0,0,1], [4,0,0,0], [0,3,0,0]]),
            np.array([[0,1,0,0], [0,0,0,3], [2,0,3,1], [0,0,4,0]])
        ]
    )
