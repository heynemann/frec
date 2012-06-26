#include "extension.h"
#include <numpy/arrayobject.h>

#define EPSILON 2.2204460492503131e-16

static PyObject*
_distance_apply(PyObject *self, PyObject *args)
{
    PyObject *array = NULL, *array2 = NULL, *py_sum = NULL;

    if (!PyArg_UnpackTuple(args, "apply", 2, 2, &array, &array2)) {
        return NULL;
    }

    double *array_data = PyArray_DATA(array);
    double *array_data_2 = PyArray_DATA(array2);
    npy_intp *size = PyArray_DIMS(array);

    double sum = 0;
    int i = 0;
    for (; i < (int)*size; ++i) {
        double array_sum = array_data[i] + array_data_2[i];
        double array_diff = array_data[i] - array_data_2[i];
        sum += (array_diff * array_diff) / (array_sum + EPSILON);
    }

    py_sum = PyFloat_FromDouble(sum);
    Py_INCREF(py_sum);
    return py_sum;
}

EXTENSION_MODULE(_distance,
    "apply(buffer) -> string\n"
    "calculates the chi square distance of two arrays"
)
