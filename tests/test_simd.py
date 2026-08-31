# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes

from jitasm.utils import ccall
from jitasm.x86_64 import *


def simd_move() -> None:
    source_storage = (ctypes.c_ubyte * 95)()
    result_storage = (ctypes.c_ubyte * 95)()
    source_address = (ctypes.addressof(source_storage) + 31) & ~31
    result_address = (ctypes.addressof(result_storage) + 31) & ~31
    assert source_address % 32 == 0
    assert result_address % 32 == 0
    source = (ctypes.c_float * 16).from_address(source_address)
    result = (ctypes.c_float * 16).from_address(result_address)
    source[:] = range(16)

    e = Emitter()
    e.label('f')
    e.vmovaps(ymm0, m256_ptr(rdi))
    e.vmovaps(ymm1, ymm0)
    e.vmovaps(m256_ptr(rsi), ymm1)
    e.vmovaps(xmm2, m128_ptr(rdi))
    e.vmovaps(xmm3, xmm2)
    e.vmovaps(m128_ptr(rsi), xmm3)
    e.vmovaps(ymm4, m256_ptr(rdi + rdx * 8))
    e.vmovaps(m256_ptr(rsi + rcx * 8), ymm4)
    e.ret()
    e.finalize()
    _ = ccall(e.symbol('f'), source_address, result_address, 4, 4)
    assert list(result) == list(source)

    result[:] = [0.0] * 16
    e = Emitter()
    e.label('f')
    e.vmovaps(ymm0, m256_ptr(RIP + 'value'))
    e.vmovaps(m256_ptr(rdi), ymm0)
    e.vmovaps(xmm1, m128_ptr(RIP + 'value128'))
    e.vmovaps(m128_ptr(rdi + 32), xmm1)
    e.ret()
    e.set_section(Section.DATA)
    e.align(32)
    e.label('value')
    e.dd(0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
    e.label('value128')
    e.dd(8.0, 9.0, 10.0, 11.0)
    e.finalize()
    _ = ccall(e.symbol('f'), result_address)
    assert list(result[:12]) == [float(i) for i in range(12)]


def simd_arithmetic() -> None:
    left = (ctypes.c_float * 8)(*range(1, 9))
    right = (ctypes.c_float * 8)(*range(9, 17))
    add_result = (ctypes.c_float * 8)()
    sub_result = (ctypes.c_float * 8)()
    mul_result = (ctypes.c_float * 8)()
    div_result = (ctypes.c_float * 8)()
    e = Emitter()
    e.label('f')
    e.vmovups(ymm0, m256_ptr(rdi))
    e.vmovups(ymm1, m256_ptr(rsi))
    e.vaddps(ymm2, ymm0, ymm1)
    e.vmovups(m256_ptr(rdx), ymm2)
    e.vsubps(ymm3, ymm1, ymm0)
    e.vmovups(m256_ptr(rcx), ymm3)
    e.vmulps(ymm4, ymm0, ymm1)
    e.vmovups(m256_ptr(r8), ymm4)
    e.vdivps(ymm5, ymm1, ymm0)
    e.vmovups(m256_ptr(r9), ymm5)
    e.ret()
    e.finalize()
    _ = ccall(
        e.symbol('f'), ctypes.addressof(left), ctypes.addressof(right),
        ctypes.addressof(add_result), ctypes.addressof(sub_result),
        ctypes.addressof(mul_result), ctypes.addressof(div_result),
    )
    assert list(add_result) == [float(i + i + 10) for i in range(8)]
    assert list(sub_result) == [8.0] * 8
    assert list(mul_result) == [float((i + 1) * (i + 9)) for i in range(8)]
    assert list(div_result) == [ctypes.c_float((i + 9) / (i + 1)).value for i in range(8)]

    xmm_result = (ctypes.c_float * 16)()
    e = Emitter()

    e.label('f')
    (
        e.vmovups(xmm0, m128_ptr(rdi)),
        e.vmovups(xmm1, m128_ptr(rsi)),
        e.vaddps(xmm2, xmm0, xmm1),
        e.vmovups(m128_ptr(rdx), xmm2),
        e.vsubps(xmm3, xmm1, xmm0),
        e.vmovups(m128_ptr(rdx + 16), xmm3),
        e.vmulps(xmm4, xmm0, xmm1),
        e.vmovups(m128_ptr(rdx + 32), xmm4),
        e.vdivps(xmm5, xmm1, xmm0),
        e.vmovups(m128_ptr(rdx + 48), xmm5),
        e.ret(),
    )

    e.finalize()
    _ = ccall(
        e.symbol('f'), ctypes.addressof(left), ctypes.addressof(right),
        ctypes.addressof(xmm_result),
    )
    assert list(xmm_result[:4]) == [float(i + i + 10) for i in range(4)]
    assert list(xmm_result[4:8]) == [8.0] * 4
    assert list(xmm_result[8:12]) == [float((i + 1) * (i + 9)) for i in range(4)]
    assert list(xmm_result[12:]) == [ctypes.c_float((i + 9) / (i + 1)).value for i in range(4)]


def simd_min_max_sqrt() -> None:
    packed_left = (ctypes.c_float * 8)(1.0, 4.0, 9.0, 16.0, 25.0, 36.0, 49.0, 64.0)
    packed_right = (ctypes.c_float * 8)(8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0)
    packed_result = (ctypes.c_float * 36)()
    e = Emitter()
    e.label('f')
    e.vmovups(ymm0, m256_ptr(rdi))
    e.vmovups(ymm1, m256_ptr(rsi))
    e.vsqrtps(ymm2, ymm0)
    e.vmovups(m256_ptr(rdx), ymm2)
    e.vmaxps(ymm3, ymm0, ymm1)
    e.vmovups(m256_ptr(rdx + 32), ymm3)
    e.vminps(ymm4, ymm0, ymm1)
    e.vmovups(m256_ptr(rdx + 64), ymm4)
    e.vsqrtps(xmm2, xmm0)
    e.vmovups(m128_ptr(rdx + 96), xmm2)
    e.vmaxps(xmm3, xmm0, xmm1)
    e.vmovups(m128_ptr(rdx + 112), xmm3)
    e.vminps(xmm4, xmm0, xmm1)
    e.vmovups(m128_ptr(rdx + 128), xmm4)
    e.ret()
    e.finalize()
    _ = ccall(
        e.symbol('f'), ctypes.addressof(packed_left), ctypes.addressof(packed_right),
        ctypes.addressof(packed_result),
    )

    expected_sqrt = [float(i) for i in range(1, 9)]
    expected_max = [max(left, right) for left, right in zip(packed_left, packed_right)]
    expected_min = [min(left, right) for left, right in zip(packed_left, packed_right)]
    assert list(packed_result[:8]) == expected_sqrt
    assert list(packed_result[8:16]) == expected_max
    assert list(packed_result[16:24]) == expected_min
    assert list(packed_result[24:28]) == expected_sqrt[:4]
    assert list(packed_result[28:32]) == expected_max[:4]
    assert list(packed_result[32:36]) == expected_min[:4]


def simd_bitwise() -> None:
    bitwise_left = (ctypes.c_uint32 * 8)(
        0xffffffff, 0x00000000, 0xaaaaaaaa, 0x55555555,
        0x12345678, 0x87654321, 0x7f800000, 0x80000000,
    )
    bitwise_right = (ctypes.c_uint32 * 8)(
        0x0f0f0f0f, 0xf0f0f0f0, 0x55555555, 0xaaaaaaaa,
        0xffffffff, 0x00000000, 0x007fffff, 0x7fffffff,
    )
    bitwise_result = (ctypes.c_uint32 * 24)()
    e = Emitter()
    e.label('f')
    e.vmovups(ymm0, m256_ptr(rdi))
    e.vmovups(ymm1, m256_ptr(rsi))
    e.vandps(ymm2, ymm0, ymm1)
    e.vmovups(m256_ptr(rdx), ymm2)
    e.vorps(ymm3, ymm0, ymm1)
    e.vmovups(m256_ptr(rdx + 32), ymm3)
    e.vandps(xmm2, xmm0, xmm1)
    e.vmovups(m128_ptr(rdx + 64), xmm2)
    e.vorps(xmm3, xmm0, xmm1)
    e.vmovups(m128_ptr(rdx + 80), xmm3)
    e.ret()
    e.finalize()
    _ = ccall(
        e.symbol('f'), ctypes.addressof(bitwise_left), ctypes.addressof(bitwise_right),
        ctypes.addressof(bitwise_result),
    )

    expected_and = [left & right for left, right in zip(bitwise_left, bitwise_right)]
    expected_or = [left | right for left, right in zip(bitwise_left, bitwise_right)]
    assert list(bitwise_result[:8]) == expected_and
    assert list(bitwise_result[8:16]) == expected_or
    assert list(bitwise_result[16:20]) == expected_and[:4]
    assert list(bitwise_result[20:24]) == expected_or[:4]


def test_simd() -> None:
    simd_move()
    simd_arithmetic()
    simd_min_max_sqrt()
    simd_bitwise()
