
from asmjit.utils import ccall

from asmjit.x86_64 import *


def test_label() -> None:
    failed = False
    try:
        _ = Emitter().symbol('value')
    except EmitterError:
        failed = True
    assert failed

    e = Emitter()
    e.label('value')
    failed = False
    try:
        e.label('value')
    except EmitterError:
        failed = True
    assert failed

    e = Emitter()
    e.label('f')
    e.movzx(RAX, byte_ptr(RIP + '.value'))
    e.ret()
    e.set_section(Section.DATA)
    e.label('.value')
    e.db(0x80)
    e.finalize()

    f = e.symbol('f')
    assert ccall(f) == 0x80

    failed = False
    try:
        _ = e.symbol('.value')
    except EmitterError:
        failed = True
    assert failed

    e = Emitter()
    e.label('value')
    e.set_section(Section.DATA)
    failed = False
    try:
        e.label('value')
    except EmitterError:
        failed = True
    assert failed
