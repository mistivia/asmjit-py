import ctypes

from asmjit.x86_64 import *


def test_data() -> None:
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

    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0x80
    read_qword = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('read_qword'))
    assert read_qword() == 0x123456789ABCDEF0
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
