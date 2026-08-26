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


def test_float() -> None:
    e = Emitter()
    e.addsd(XMM0, XMM1)
    e.subsd(XMM8, XMM9)
    e.mulsd(XMM10, XMM11)
    e.divsd(XMM12, XMM13)
    e.cvtsi2sd(XMM8, R9)
    e.cvttsd2si(R10, XMM11)
    e.round(XMM0, XMM1)
    e.ceil(XMM8, XMM9)
    e.floor(XMM10, XMM11)
    e.trunc(XMM12, XMM13)
    assert e.text == (
        b'\xf2\x0f\x58\xc1'
        b'\xf2\x45\x0f\x5c\xc1'
        b'\xf2\x45\x0f\x59\xd3'
        b'\xf2\x45\x0f\x5e\xe5'
        b'\xf2\x4d\x0f\x2a\xc1'
        b'\xf2\x4d\x0f\x2c\xd3'
        b'\x66\x0f\x3a\x0b\xc1\x00'
        b'\x66\x45\x0f\x3a\x0b\xc1\x02'
        b'\x66\x45\x0f\x3a\x0b\xd3\x01'
        b'\x66\x45\x0f\x3a\x0b\xe5\x03'
    )

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.addsd(XMM0, XMM1)
    e.movsd(qword_ptr(RDX), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_2(f, 20.5, 21.5) == 42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.subsd(XMM0, XMM1)
    e.movsd(qword_ptr(RDX), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_2(f, 50.5, 8.5) == 42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.mulsd(XMM0, XMM1)
    e.movsd(qword_ptr(RDX), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_2(f, 6.0, 7.0) == 42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.divsd(XMM0, XMM1)
    e.movsd(qword_ptr(RDX), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_2(f, 84.0, 2.0) == 42.0

    e = Emitter()
    e.label('f')
    e.cvtsi2sd(XMM0, RDI)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    result = ctypes.c_double()
    _ = ccall(f, 42, ctypes.addressof(result))
    assert result.value == 42.0
    _ = ccall(f, -42, ctypes.addressof(result))
    assert result.value == -42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.cvttsd2si(RAX, XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    value = ctypes.c_double(42.9)
    assert ccall(f, ctypes.addressof(value)) == 42
    value.value = -42.9
    assert ccall(f, ctypes.addressof(value)) == -42

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.round(XMM0, XMM0)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 42.5) == 42.0
    assert ccall_f64_1(f, 43.5) == 44.0
    assert ccall_f64_1(f, -42.5) == -42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.ceil(XMM0, XMM0)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 42.1) == 43.0
    assert ccall_f64_1(f, -42.9) == -42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.floor(XMM0, XMM0)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 42.9) == 42.0
    assert ccall_f64_1(f, -42.1) == -43.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.trunc(XMM0, XMM0)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 42.9) == 42.0
    assert ccall_f64_1(f, -42.9) == -42.0

    e = Emitter()
    failed = False
    try:
        e.addsd(Xmm(16), XMM0)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.round(Xmm(16), XMM0)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.cvtsi2sd(XMM0, EAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.cvttsd2si(RIP, XMM0)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.divsd(XMM0, XMM1)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.trunc(XMM0, XMM1)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.floor(XMM0, XMM1)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.cvtsi2sd(XMM0, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''
