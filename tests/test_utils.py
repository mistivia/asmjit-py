from asmjit.utils import ccall
from asmjit.x86_64 import R8, R9, R10, RAX, RCX, RDI, RDX, RSI, RSP, Emitter, qword_ptr


def test_utils() -> None:
    emitter = Emitter()

    emitter.label("return_42")
    emitter.mov(RAX, 42)
    emitter.ret()

    emitter.label("return_negative_42")
    emitter.mov(RAX, -42)
    emitter.ret()

    emitter.label("add")
    emitter.mov(RAX, RDI)
    emitter.add(RAX, RSI)
    emitter.ret()

    emitter.label("signed_identity")
    emitter.mov(RAX, RDI)
    emitter.ret()

    emitter.label("sum_32")
    emitter.mov(RAX, RDI)
    for register in (RSI, RDX, RCX, R8, R9):
        emitter.add(RAX, register)
    for offset in range(8, 8 + 26 * 8, 8):
        emitter.mov(R10, qword_ptr(RSP + offset))
        emitter.add(RAX, R10)
    emitter.ret()

    emitter.finalize()
    return_42 = emitter.symbol("return_42")
    return_negative_42 = emitter.symbol("return_negative_42")
    add = emitter.symbol("add")
    signed_identity = emitter.symbol("signed_identity")
    sum_32 = emitter.symbol("sum_32")

    assert ccall(return_42) == 42
    assert ccall(return_negative_42) == -42
    assert ccall(add, 20, 22) == 42
    assert ccall(signed_identity, -42) == -42
    assert ccall(sum_32, *range(32)) == sum(range(32))

    try:
        _ = ccall(return_42, *([0] * 33))
    except ValueError:
        pass
    else:
        raise AssertionError("ccall accepted more than 32 arguments")

    try:
        _ = ccall(return_42, "not an int")  # pyright: ignore[reportArgumentType]
    except TypeError:
        pass
    else:
        raise AssertionError("ccall accepted a non-integer argument")
