import ctypes
from asmjit.asmjit import *


def test_function_returning_42() -> None:
    e = Emitter()

    e.label("f")
    e.mov(RAX, 42)
    e.ret()
    symbols = e.finalize()

    f = ctypes.CFUNCTYPE(ctypes.c_int)(symbols["f"])
    assert f() == 42
