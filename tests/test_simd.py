# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes

from jitasm.utils import ccall
from jitasm.x86_64 import *


def test_simd() -> None:
    source_storage = (ctypes.c_ubyte * 63)()
    result_storage = (ctypes.c_ubyte * 63)()
    source_address = (ctypes.addressof(source_storage) + 31) & ~31
    result_address = (ctypes.addressof(result_storage) + 31) & ~31
    source = (ctypes.c_float * 8).from_address(source_address)
    result = (ctypes.c_float * 8).from_address(result_address)
    source[:] = range(8)

    e = Emitter()
    e.label('f')
    e.vmovaps(ymm0, m256_ptr(rdi))
    e.vmovaps(m256_ptr(rsi), ymm0)
    e.ret()
    e.finalize()
    _ = ccall(e.symbol('f'), source_address, result_address)
    assert list(result) == list(source)

    left = (ctypes.c_float * 8)(*range(8))
    right = (ctypes.c_float * 8)(*range(8, 16))
    result = (ctypes.c_float * 8)()
    e = Emitter()
    e.label('f')
    e.vmovups(ymm0, m256_ptr(rdi))
    e.vmovups(ymm1, m256_ptr(rsi))
    e.vaddps(ymm2, ymm0, ymm1)
    e.vmovups(m256_ptr(rdx), ymm2)
    e.ret()
    e.finalize()
    _ = ccall(
        e.symbol('f'), ctypes.addressof(left), ctypes.addressof(right),
        ctypes.addressof(result),
    )
    expected = [float(i + i + 8) for i in range(8)]
    assert list(result) == expected
