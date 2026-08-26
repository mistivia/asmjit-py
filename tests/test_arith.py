import ctypes

from asmjit.x86_64 import *


def test_arith() -> None:
    e = Emitter()
    e.label('f')
    e.add(RDI, RSI)
    e.mov(RAX, RDI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(20, 22) == 42
    assert f(-20, 5) == -15

    e = Emitter()
    e.label('f')
    e.sub(RDI, RSI)
    e.mov(RAX, RDI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(50, 8) == 42
    assert f(-20, 5) == -25

    e = Emitter()
    e.label('f')
    e.add(RDI, 50)
    e.sub(RDI, 8)
    e.mov(RAX, RDI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_int64)(e.symbol('f'))
    assert f(0) == 42
    assert f(-42) == 0

    e = Emitter()
    e.label('f')
    e.push(RDI)
    e.mov(RDI, 0)
    e.pop(RAX)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_uint64)(e.symbol('f'))
    assert f(0x123456789ABCDEF0) == 0x123456789ABCDEF0

    e = Emitter()
    e.label('f')
    e.mov(RAX, RSP)
    e.push(RSP)
    e.pop(RCX)
    e.cset(EQ, RAX, RCX, AL)
    e.movzx(RAX, AL)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 1

    e = Emitter()
    e.add(R8, R9)
    e.sub(R10, -2)
    assert e.text == b'\x4d\x01\xc8\x49\x81\xea\xfe\xff\xff\xff'

    failed = False
    try:
        Emitter().add(EAX, RAX)
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().sub(RAX, 1 << 31)
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().push(EAX)
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        Emitter().pop(RIP)
    except EmitterError:
        failed = True
    assert failed
