import ctypes

from asmjit.x86_64 import *


def test_sib() -> None:
    value = ctypes.c_uint64(0xFEDCBA9876543210)

    e = Emitter()
    e.label('f')
    e.mov(RAX, Mem(QWORD, Sib(RDI)))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(e.symbol('f'))
    assert f(ctypes.addressof(value)) == 0xFEDCBA9876543210

    values = (ctypes.c_uint64 * 4)(11, 22, 33, 44)

    e = Emitter()
    e.label('f')
    e.mov(RAX, Mem(QWORD, Sib(RDI, RSI, 8, 8)))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p, ctypes.c_uint64)(e.symbol('f'))
    assert f(ctypes.addressof(values), 1) == 33

    e = Emitter()
    e.label('f')
    e.mov(R8, RDI)
    e.mov(R9, RSI)
    e.mov(RAX, Mem(QWORD, Sib(R8, R9, 8, -8)))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p, ctypes.c_uint64)(e.symbol('f'))
    assert f(ctypes.addressof(values), 2) == 22

    failed = False
    try:
        validate_sib(Sib())
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        validate_sib(Sib(EAX))
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        validate_sib(Sib(RIP))
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        validate_sib(Sib(RAX, RSP))
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        validate_sib(Sib(RAX, RCX, 3))
    except EmitterError:
        failed = True
    assert failed

    failed = False
    try:
        validate_sib(Sib(RAX, offset=1 << 31))
    except EmitterError:
        failed = True
    assert failed
