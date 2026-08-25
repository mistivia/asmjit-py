import ctypes
from asmjit.x86_64 import *


def test_movsd() -> None:
    e = Emitter()
    e.label('f')
    e.movsd(XMM0, XMM1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(1.25, -3.5) == -3.5

    e = Emitter()
    e.label('f')
    e.movsd(XMM8, XMM0)
    e.movsd(XMM0, XMM8)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(123.75) == 123.75

    value = ctypes.c_double(-123.75)
    e = Emitter()
    e.label('f')
    e.movsd(XMM0, Mem(QWORD, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_void_p)(e.symbol('f'))
    assert f(ctypes.addressof(value)) == -123.75

    values = (ctypes.c_double * 4)(0.0, 0.0, 0.0, 0.0)
    e = Emitter()
    e.label('f')
    e.movsd(Mem(QWORD, Sib(RDI, RSI, 8, 8)), XMM0)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint64, ctypes.c_double)(e.symbol('f'))
    f(ctypes.addressof(values), 1, -456.25)
    assert values[2] == -456.25
