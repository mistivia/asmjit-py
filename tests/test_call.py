import ctypes

from asmjit.x86_64 import *


def test_call() -> None:
    e = Emitter()
    e.label('f')
    e.sub(RSP, 8)
    e.call('.answer')
    e.add(RSP, 8)
    e.ret()
    e.label('.answer')
    e.mov(RAX, 42)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 42

    e = Emitter()
    e.call(R8)
    assert e.text == b'\x41\xff\xd0'

    e = Emitter()
    e.label('f')
    e.begin()
    e.mov(R8, RDI)
    e.call(R8)
    e.end()
    e.label('answer')
    e.mov(RAX, 42)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(e.symbol('f'))
    assert f(e.symbol('answer')) == 42

    failed = False
    try:
        Emitter().call(EAX)
    except EmitterError:
        failed = True
    assert failed
