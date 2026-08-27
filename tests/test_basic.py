# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3


from jitasm.utils import ccall
from jitasm.x86_64 import *

def test_function_returning_42() -> None:
    e = Emitter()
    # int64_t max(int64_t a, int64_t b)
    (e.label('max'),
        e.mov(rax, rdi),
        e.bge(rdi, rsi, '.done'),
        e.mov(rax, rsi),
     e.label('.done'),
        e.ret())
    e.finalize()
    max_fn_ptr = e.symbol("max")

    assert ccall(max_fn_ptr, 3, 7)   == 7
    assert ccall(max_fn_ptr, 42, -1) == 42
