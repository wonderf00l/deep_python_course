from random import randint
from itertools import accumulate
from time import time


def matrix_init(size):
    return [
        [
            randint(-10, 10) for _ in range(0, size)
        ]
        for _ in range(0, size)]


def multiply_two_matrix(matrix1, matrix2):
    res = []
    for col in zip(*matrix2):
        new_col = []
        for row in matrix1:
            new_val = 0
            for tup in zip(row, col):
                new_val += tup[0] * tup[1]
            new_col.append(new_val)
        res.append(new_col)
    return list(zip(*res))


def chain_multiply(quantity):
    start = time()
    matrix_list = [matrix_init(5) for _ in range(0, quantity)]
    result = list(accumulate(matrix_list, multiply_two_matrix))[-1]
    end = time()
    for row in result:
        print(row)
    print(f"It took {end - start} seconds")
    return result


chain_multiply(10500)
