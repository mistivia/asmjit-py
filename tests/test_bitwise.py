
from jitasm.utils import ccall
from jitasm.x86_64 import *


def test_bitwise() -> None:
    e = Emitter()
    e.bitand(RAX, RBX)
    e.bitor(R8, R9)
    e.bitand(R12, 0x12345678)
    e.bitor(R13, -2)
    e.xor(R10, -2)
    e.bitnot(R11)
    assert e.text == (
        b'\x48\x21\xd8'
        b'\x4d\x09\xc8'
        b'\x49\x81\xe4\x78\x56\x34\x12'
        b'\x49\x81\xcd\xfe\xff\xff\xff'
        b'\x49\x81\xf2\xfe\xff\xff\xff'
        b'\x49\x81\xf3\xff\xff\xff\xff'
    )

    e = Emitter()
    e.label('f')
    e.mov(RAX, RDI)
    e.bitand(RAX, RSI)
    e.bitor(RAX, RDX)
    e.xor(RAX, RCX)
    e.bitnot(RAX)
    e.ret()
    e.finalize()
    f = e.symbol('f')
    expected = ~(((0xF0 & 0xCC) | 0x03) ^ 0x55)
    assert ccall(f, 0xF0, 0xCC, 0x03, 0x55) == expected

    e = Emitter()
    failed = False
    try:
        e.bitand(EAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.bitor(RAX, EAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.xor(RIP, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.bitnot(EAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    failed = False
    try:
        e.xor(RAX, 1 << 31)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.bitand(RAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.bitor(RAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.xor(RAX, RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.bitnot(RAX)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''
