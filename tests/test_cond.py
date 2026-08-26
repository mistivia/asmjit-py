import ctypes

from asmjit.x86_64 import *


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
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(2, 2) == 1
    assert f(2, 3) == 0

    e = Emitter()
    e.label('f')
    e.branch(NE, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(2, 3) == 1
    assert f(2, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(GT, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(2, -3) == 1
    assert f(-3, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(GE, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(-2, -2) == 1
    assert f(-3, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(LT, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(-3, 2) == 1
    assert f(2, -3) == 0

    e = Emitter()
    e.label('f')
    e.branch(LE, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(-2, -2) == 1
    assert f(2, -3) == 0

    e = Emitter()
    e.label('f')
    e.mov(RAX, 0)
    e.cset(LT, RDI, 0, AL)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_int64)(e.symbol('f'))
    assert f(-1) == 1
    assert f(0) == 0

    e = Emitter()
    e.label('f')
    e.branch(LTU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)(e.symbol('f'))
    assert f(0, 1) == 1
    assert f(1 << 63, 2) == 0

    e = Emitter()
    e.label('f')
    e.branch(LEU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)(e.symbol('f'))
    assert f(1, 1) == 1
    assert f(2, 1) == 0

    e = Emitter()
    e.label('f')
    e.branch(GTU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)(e.symbol('f'))
    assert f(1 << 63, 2) == 1
    assert f(0, 1) == 0

    e = Emitter()
    e.label('f')
    e.branch(GEU, RDI, RSI, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64)(e.symbol('f'))
    assert f(1, 1) == 1
    assert f(0, 1) == 0

    e = Emitter()
    e.label('f')
    e.branch(LT, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(-1.5, 2.0) == 1
    assert f(2.0, -1.5) == 0
    assert f(float('nan'), 1.0) == 1

    e = Emitter()
    e.label('f')
    e.branch(GT, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(2.0, -1.5) == 1
    assert f(-1.5, 2.0) == 0
    assert f(float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.branch(EQ, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(2.0, 2.0) == 1
    assert f(2.0, 3.0) == 0
    assert f(float('nan'), 1.0) == 1

    e = Emitter()
    e.label('f')
    e.branch(NE, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(2.0, 3.0) == 1
    assert f(2.0, 2.0) == 0
    assert f(float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.branch(GE, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(2.0, 2.0) == 1
    assert f(1.0, 2.0) == 0
    assert f(float('nan'), 1.0) == 0

    e = Emitter()
    e.label('f')
    e.branch(LE, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(2.0, 2.0) == 1
    assert f(2.0, 1.0) == 0
    assert f(float('nan'), 1.0) == 1

    e = Emitter()
    e.label('f')
    e.branch(P, XMM0, XMM1, '.true')
    e.mov(RAX, 0)
    e.ret()
    e.label('.true')
    e.mov(RAX, 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(float('nan'), 1.0) == 1
    assert f(1.0, 1.0) == 0

    e = Emitter()
    e.label('f')
    e.mov(RAX, 0)
    e.cset(GT, XMM0, XMM1, AL)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_double, ctypes.c_double)(e.symbol('f'))
    assert f(2.0, 1.0) == 1
    assert f(float('nan'), 1.0) == 0

    e = Emitter()
    e.cmp(R8, R9)
    e.setcc(P, R8B)
    e.setcc(EQ, SPL)
    assert e.text == b'\x4d\x39\xc8\x41\x0f\x9a\xc0\x40\x0f\x94\xc4'

    e = Emitter()
    e.ucomisd(XMM8, XMM9)
    assert e.text == b'\x66\x45\x0f\x2e\xc1'

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
        Emitter().branch(LTU, XMM0, XMM1, '.label')
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().cset(GEU, XMM0, XMM1, AL)
    except EmitterError:
        failed = True
    assert failed
