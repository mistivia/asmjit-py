
from jitasm.utils import ccall

from jitasm.x86_64 import *


def test_shift() -> None:
    e = Emitter()
    e.shl(RAX, RBX)
    e.shr(R8, R9)
    e.sar(R10, 7)
    e.ror(R11, 8)
    e.rol(R12, 9)
    assert e.text == (
        b'\x48\x89\xd9\x48\xd3\xe0'
        b'\x4c\x89\xc9\x49\xd3\xe8'
        b'\x49\xc1\xfa\x07'
        b'\x49\xc1\xcb\x08'
        b'\x49\xc1\xc4\x09'
    )

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.shl(RAX, RSI)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 3, 4) == 48

    e = Emitter()
    e.label('f')
    e.mov(R8, RDI)
    e.shr(R8, RSI)
    e.mov(RAX, R8)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 0xF0, 4) == 0x0F

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.sar(RAX, 2)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, -16) == -4

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.ror(RAX, 1)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 2) == 1

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.rol(RAX, RSI)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    assert ccall(f, 1, 63) == -(1 << 63)

    e = Emitter()
    failed = False
    try:
        e.shl(EAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.shr(RAX, EAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.sar(RAX, 1 << 8)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.ror(RAX, 1)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.rol(RAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''
