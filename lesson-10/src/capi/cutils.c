#include <stdlib.h>
#include <stdio.h>

#include <Python.h>

PyObject* cutils_sum(PyObject* self, PyObject* args)
{
    PyObject* list_obj;
    if(!PyArg_ParseTuple(args, "O", &list_obj))
    {
        printf("ERROR: Failed to parse arguments\n");
        // error!
        return NULL;
    }
    long list_len = PyList_Size(list_obj);
    printf("DEBUG: length of list is %ld\n", list_len);
    long res = 0;
    for (long i = 0; i < list_len; ++i)
    {
        PyObject* element = PyList_GetItem(list_obj, i);
        res += PyLong_AsLong(element);
    }
    return Py_BuildValue("l", res);
}

int fibonacci(int n)
{
    if (n < 2)
        return 1;
    return fibonacci(n-1) + fibonacci(n-2);
}

PyObject* cutils_fibonacci(PyObject* self, PyObject* args)
{
    long num;
    if(!PyArg_ParseTuple(args, "l", &num))
    {
        return NULL;
    }
    long res = fibonacci(num);
    PyObject* res_obj = Py_BuildValue("l", res);
    return res_obj;
}

static PyMethodDef methods[] = {
    {"sum", cutils_sum, METH_VARARGS, "Sum of elements of input array."},
    {"fibonacci", cutils_fibonacci, METH_VARARGS, "Returns i'th number of Fibonacci sequence."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cutilsmodule = {
    PyModuleDef_HEAD_INIT,
    "cutils",
    "Module for my first c api code.",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cutils(void)
{
    return PyModule_Create( &cutilsmodule );
}
