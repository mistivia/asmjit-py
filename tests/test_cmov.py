# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

from jitasm.utils import ccall
from jitasm.x86_64 import *


def test_cmov() -> None:
    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmoveq(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2, 2) == 20
    assert ccall(f, 2, 3) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovne(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2, 3) == 20
    assert ccall(f, 2, 2) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovgt(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2, -3) == 20
    assert ccall(f, -3, 2) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovge(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -2, -2) == 20
    assert ccall(f, -3, 2) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovlt(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -3, 2) == 20
    assert ccall(f, 2, -3) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovle(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -2, -2) == 20
    assert ccall(f, 2, -3) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovgtu(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1 << 63, 2) == 20
    assert ccall(f, 0, 1) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovgeu(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 1) == 20
    assert ccall(f, 0, 1) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovltu(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 0, 1) == 20
    assert ccall(f, 1 << 63, 2) == 10

    e = Emitter()
    e.label('f')
    e.mov(RAX, 10)
    e.mov(RCX, 20)
    e.cmp(RDI, RSI)
    e.cmovleu(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 1) == 20
    assert ccall(f, 2, 1) == 10

    e = Emitter()
    e.label('f')
    e.mov(R8, 10)
    e.mov(R9, 20)
    e.cmp(RDI, RSI)
    e.cmovp(R8, R9)
    e.mov(RAX, R8)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 1) == 20
    assert ccall(f, 1, 0) == 10
