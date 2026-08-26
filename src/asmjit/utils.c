#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdint.h>

typedef uintptr_t word_t;

static PyObject *
utils_ccall(PyObject *Py_UNUSED(module), PyObject *args) {
    PyObject *address_object;
    PyObject *arguments_object;

    if (!PyArg_ParseTuple(args, "OO:ccall", &address_object, &arguments_object)) {
        return NULL;
    }
    if (!PyLong_Check(address_object)) {
        PyErr_SetString(PyExc_TypeError, "fptr must be an int");
        return NULL;
    }

    void *address = PyLong_AsVoidPtr(address_object);
    if (address == NULL && PyErr_Occurred()) {
        return NULL;
    }
    if (address == NULL) {
        PyErr_SetString(PyExc_ValueError, "fptr must not be zero");
        return NULL;
    }

    PyObject *sequence = PySequence_Fast(arguments_object, "args must be a sequence");
    if (sequence == NULL) {
        return NULL;
    }

    Py_ssize_t count = PySequence_Fast_GET_SIZE(sequence);
    if (count > 32) {
        Py_DECREF(sequence);
        PyErr_SetString(PyExc_ValueError, "ccall supports at most 32 arguments");
        return NULL;
    }

    word_t values[32];
    PyObject **items = PySequence_Fast_ITEMS(sequence);
    for (Py_ssize_t i = 0; i < count; i++) {
        if (!PyLong_Check(items[i])) {
            Py_DECREF(sequence);
            PyErr_Format(PyExc_TypeError, "args[%zd] must be an int", i);
            return NULL;
        }
        values[i] = (word_t)PyLong_AsUnsignedLongLongMask(items[i]);
        if (PyErr_Occurred()) {
            Py_DECREF(sequence);
            return NULL;
        }
    }

#define A(n) values[(n)]
    word_t result;
    switch (count) {
    case 0: result = ((word_t (*)(void))address)(); break;
    case 1: result = ((word_t (*)(word_t))address)(A(0)); break;
    case 2: result = ((word_t (*)(word_t, word_t))address)(A(0), A(1)); break;
    case 3: result = ((word_t (*)(word_t, word_t, word_t))address)(A(0), A(1), A(2)); break;
    case 4: result = ((word_t (*)(word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3)); break;
    case 5: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4)); break;
    case 6: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5)); break;
    case 7: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6)); break;
    case 8: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7)); break;
    case 9: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8)); break;
    case 10: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9)); break;
    case 11: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10)); break;
    case 12: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11)); break;
    case 13: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12)); break;
    case 14: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13)); break;
    case 15: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14)); break;
    case 16: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15)); break;
    case 17: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16)); break;
    case 18: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17)); break;
    case 19: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18)); break;
    case 20: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19)); break;
    case 21: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20)); break;
    case 22: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21)); break;
    case 23: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22)); break;
    case 24: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23)); break;
    case 25: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24)); break;
    case 26: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25)); break;
    case 27: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25), A(26)); break;
    case 28: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25), A(26), A(27)); break;
    case 29: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25), A(26), A(27), A(28)); break;
    case 30: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25), A(26), A(27), A(28), A(29)); break;
    case 31: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25), A(26), A(27), A(28), A(29), A(30)); break;
    case 32: result = ((word_t (*)(word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t, word_t))address)(A(0), A(1), A(2), A(3), A(4), A(5), A(6), A(7), A(8), A(9), A(10), A(11), A(12), A(13), A(14), A(15), A(16), A(17), A(18), A(19), A(20), A(21), A(22), A(23), A(24), A(25), A(26), A(27), A(28), A(29), A(30), A(31)); break;
    default: Py_UNREACHABLE();
    }
#undef A

    Py_DECREF(sequence);
    return PyLong_FromUnsignedLongLong((unsigned long long)result);
}

PyDoc_STRVAR(ccall_doc,
"ccall(fptr, args, /)\n"
"--\n\n"
"Call a function pointer with zero to 32 machine-word integer arguments.");

static PyMethodDef utils_methods[] = {
    {"ccall", utils_ccall, METH_VARARGS, ccall_doc},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef utils_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "asmjit.utils",
    .m_doc = "Utilities implemented in C.",
    .m_size = 0,
    .m_methods = utils_methods
};

PyMODINIT_FUNC
PyInit_utils(void) {
    return PyModuleDef_Init(&utils_module);
}
