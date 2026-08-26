import ctypes
from jitasm.utils import ccall
from jitasm.x86_64 import *


def ccall_f64_2(fptr: int, left: float, right: float) -> float:
    left_value = ctypes.c_double(left)
    right_value = ctypes.c_double(right)
    result = ctypes.c_double()
    _ = ccall(fptr, ctypes.addressof(left_value), ctypes.addressof(right_value), ctypes.addressof(result))
    return result.value


def ccall_f64_1(fptr: int, value: float) -> float:
    input_value = ctypes.c_double(value)
    result = ctypes.c_double()
    _ = ccall(fptr, ctypes.addressof(input_value), ctypes.addressof(result))
    return result.value


def test_movsd() -> None:
    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.movsd(XMM0, XMM1)
    e.movsd(qword_ptr(RDX), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_2(f, 1.25, -3.5) == -3.5

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM8, XMM0)
    e.movsd(XMM0, XMM8)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 123.75) == 123.75

    value = ctypes.c_double(-123.75)
    e = Emitter()
    e.label('f')
    e.movsd(XMM0, Mem(QWORD, RDI))
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    result = ctypes.c_double()
    _ = ccall(f, ctypes.addressof(value), ctypes.addressof(result))
    assert result.value == -123.75

    values = (ctypes.c_double * 4)(0.0, 0.0, 0.0, 0.0)
    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDX))
    e.movsd(Mem(QWORD, Sib(RDI, RSI, 8, 8)), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    input_value = ctypes.c_double(-456.25)
    _ = ccall(f, ctypes.addressof(values), 1, ctypes.addressof(input_value))
    assert values[2] == -456.25
