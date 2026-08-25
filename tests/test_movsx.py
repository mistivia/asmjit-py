import ctypes

from asmjit.x86_64 import *


def test_movsx() -> None:
    e = Emitter()
    e.label('f')
    e.mov(RAX, 0x80)
    e.movsx(RAX, AL)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64)(e.symbol('f'))
    assert f() == -128

    e = Emitter()
    e.label('f')
    e.mov(R8, 0x8001)
    e.movsx(RAX, R8W)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64)(e.symbol('f'))
    assert f() == -32767

    e = Emitter()
    e.label('f')
    e.mov(R10, 0x80000001)
    e.movsx(R9, R10D)
    e.mov(RAX, R9)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64)(e.symbol('f'))
    assert f() == -2147483647

    value8 = ctypes.c_uint8(0x80)
    e = Emitter()
    e.label('f')
    e.movsx(RAX, Mem(BYTE, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(e.symbol('f'))
    assert f(ctypes.addressof(value8)) == -128

    value16 = ctypes.c_uint16(0x8001)
    e = Emitter()
    e.label('f')
    e.movsx(RAX, Mem(WORD, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(e.symbol('f'))
    assert f(ctypes.addressof(value16)) == -32767

    value32 = ctypes.c_uint32(0x80000001)
    e = Emitter()
    e.label('f')
    e.movsx(RAX, Mem(DWORD, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)(e.symbol('f'))
    assert f(ctypes.addressof(value32)) == -2147483647

    e = Emitter()
    e.label('f')
    e.movsx(RAX, Mem(BYTE, Rel('value')))
    e.ret()
    e.set_section(Section.DATA)
    e.label('value')
    e.emit_bytes(b'\x80')
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_int64)(e.symbol('f'))
    assert f() == -128
