#! /usr/bin/env python3

import time
import ctypes

import cffi

import cutils
import cyutils

MAX_FIBONACCI_N = 34

def fibonacci(n):
    if n < 2:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def python_fibonacci():
    start_ts = time.time()
    python_res = fibonacci(MAX_FIBONACCI_N)
    end_ts = time.time()
    print(f"Time of execution of PYTHON fibonacci's function is {end_ts - start_ts} seconds")
    return python_res

def ctypes_fibonacci():
    mylibc = ctypes.CDLL('./ctypes/mylibc.so')
    mylibc.fibonacci.argstype = [ctypes.c_int]
    mylibc.fibonacci.restype = ctypes.c_int
    start_ts = time.time()
    ctypes_res = mylibc.fibonacci(MAX_FIBONACCI_N)
    end_ts = time.time()
    print(f"Time of execution of CTYPES fibonacci's function is {end_ts - start_ts} seconds")
    return ctypes_res

def cffi_fibonacci():
    ffi = cffi.FFI()
    ffi.cdef('''
    int fibonacci(int n);
    ''')
    ffi.set_source('cffi_utils',
    r'''
    int fibonacci(int n)
    {
        if (n < 2)
            return 1;
        return fibonacci(n-1) + fibonacci(n-2);
    }
    ''')
    ffi.compile()
    from cffi_utils import lib
    start_ts = time.time()
    res = lib.fibonacci(MAX_FIBONACCI_N)
    end_ts = time.time()
    print(f"Time of execution of CFFI fibonacci's function is {end_ts - start_ts} seconds")
    return res

def capi_fibonacci():
    start_ts = time.time()
    res = cutils.fibonacci(MAX_FIBONACCI_N)
    end_ts = time.time()
    print(f"Time of execution of CAPI fibonacci's function is {end_ts - start_ts} seconds")
    return res

def cython_fibonacci():
    start_ts = time.time()
    res = cyutils.fibonacci(MAX_FIBONACCI_N)
    end_ts = time.time()
    print(f"Time of execution of CYTHON fibonacci's function is {end_ts - start_ts} seconds")
    return res

def main():
    python_res = python_fibonacci()
    ctypes_res = ctypes_fibonacci()
    cffi_res = cffi_fibonacci()
    capi_res = capi_fibonacci()
    cython_res = cython_fibonacci()
    assert python_res == ctypes_res == cffi_res == capi_res == cython_res

if __name__ == "__main__":
    main()
