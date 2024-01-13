#! /usr/bin/env python3

import ctypes

def libc_example():
    libc = ctypes.CDLL('libc.so.6')
    # char* strstr(char *text, char *pattern)
    libc.strstr.argstype = [ctypes.c_char_p, ctypes.c_char_p]
    libc.strstr.restype = ctypes.c_char_p
    #       |
    # t = a b a b a c \0
    # p = b a b a \0
    #     |
    res = libc.strstr(b"ababac", b"baba")
    print(res)

def mylibc_example():
    mylibc = ctypes.CDLL('mylibc.so')
    mylibc.func1.argstype = [ctypes.c_int]
    mylibc.func1.restype = ctypes.c_int
    for num in range(10):
        res = mylibc.func1(num)
        print(f"#{num}: res={res}")

    mylibc.func2.argstype = [ctypes.c_char_p, ctypes.c_int]
    mylibc.func2.restype = ctypes.c_void_p
    mylibc.func2(b"Hello, world", 10)

def main():
    # Используем стандартную библиотеку C.
    libc_example()
    # Используем собственную библиотеку.
    mylibc_example()

if __name__ == "__main__":
    main()
