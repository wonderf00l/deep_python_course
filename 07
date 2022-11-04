from random import randint
from itertools import accumulate
from time import time

def multiply_matrix(size, quantity):
    matrix_list = []
    for _ in range(0, quantity):
        matrix = []
        for _ in range(0, size):
            matrix.append([
                randint(-50, 50) for _ in range(0, size)
            ])
        print(matrix)
        matrix_list.append(matrix)
    print(matrix_list)


def matrix_init(size):
    return [
        [
            randint(-50, 50) for _ in range(0, size)
        ]
        for _ in range(0, size)]


def multiply_two_matrix(matrix1, matrix2):
    res = []
    for col in zip(*matrix2):
        new_col = []
        for row in matrix1:
            new_val = 0
            for tup in zip(row, col):
                new_val += tup[0]*tup[1]
            new_col.append(new_val)
        res.append(new_col)
    return list(zip(*res))

def chain_multiply(quantity):
    start = time()
    matrix_list = [matrix_init(5) for _ in range(0, quantity)]
    result = list(accumulate(matrix_list, multiply_two_matrix))[-1]
    end = time()
    print(f"It took {end - start} seconds")
    print(result)
    return result

# a = matrix_init(3)
# b = matrix_init(3)
# print(a,"qwer", b)
# # print(list(zip(a, list(zip(*b)))))
# # for row, col in zip(a, list(zip(*b))):
# #     print(row*col, end=' ')
# print(multiply_two_matrix(a, b))
chain_multiply(5)
