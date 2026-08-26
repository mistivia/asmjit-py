
from jitasm.utils import ccall
from jitasm.x86_64 import *

def test_function_returning_42() -> None:
    e = Emitter()

    (e.label("f"),
        e.mov(RAX, 42),
        e.ret())

    e.finalize()

    assert ccall(e.symbol('f')) == 42
