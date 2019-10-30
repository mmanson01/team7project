#!/usr/bin/env python
# dancing links solution
import numpy as np
import math

# each column special node for "column header"...included in column list
# ^ special row ("control row") that has all columns still exist in matrix
# column header can track # of nodes in its column to easily get column w lowest # of nondeterministically

# eliminate by selecting a column and a row in that column
# if column doesnt have any rows, current matrix unsolvable..must be backtracked
# elimination: all columns that have a 1 in the selected row are removed
    # and all rows (including selected row) that contain a 1 in any of the removed columns

# how to remove single column:
    # 1) remove column's header
    # 2) for each row where selected column has a 1, traverese row + remove it from columns
    # 3) repeat for each column where selected row contains a 1
# if matrix has no columns, then they have all been filled and selected rows form the solution
def get_matrix(ny_times_puzzle, universe):
    matrix = []


    return matrix

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
    universe = [1,2,3,4,5,6,7,8,9]
    ny_times_matrix = get_matrix(ny_times_puzzle, universe)
    our_solution = solve(ny_times_puzzle)
    print(np.array_equal(our_solution,ny_times_correct))
