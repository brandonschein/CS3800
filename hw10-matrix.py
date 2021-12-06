#!/usr/bin/env python3
# # Program to multiply two matrices using nested loops

# # 3x3 matrix
# X = [[1, 2],
#     [1, 3],
#     [6, 2],
#     [5, 1]]
# # 3x4 matrix
# Y = [[3, 6, 1],
#     [-2, 3, 1]]
# # result is 3x4
# result = [[0,0,0],
#          [0,0,0],
#          [0,0,0],
#          [0,0,0]]

# # iterate through rows of X
# for i in range(len(X)):
#    # iterate through columns of Y
#    for j in range(len(Y[0])):
#        # iterate through rows of Y
#        for k in range(len(Y)):
#            result[i][j] += X[i][k] * Y[k][j]

# for r in result:
#    print(r)

import sys
import copy

X = [] # n by m
Y = [] # m by k 
Z = [] # n by k
result = []
# n m k 
def make_matricies(input_arr):
    n, m, k = input_arr[0].split(" ")
    curr = 1
    for i in range(curr, curr + int(n)):
        X.append(list (map(int, input_arr[i].split(" "))))
    curr += int(n)
    for i in range(curr, curr + int(m)):
        Y.append(list (map(int, input_arr[i].split(" "))))
    curr += int(m)
    for i in range(curr, curr + int(n)):
        Z.append(list (map(int, input_arr[i].split(" "))))
    empty_row_matrix = []
    for i in range(int(k)):
        empty_row_matrix.append(0)
    for i in range(int(n)):
        result.append(copy.deepcopy(empty_row_matrix))
    

def calculate_result():
    for i in range(len(X)):
   # iterate through columns of Y
        for j in range(len(Y[0])):
            # iterate through rows of Y
            for k in range(len(Y)):
                result[i][j] += int(X[i][k]) * int(Y[k][j])


################################
input_arr = sys.stdin.read().split("\n ")
input_arr[len(input_arr) - 1] = input_arr[len(input_arr) - 1].split("\n")[0]

#print(input_arr)

make_matricies(input_arr)
#print(X)
#print(Y)
#print(Z)
#print(result)

calculate_result()
#print(result)

if(result == Z):
    print(1)
else:
    print(0)

# printf "4 2 3\n 1 2\n 1 3\n 6 2\n 5 1\n 3 6 1\n -2 3 1\n -1 12 3\n -3 15 4\n 14 42 8\n 13 33 6\n" | make -sf Makefile run-hw10-matrix
