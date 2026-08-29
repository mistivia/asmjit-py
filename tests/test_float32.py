# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes

from jitasm.utils import ccall
from jitasm.x86_64 import *


def ccall_f32_2(fptr: int, left: float, right: float) -> float:
    left_value = ctypes.c_float(left)
    right_value = ctypes.c_float(right)
    result = ctypes.c_float()
    _ = ccall(fptr, ctypes.addressof(left_value), ctypes.addressof(right_value), ctypes.addressof(result))
    return result.value


def test_float32() -> None:
    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(RIP + 'value'))
    e.movss(dword_ptr(rdi), xmm0)
    e.ret()
    e.set_section(Section.DATA)
    e.label('value')
    e.dd(0x42280000)
    e.finalize()
    output_value = ctypes.c_float()
    _ = ccall(e.symbol('f'), ctypes.addressof(output_value))
    assert output_value.value == 42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.movss(xmm1, dword_ptr(rsi))
    e.addss(xmm0, xmm1)
    e.movss(dword_ptr(rdx), xmm0)
    e.ret()
    e.finalize()
    assert ccall_f32_2(e.symbol('f'), 20.5, 21.5) == 42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.movss(xmm1, dword_ptr(rsi))
    e.subss(xmm0, xmm1)
    e.movss(dword_ptr(rdx), xmm0)
    e.ret()
    e.finalize()
    assert ccall_f32_2(e.symbol('f'), 50.5, 8.5) == 42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.movss(xmm1, dword_ptr(rsi))
    e.mulss(xmm0, xmm1)
    e.movss(dword_ptr(rdx), xmm0)
    e.ret()
    e.finalize()
    assert ccall_f32_2(e.symbol('f'), 6.0, 7.0) == 42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.movss(xmm1, dword_ptr(rsi))
    e.divss(xmm0, xmm1)
    e.movss(dword_ptr(rdx), xmm0)
    e.ret()
    e.finalize()
    assert ccall_f32_2(e.symbol('f'), 84.0, 2.0) == 42.0

    e = Emitter()
    e.label('f')
    e.cvtsi2ss(xmm0, rdi)
    e.movss(dword_ptr(rsi), xmm0)
    e.ret()
    e.finalize()
    result = ctypes.c_float()
    _ = ccall(e.symbol('f'), -42, ctypes.addressof(result))
    assert result.value == -42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.cvttss2si(rax, xmm0)
    e.ret()
    e.finalize()
    value = ctypes.c_float(-42.9)
    assert ccall(e.symbol('f'), ctypes.addressof(value)) == -42

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.rounds(xmm0, xmm0)
    e.movss(dword_ptr(rsi), xmm0)
    e.ret()
    e.finalize()
    input_value = ctypes.c_float(42.5)
    output_value = ctypes.c_float()
    _ = ccall(e.symbol('f'), ctypes.addressof(input_value), ctypes.addressof(output_value))
    assert output_value.value == 42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.ceils(xmm0, xmm0)
    e.movss(dword_ptr(rsi), xmm0)
    e.ret()
    e.finalize()
    input_value.value = 42.1
    _ = ccall(e.symbol('f'), ctypes.addressof(input_value), ctypes.addressof(output_value))
    assert output_value.value == 43.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.floors(xmm0, xmm0)
    e.movss(dword_ptr(rsi), xmm0)
    e.ret()
    e.finalize()
    input_value.value = -42.1
    _ = ccall(e.symbol('f'), ctypes.addressof(input_value), ctypes.addressof(output_value))
    assert output_value.value == -43.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.truncs(xmm0, xmm0)
    e.movss(dword_ptr(rsi), xmm0)
    e.ret()
    e.finalize()
    input_value.value = -42.9
    _ = ccall(e.symbol('f'), ctypes.addressof(input_value), ctypes.addressof(output_value))
    assert output_value.value == -42.0

    e = Emitter()
    e.label('f')
    e.movss(xmm0, dword_ptr(rdi))
    e.movss(xmm1, dword_ptr(rsi))
    e.bges(xmm0, xmm1, '.true')
    e.mov(rax, 0)
    e.ret()
    e.label('.true')
    e.mov(rax, 1)
    e.ret()
    e.finalize()
    left_value = ctypes.c_float(2.0)
    right_value = ctypes.c_float(2.0)
    assert ccall(e.symbol('f'), ctypes.addressof(left_value), ctypes.addressof(right_value)) == 1
