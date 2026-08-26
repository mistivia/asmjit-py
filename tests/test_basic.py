
from asmjit.utils import ccall
from asmjit.x86_64 import *

def test_function_returning_42() -> None:
    e = Emitter()
    e.label('f')
    e.mov(RAX, 42)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f) == 42

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.ret()
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''
