import ctypes

from asmjit.utils import ccall


def test_utils() -> None:
    word = ctypes.c_size_t

    def address(function: ctypes._CFuncPtr) -> int:
        value = ctypes.cast(function, ctypes.c_void_p).value
        assert value is not None
        return value

    return_42 = ctypes.CFUNCTYPE(word)(lambda: 42)
    add = ctypes.CFUNCTYPE(word, word, word)(lambda a, b: a + b)
    sum_32 = ctypes.CFUNCTYPE(word, *([word] * 32))(lambda *args: sum(args))

    assert ccall(address(return_42), []) == 42
    assert ccall(address(add), [20, 22]) == 42
    assert ccall(address(sum_32), list(range(32))) == sum(range(32))

    try:
        ccall(address(return_42), [0] * 33)
    except ValueError:
        pass
    else:
        raise AssertionError("ccall accepted more than 32 arguments")

    try:
        ccall(address(return_42), ["not an int"])
    except TypeError:
        pass
    else:
        raise AssertionError("ccall accepted a non-integer argument")

