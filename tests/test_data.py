# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes

from jitasm.utils import ccall

from jitasm.x86_64 import *


def test_data() -> None:
    e = Emitter()
    e.set_section(Section.DATA)
    e.db(1)
    e.align(8)
    e.dq(0x123456789ABCDEF0)
    e.align(8)
    assert e.data == b'\x01' + b'\x00' * 7 + b'\xf0\xde\xbc\x9a\x78\x56\x34\x12'

    failed = False
    try:
        Emitter().align(8)
    except EmitterError:
        failed = True
    assert failed

    e = Emitter()
    e.set_section(Section.DATA)
    failed = False
    try:
        e.align(0)
    except EmitterError:
        failed = True
    assert failed
    assert e.data == b''

    e = Emitter()
    e.label('f')
    e.movzx(RAX, byte_ptr(RIP + 'bytes'))
    e.ret()

    e.label('read_qword')
    e.mov(RAX, qword_ptr(RIP + 'qwords'))
    e.ret()

    e.set_section(Section.DATA)
    e.label('bytes')
    e.db(0x80, -1)
    e.label('words')
    e.dw(0x1234, 0xABCD, -1)
    e.label('dwords')
    e.dd(0x12345678, 0xABCDEF01, -1)
    e.label('qwords')
    e.dq(0x123456789ABCDEF0, 0xFEDCBA9876543210, -1)
    e.label('text')
    e.ascii('hello')
    e.label('string')
    e.asciz('world')
    e.finalize()

    f = e.symbol('f')
    assert ccall(f) == 0x80
    read_qword = e.symbol('read_qword')
    assert ccall(read_qword) == 0x123456789ABCDEF0
    assert ctypes.string_at(e.symbol('bytes'), 2) == b'\x80\xff'
    assert ctypes.string_at(e.symbol('words'), 6) == b'\x34\x12\xcd\xab\xff\xff'
    assert ctypes.string_at(e.symbol('dwords'), 12) == (
        b'\x78\x56\x34\x12\x01\xef\xcd\xab\xff\xff\xff\xff'
    )
    assert ctypes.string_at(e.symbol('qwords'), 24) == (
        b'\xf0\xde\xbc\x9a\x78\x56\x34\x12'
        b'\x10\x32\x54\x76\x98\xba\xdc\xfe'
        b'\xff\xff\xff\xff\xff\xff\xff\xff'
    )
    assert ctypes.string_at(e.symbol('text'), 5) == b'hello'
    assert ctypes.string_at(e.symbol('string')) == b'world'

    e = Emitter()
    e.label('base')
    e.ret()
    e.label('case1')
    e.ret()
    e.label('case2')
    e.set_section(Section.DATA)
    e.label('table')
    e.dd(('case1', 'base'), ('case2', 'base'))
    e.finalize()

    assert ctypes.string_at(e.symbol('table'), 8) == (
        b'\x01\x00\x00\x00\x02\x00\x00\x00'
    )

    e = Emitter()
    e.label('switch')
    e.lea(RAX, qword_ptr(RIP + '.jump_table'))
    e.movsx(RCX, dword_ptr(RAX + RDI * 4))
    e.add(RAX, RCX)
    e.jmp(RAX)

    e.label('.case0')
    e.mov(RAX, 10)
    e.ret()
    e.label('.case1')
    e.mov(RAX, 20)
    e.ret()
    e.label('.case2')
    e.mov(RAX, 30)
    e.ret()

    e.set_section(Section.DATA)
    e.label('.jump_table')
    e.dd(
        ('.case0', '.jump_table'),
        ('.case1', '.jump_table'),
        ('.case2', '.jump_table'),
    )
    e.finalize()

    switch = e.symbol('switch')
    assert ccall(switch, 0) == 10
    assert ccall(switch, 1) == 20
    assert ccall(switch, 2) == 30
