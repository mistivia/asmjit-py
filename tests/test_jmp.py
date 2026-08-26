
from asmjit.utils import ccall

from asmjit.x86_64 import *


def test_jmp() -> None:
    e = Emitter()
    e.label('f')
    e.jmp('.answer')
    e.mov(RAX, 0)
    e.ret()
    e.label('.answer')
    e.mov(RAX, 42)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f) == 42

    e = Emitter()
    e.label('f')
    e.mov(R8, RDI)
    e.jmp(R8)
    e.label('answer')
    e.mov(RAX, 42)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, e.symbol('answer')) == 42

    e = Emitter()
    e.jmp(R8)
    assert e.text == b'\x41\xff\xe0'

    failed = False
    try:
        Emitter().jmp(EAX)
    except EmitterError:
        failed = True
    assert failed
