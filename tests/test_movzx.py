import ctypes

from asmjit.x86_64 import *


def test_movzx() -> None:
    e = Emitter()
    e.label('f')
    e.mov(RAX, 0xFEDCBA98765432FF)
    e.movzx(RAX, AL)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0xFF

    e = Emitter()
    e.label('f')
    e.mov(R8, 0xFEDCBA987654ABCD)
    e.movzx(RAX, R8W)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0xABCD

    e = Emitter()
    e.label('f')
    e.mov(R10, 0xFEDCBA9887654321)
    e.movzx(R9, R10D)
    e.mov(RAX, R9)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0x87654321

    e = Emitter()
    e.label('f')
    e.movzx(RAX, Mem(BYTE, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(e.symbol('f'))
    value8 = ctypes.c_uint8(0x80)
    assert f(ctypes.addressof(value8)) == 0x80

    e = Emitter()
    e.label('f')
    e.movzx(RAX, Mem(WORD, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(e.symbol('f'))
    value16 = ctypes.c_uint16(0x8001)
    assert f(ctypes.addressof(value16)) == 0x8001

    e = Emitter()
    e.label('f')
    e.movzx(RAX, Mem(DWORD, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(e.symbol('f'))
    value32 = ctypes.c_uint32(0x80000001)
    assert f(ctypes.addressof(value32)) == 0x80000001

    e = Emitter()
    e.label('f')
    e.movzx(RAX, Mem(BYTE, Rel('value')))
    e.ret()
    e.set_section(Section.DATA)
    e.label('value')
    e.emit_bytes(b'\x80')
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0x80
