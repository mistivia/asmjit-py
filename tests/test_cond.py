# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes

from jitasm.utils import ccall

from jitasm.x86_64 import *


def ccall_f64_compare(fptr: int, left: float, right: float) -> int:
    left_value = ctypes.c_double(left)
    right_value = ctypes.c_double(right)
    return ccall(fptr, ctypes.addressof(left_value), ctypes.addressof(right_value))


def ccall_f32_compare(fptr: int, left: float, right: float) -> int:
    left_value = ctypes.c_float(left)
    right_value = ctypes.c_float(right)
    return ccall(fptr, ctypes.addressof(left_value), ctypes.addressof(right_value))


def test_cond() -> None:
    e = Emitter()
    e.label('f')
    e.branch(EQ, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2, 2) == 1
    assert ccall(f, 2, 3) == 0

    e = Emitter()
    e.label('f')
    e.branch(NE, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2, 3) == 1
    assert ccall(f, 2, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(GT, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2, -3) == 1
    assert ccall(f, -3, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(GE, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -2, -2) == 1
    assert ccall(f, -3, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(LT, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -3, 2) == 1
    assert ccall(f, 2, -3) == 0

    e = Emitter()
    e.label('f')
    e.branch(LE, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -2, -2) == 1
    assert ccall(f, 2, -3) == 0

    e = Emitter()
    e.label('f')
    e.mov(RAX, 0)
    e.cset(LT, RDI, 0, AL)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -1) == 1
    assert ccall(f, 0) == 0

    e = Emitter()
    e.label('f')
    e.branch(LTU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 0, 1) == 1
    assert ccall(f, 1 << 63, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(LEU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 1) == 1
    assert ccall(f, 2, 1) == 0

    e = Emitter()
    e.label('f')
    e.branch(GTU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1 << 63, 2) == 1
    assert ccall(f, 0, 1) == 0

    e = Emitter()
    e.label('f')
    e.branch(GEU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 1) == 1
    assert ccall(f, 0, 1) == 0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.bltd(XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, -1.5, 2.0) == 1
    assert ccall_f64_compare(f, 2.0, -1.5) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 1

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.bgtd(XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, -1.5) == 1
    assert ccall_f64_compare(f, -1.5, 2.0) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.beqd(XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, 2.0) == 1
    assert ccall_f64_compare(f, 2.0, 3.0) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 1

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.bned(XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, 3.0) == 1
    assert ccall_f64_compare(f, 2.0, 2.0) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.bged(XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, 2.0) == 1
    assert ccall_f64_compare(f, 1.0, 2.0) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.bled(XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, 2.0) == 1
    assert ccall_f64_compare(f, 2.0, 1.0) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 1

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.branchd(P, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, float('nan'), 1.0) == 1
    assert ccall_f64_compare(f, 1.0, 1.0) == 0

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.mov(RAX, 0)
    e.csetd(GT, XMM0, XMM1, AL)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, 1.0) == 1
    assert ccall_f64_compare(f, float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.movss(XMM0, dword_ptr(RDI))
    e.movss(XMM1, dword_ptr(RSI))
    e.mov(RAX, 0)
    e.setlts(XMM0, XMM1, AL)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f32_compare(f, -1.5, 2.0) == 1
    assert ccall_f32_compare(f, 2.0, -1.5) == 0

    e = Emitter()
    e.csets(EQ, XMM8, XMM9, AL)
    e.csetd(EQ, XMM8, XMM9, AL)
    assert e.text == b'\x45\x0f\x2e\xc1\x0f\x94\xc0\x66\x45\x0f\x2e\xc1\x0f\x94\xc0'

    e = Emitter()
    e.cmp(R8, R9)
    e.setcc(P, R8B)
    e.setcc(EQ, SPL)
    assert e.text == b'\x4d\x39\xc8\x41\x0f\x9a\xc0\x40\x0f\x94\xc4'

    e = Emitter()
    e.label('f')
    e.mov(R8, 0)
    e.cmp(RDI, RSI)
    e.setcc(P, R8B)
    e.movzx(RAX, R8B)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 1) == 1
    assert ccall(f, 1, 0) == 0

    e = Emitter()
    e.label('f')
    e.mov(R11, RSP)
    e.cmp(RDI, RSI)
    e.setcc(EQ, SPL)
    e.movzx(RAX, SPL)
    e.mov(RSP, R11)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 42, 42) == 1
    assert ccall(f, 42, 41) == 0

    e = Emitter()
    e.ucomisd(XMM8, XMM9)
    assert e.text == b'\x66\x45\x0f\x2e\xc1'

    e = Emitter()
    e.label('f')
    e.movsd(XMM0, qword_ptr(RDI))
    e.movsd(XMM1, qword_ptr(RSI))
    e.mov(RAX, 0)
    e.movsd(XMM8, XMM0)
    e.movsd(XMM9, XMM1)
    e.ucomisd(XMM8, XMM9)
    e.setcc(GTU, AL)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall_f64_compare(f, 2.0, 1.0) == 1
    assert ccall_f64_compare(f, 1.0, 2.0) == 0
    assert ccall_f64_compare(f, float('nan'), 1.0) == 0

    failed = False
    try:
        Emitter().cmp(EAX, RAX)
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().cmp(RAX, 1 << 31)
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().setcc(EQ, RAX)
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().setcc(EQ, Reg(RegName.RIP, BYTE))
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().branchd(LTU, XMM0, XMM1, '.label')
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().csets(GEU, XMM0, XMM1, AL)
    except EmitterError:
        failed = True
    assert failed
