
from asmjit.utils import ccall

from asmjit.x86_64 import *


def test_unmap() -> None:
    e = Emitter()

    # Unmapping before finalization, or more than once, is a no-op.
    e.unmap()
    assert e.mapping is None

    e.label('f')
    e.mov(RAX, 42)
    e.ret()
    e.finalize()

    first_mapping = e.mapping
    assert first_mapping is not None
    assert not first_mapping.closed

    e.unmap()
    assert first_mapping.closed
    assert e.mapping is None

    e.unmap()
    assert e.mapping is None

    # The emitter can create and use a fresh mapping after being unmapped.
    e.finalize()
    second_mapping = e.mapping
    assert second_mapping is not None
    assert second_mapping is not first_mapping
    f = e.symbol('f')
    assert ccall(f) == 42

    e.unmap()
    assert second_mapping.closed
