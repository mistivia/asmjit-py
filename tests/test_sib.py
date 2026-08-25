import pytest

from asmjit.x86_64 import *


@pytest.mark.parametrize('sib', [
    Sib(RAX),
    Sib(RAX, RCX, 2, -128),
    Sib(None, R12, 8, (1 << 31) - 1),
    Sib(R13, None, 1, -(1 << 31)),
])
def test_validate_sib_accepts_encodable_addresses(sib: Sib) -> None:
    validate_sib(sib)


@pytest.mark.parametrize('sib', [
    Sib(),
    Sib(EAX),
    Sib(RIP),
    Sib(RAX, ECX),
    Sib(RAX, RIP),
    Sib(RAX, RSP),
    Sib(RAX, RCX, 3),
    Sib(RAX, None, 2),
    Sib(RAX, offset=1 << 31),
    Sib(RAX, offset=-(1 << 31) - 1),
])
def test_validate_sib_rejects_unencodable_addresses(sib: Sib) -> None:
    with pytest.raises(EmitterError):
        validate_sib(sib)


def test_mov_with_sib_encodes_extended_index() -> None:
    e = Emitter()
    e.mov(RAX, Mem(QWORD, Sib(R13, R12, 8, 0x1234)))
    assert e.text == bytes.fromhex('4b 8b 84 e5 34 12 00 00')
