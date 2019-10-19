# tester to check constraints
import numpy as np
import math

def test_correctness(solution, n):
    correct = True
    #test rows
    for row in solution:
        if set(row) != set(range(1,n+1)):
            correct = False
    #test cols
    for col in range(n):
        column = [row[col] for row in solution]
        if set(column) != set(range(1,n+1)):
            correct = False
    #test boxes
    box_size = int(math.sqrt(n))
    for i in range(box_size): #row
        for j in range(box_size): #col
            box = solution[i*box_size:i*box_size + box_size]#[j*box_size:j*box_size + box_size]
            elements = []
            for row in box:
                for elem in row[j*box_size: j*box_size + box_size]:
                    elements.append(elem)
            if set(elements) != set(range(1,n+1)):
                correct = False
    return correct


if __name__ == "__main__":
    solution = np.array([[5,6,3,4,7,2,1,9,8], 
                         [2,1,9,3,8,6,7,5,4], 
                         [8,4,7,1,9,5,6,2,3], 
                         [4,7,2,6,3,8,5,1,9], 
                         [9,5,1,2,4,7,3,8,6], 
                         [6,3,8,5,1,9,4,7,2],
                         [7,9,5,8,4,2,3,1,6], 
                         [3,2,4,9,5,1,8,6,7], 
                         [1,8,6,7,2,3,9,4,5]])
    ny_times = np.array([[2,3,4,9,5,6,7,8,1],
                         [8,6,5,2,1,7,4,3,9],
                         [7,1,9,8,3,4,5,6,2],
                         [3,2,8,7,9,5,1,4,6],
                         [1,4,7,3,6,8,9,2,5],
                         [9,5,6,1,4,2,8,7,3],
                         [4,8,1,6,2,9,3,5,7],
                         [6,7,3,5,8,1,2,9,4],
                         [5,9,2,4,7,3,6,1,8]])
    print(test_correctness(ny_times, 9))
    print(test_correctness(solution, 9))

