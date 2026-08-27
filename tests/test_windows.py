# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes

from jitasm.utils import ccall
from jitasm.x86_64 import Emitter, R8, R9, RAX, RCX, RDX, RIP, Section, qword_ptr


def test_windows() -> None:
    # Windows x64 passes the first four integer arguments in RCX, RDX, R8, R9.
    e = Emitter()
    e.label('add_two')
    e.mov(RAX, RCX)
    e.add(RAX, RDX)
    e.ret()
    e.finalize()
    assert ccall(e.symbol('add_two'), 20, 22) == 42
    e.unmap()

    e = Emitter()
    e.label('add_four')
    e.mov(RAX, RCX)
    e.add(RAX, RDX)
    e.add(RAX, R8)
    e.add(RAX, R9)
    e.ret()
    e.finalize()
    assert ccall(e.symbol('add_four'), 10, 20, 5, 7) == 42
    e.unmap()

    e = Emitter()
    e.label('read_data')
    e.mov(RAX, qword_ptr(RIP + 'answer'))
    e.ret()
    e.set_section(Section.DATA)
    e.label('answer')
    e.dq(42)
    e.finalize()
    assert ccall(e.symbol('read_data')) == 42
    assert ctypes.string_at(e.symbol('answer'), 8) == b'*\x00\x00\x00\x00\x00\x00\x00'
    e.unmap()
