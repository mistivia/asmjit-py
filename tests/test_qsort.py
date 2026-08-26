# Copyright (c) 2026, Mistivia <i@mistivia.com>
# Distributed under the terms of the GPLv3

import ctypes
import random

from jitasm.utils import ccall
from jitasm.x86_64 import *


def test_qsort() -> None:
    length = 10_000
    rng = random.Random(42)
    storage = bytearray(length * 8)
    data = memoryview(storage).cast('q')
    for index in range(length):
        data[index] = rng.randint(-(1 << 63), (1 << 63) - 1)
    expected = sorted(data.tolist())

    values = RDI
    count = RSI
    low = RSI
    high = RDX
    i = R8
    j = R9
    pivot = RAX
    value = RCX
    swap = R10

    e = Emitter()

    # void qsort( int64_t *values, uint64_t count)
    # Convert the public (values, count) entry point into
    # qsort_range(values, 0, count - 1).
    e.label('qsort')
    e.begin()
    e.branch(LEU, count, 1, '.qsort_done')
    e.mov(high, count)
    # RSI is no longer count after this point; reuse it as low.
    count = None
    e.sub(high, 1)
    e.mov(low, 0)
    e.call('.qsort_range')

    e.label('.qsort_done')
    e.end()

    # void qsort_range(int64_t *values, uint64_t low, uint64_t high)
    # Arguments remain in RDI, RSI, and RDX for recursive calls.
    e.label('.qsort_range')
    e.begin()

    # An empty or one-element range is already sorted.
    e.branch(GEU, low, high, '.range_done')

    # Lomuto partition using values[high] as the pivot.
    # values[low:i] <= pivot and values[i:j] > pivot.
    e.mov(i, low)
    e.mov(j, low)
    e.mov(pivot, qword_ptr(values + high * 8))

    e.label('.partition')
    e.branch(GE, j, high, '.place_pivot')
    e.mov(value, qword_ptr(values + j * 8))
    e.branch(GT, value, pivot, '.next')

    # values[j] belongs in the lower partition; swap it with values[i].
    e.mov(swap, qword_ptr(values + i * 8))
    e.mov(qword_ptr(values + i * 8), value)
    e.mov(qword_ptr(values + j * 8), swap)
    e.add(i, 1)

    e.label('.next')
    e.add(j, 1)
    e.jmp('.partition')

    # Put the pivot between the two partitions. Its final index is i.
    e.label('.place_pivot')
    e.mov(value, qword_ptr(values + i * 8))
    e.mov(qword_ptr(values + i * 8), pivot)
    e.mov(qword_ptr(values + high * 8), value)

    # Recurse into [low, i - 1]. The recursive call clobbers caller-saved
    # registers, so preserve high and i. Two pushes keep the stack aligned.
    e.branch(GEU, low, i, '.skip_left')
    e.push(high)
    e.push(i)
    e.mov(high, i)
    e.sub(high, 1)
    e.call('.qsort_range')
    e.pop(i)
    e.pop(high)

    # Recurse into [i + 1, high]. Nothing remains live after this call,
    # so high and i do not need to be saved again.
    e.label('.skip_left')
    e.branch(GEU, i, high, '.range_done')
    e.mov(low, i)
    e.add(low, 1)
    e.call('.qsort_range')

    e.label('.range_done')
    e.end()
    e.finalize()

    qsort = e.symbol('qsort')
    address = ctypes.addressof(ctypes.c_char.from_buffer(data))
    _ = ccall(qsort, address, length)

    assert data.tolist() == expected
