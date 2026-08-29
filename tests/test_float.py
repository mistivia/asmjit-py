# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

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
    e.roundd(XMM0, XMM0)
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
    e.ceild(XMM0, XMM0)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 42.1) == 43.0
    assert ccall_f64_1(f, -42.9) == -42.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.floord(XMM0, XMM0)
    e.movsd(qword_ptr(RSI), XMM0)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_1(f, 42.9) == 42.0
    assert ccall_f64_1(f, -42.1) == -43.0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.truncd(XMM0, XMM0)
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
        e.roundd(Xmm(16), XMM0)
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
        e.truncd(XMM0, XMM1)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.floord(XMM0, XMM1)
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
