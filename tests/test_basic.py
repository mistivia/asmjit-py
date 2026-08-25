import ctypes
from asmjit.x86_64 import *

def test_function_returning_42() -> None:
    e = Emitter()
    (e.label('f'),
        e.mov(RAX, 42),
        e.ret())
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int)(e.symbol('f'))
    assert f() == 42
