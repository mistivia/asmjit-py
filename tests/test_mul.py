# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3


from jitasm.utils import ccall

from jitasm.x86_64 import *


def test_mul() -> None:
    e = Emitter()
    e.neg(RAX)
    e.neg(R9)
    e.imul(RAX, RBX)
    e.imul(R8, R9)
    e.imul(R10, -2)
    assert e.text == (
        b'\x48\xf7\xd8'
        b'\x49\xf7\xd9'
        b'\x48\x0f\xaf\xc3'
        b'\x4d\x0f\xaf\xc1'
        b'\x4d\x69\xd2\xfe\xff\xff\xff'
    )

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.neg(RAX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 42) == -42
    assert ccall(f, -42) == 42

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.imul(RAX, RSI)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 6, 7) == 42
    assert ccall(f, -6, 7) == -42

    e = Emitter()
    e.label('f')
    e.mov(R8, RDI)
    e.imul(R8, -3)
    e.mov(RAX, R8)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -14) == 42

    e = Emitter()
    failed = False
    try:
        e.neg(EAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.imul(RAX, EAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.imul(RAX, 1 << 31)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.neg(RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.imul(RAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''
