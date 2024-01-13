#! /usr/bin/env python3

import cutils

def main():
    arr = list(range(1,6))
    res = cutils.sum(arr)
    print(res)
    res = cutils.fibonacci(10)
    print(res)

if __name__ == "__main__":
    main()
