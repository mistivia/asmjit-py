# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3


from jitasm.utils import ccall

from jitasm.x86_64 import *


def test_div() -> None:
    e = Emitter()
    e.label('f')
    e.mov(RBX, RDI)
    e.mov(RCX, RSI)
    e.idiv(RBX, RCX)
    e.mov(RAX, RBX)
    e.add(RAX, RCX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 43, 10) == 7
    assert ccall(f, -43, 10) == -7
    assert ccall(f, 43, -10) == -1

    e = Emitter()
    e.label('f')
    e.mov(R8, RDI)
    e.mov(R9, RSI)
    e.div(R8, R9)
    e.mov(RAX, R8)
    e.add(RAX, R9)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 43, 10) == 7

    e = Emitter()
    e.label('f')
    e.mov(RBX, RDI)
    e.mov(RAX, RSI)
    e.idiv(RBX, RAX)
    e.add(RBX, RAX)
    e.mov(RAX, RBX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 43, 10) == 7

    e = Emitter()
    e.label('f')
    e.mov(RBX, RDI)
    e.mov(RDX, RSI)
    e.div(RBX, RDX)
    e.add(RBX, RDX)
    e.mov(RAX, RBX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 43, 10) == 7

    e = Emitter()
    failed = False
    try:
        e.idiv(RBX, RBX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.div(RBX, RBX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.idiv(RDX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.idiv(RAX, RDX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.div(RDX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.div(RAX, RDX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.idiv(EAX, RBX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.div(RAX, RBX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''
