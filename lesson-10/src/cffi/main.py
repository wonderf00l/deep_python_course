#! /usr/bin/env python3

import cffi

def ABI():
    ffi = cffi.FFI()
    lib = ffi.dlopen('./libarea.so')
    ffi.cdef('''
    struct Point
    {
        int x;
        int y;
    };
    int area(struct Point* p1, struct Point* p2);
    int foo();
    char *boo();
    ''')

    p1 = ffi.new('struct Point*')
    p2 = ffi.new('struct Point*')
    p1.x, p1.y = (10, 10)
    p2.x, p2.y = (-2, 2)
    res = lib.area(p1, p2)
    print(res)
    res = lib.foo()
    print(f"foo result is [{res}]")
    res = lib.boo()
    print(f"boo result is [{res}]")

def API():
    ffi = cffi.FFI()
    ffi.cdef('''
    int sum(int* arr, int len);
    int fibonacci(int n);
    ''')
    ffi.set_source('cffi_utils',
    r'''
    int sum(int *arr, int len)
    {
        int res = 0;
        for (int i = 0; i < len; ++i)
        {
            res += arr[i];
        }
        return res;
    }

    int fooboo()
    {
        return 500100;
    }

    int fibonacci(int n)
    {
        if (n < 2)
            return 1;
        return fibonacci(n-1) + fibonacci(n-2);
    }
    ''')
    ffi.compile()
    arr = list(range(1,6))
    c_arr = ffi.new('int []', arr)
    from cffi_utils import lib
    print(lib.sum(c_arr, len(arr)))
    print("==== fibonacci ====")
    print(lib.fibonacci(34))

def main():
    print("==== ABI ===")
    ABI()
    print("==== API ===")
    API()

if __name__ == "__main__":
    main()
