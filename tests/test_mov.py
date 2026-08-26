import ctypes

from asmjit.x86_64 import *


def test_mov() -> None:
    e = Emitter()
    e.label('f')
    e.mov(R8, 0xFEDCBA9876543210)
    e.mov(RAX, R8)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0xFEDCBA9876543210

    e = Emitter()
    e.label('f')
    e.mov(RAX, (1 << 64) - 1)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == (1 << 64) - 1

    e = Emitter()
    failed = False
    try:
        e.mov(RAX, 1 << 64)
    except EmitterError:
        failed = True
    assert failed
    assert e.text == b''

    e = Emitter()
    e.label('f')
    e.mov(RAX, 0xFEDCBA9876543210)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0xFEDCBA9876543210

    value = ctypes.c_uint64(0xFEDCBA9876543210)
    e = Emitter()
    e.label('f')
    e.mov(RAX, Mem(QWORD, RDI))
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_void_p)(e.symbol('f'))
    assert f(ctypes.addressof(value)) == 0xFEDCBA9876543210

    value = ctypes.c_uint64(0)
    e = Emitter()
    e.label('f')
    e.mov(Mem(QWORD, RDI), RSI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint64)(e.symbol('f'))
    f(ctypes.addressof(value), 0xFEDCBA9876543210)
    assert value.value == 0xFEDCBA9876543210

    value = ctypes.c_uint64(0xFFFFFFFFFFFFFFFF)
    e = Emitter()
    e.label('f')
    e.mov(Mem(DWORD, RDI), RSI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint64)(e.symbol('f'))
    f(ctypes.addressof(value), 0x1234567887654321)
    assert value.value == 0xFFFFFFFF87654321

    value = ctypes.c_uint64(0xFFFFFFFFFFFFFFFF)
    e = Emitter()
    e.label('f')
    e.mov(Mem(WORD, RDI), RSI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint64)(e.symbol('f'))
    f(ctypes.addressof(value), 0x1234567887654321)
    assert value.value == 0xFFFFFFFFFFFF4321

    value = ctypes.c_uint64(0xFFFFFFFFFFFFFFFF)
    e = Emitter()
    e.label('f')
    e.mov(Mem(BYTE, RDI), RSI)
    e.ret()
    e.finalize()
    f = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_uint64)(e.symbol('f'))
    f(ctypes.addressof(value), 0x1234567887654321)
    assert value.value == 0xFFFFFFFFFFFFFF21

    e = Emitter()
    e.label('f')
    e.mov(RAX, Mem(QWORD, Rel('value')))
    e.ret()
    e.set_section(Section.DATA)
    e.label('value')
    e.emit_bytes((0xFEDCBA9876543210).to_bytes(8, 'little'))
    e.finalize()
    f = ctypes.CFUNCTYPE(ctypes.c_uint64)(e.symbol('f'))
    assert f() == 0xFEDCBA9876543210
