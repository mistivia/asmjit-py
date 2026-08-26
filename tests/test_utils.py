import ctypes
from _ctypes import CFuncPtr

from asmjit.utils import ccall


def test_utils() -> None:
    word = ctypes.c_size_t

    def get_42() -> int:
        return 42

    def get_negative_42() -> int:
        return -42

    def add_words(a: int, b: int) -> int:
        return a + b

    def absolute_word(value: int) -> int:
        return abs(value)

    def sum_words(*args: int) -> int:
        return sum(args)

    def address(function: CFuncPtr) -> int:
        value = ctypes.cast(function, ctypes.c_void_p).value
        assert value is not None
        return value

    return_42 = ctypes.CFUNCTYPE(word)(get_42)
    return_negative_42 = ctypes.CFUNCTYPE(ctypes.c_ssize_t)(get_negative_42)
    add = ctypes.CFUNCTYPE(word, word, word)(add_words)
    signed_abs = ctypes.CFUNCTYPE(word, ctypes.c_ssize_t)(absolute_word)
    sum_32 = ctypes.CFUNCTYPE(word, *([word] * 32))(sum_words)

    assert ccall(address(return_42)) == 42
    assert ccall(address(return_negative_42)) == -42
    assert ccall(address(add), 20, 22) == 42
    assert ccall(address(signed_abs), -42) == 42
    assert ccall(address(sum_32), *range(32)) == sum(range(32))

    try:
        _ = ccall(address(return_42), *([0] * 33))
    except ValueError:
        pass
    else:
        raise AssertionError("ccall accepted more than 32 arguments")

    try:
        _ = ccall(address(return_42), "not an int")  # pyright: ignore[reportArgumentType]
    except TypeError:
        pass
    else:
        raise AssertionError("ccall accepted a non-integer argument")
