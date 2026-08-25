import ctypes
import mmap
from dataclasses import dataclass
from enum import Enum
from typing import overload

class WordSize(Enum):
    BYTE  = 8
    WORD  = 16
    DWORD = 32
    QWORD = 64

BYTE = WordSize.BYTE
WORD = WordSize.WORD
DWORD = WordSize.DWORD
QWORD = WordSize.QWORD

class RegName(Enum):
    RAX = 'rax'
    RBX = 'rbx'
    RCX = 'rcx'
    RDX = 'rdx'
    RDI = 'rdi'
    RSI = 'rsi'
    RBP = 'rbp'
    RSP = 'rsp'
    RIP = 'rip'
    R8  = 'r8'
    R9  = 'r9'
    R10 = 'r10'
    R11 = 'r11'
    R12 = 'r12'
    R13 = 'r13'
    R14 = 'r14'
    R15 = 'r15'

@dataclass
class Reg:
    name: RegName
    size: WordSize

class EmitterError(RuntimeError):
    pass

RAX = Reg(RegName.RAX, QWORD)
RBX = Reg(RegName.RBX, QWORD)
RCX = Reg(RegName.RCX, QWORD)
RDX = Reg(RegName.RDX, QWORD)
RDI = Reg(RegName.RDI, QWORD)
RSI = Reg(RegName.RSI, QWORD)
RBP = Reg(RegName.RBP, QWORD)
RSP = Reg(RegName.RSP, QWORD)
RIP = Reg(RegName.RIP, QWORD)
R8  = Reg(RegName.R8,  QWORD)
R9  = Reg(RegName.R9,  QWORD)
R10 = Reg(RegName.R10, QWORD)
R11 = Reg(RegName.R11, QWORD)
R12 = Reg(RegName.R12, QWORD)
R13 = Reg(RegName.R13, QWORD)
R14 = Reg(RegName.R14, QWORD)
R15 = Reg(RegName.R15, QWORD)

EAX = Reg(RegName.RAX, DWORD)
EBX = Reg(RegName.RBX, DWORD)
ECX = Reg(RegName.RCX, DWORD)
EDX = Reg(RegName.RDX, DWORD)
EDI = Reg(RegName.RDI, DWORD)
ESI = Reg(RegName.RSI, DWORD)
EBP = Reg(RegName.RBP, DWORD)
ESP = Reg(RegName.RSP, DWORD)
R8D = Reg(RegName.R8,  DWORD)
R9D = Reg(RegName.R9,  DWORD)
R10D = Reg(RegName.R10, DWORD)
R11D = Reg(RegName.R11, DWORD)
R12D = Reg(RegName.R12, DWORD)
R13D = Reg(RegName.R13, DWORD)
R14D = Reg(RegName.R14, DWORD)
R15D = Reg(RegName.R15, DWORD)

AX = Reg(RegName.RAX, WORD)
BX = Reg(RegName.RBX, WORD)
CX = Reg(RegName.RCX, WORD)
DX = Reg(RegName.RDX, WORD)
DI = Reg(RegName.RDI, WORD)
SI = Reg(RegName.RSI, WORD)
BP = Reg(RegName.RBP, WORD)
SP = Reg(RegName.RSP, WORD)
R8W = Reg(RegName.R8,  WORD)
R9W = Reg(RegName.R9,  WORD)
R10W = Reg(RegName.R10, WORD)
R11W = Reg(RegName.R11, WORD)
R12W = Reg(RegName.R12, WORD)
R13W = Reg(RegName.R13, WORD)
R14W = Reg(RegName.R14, WORD)
R15W = Reg(RegName.R15, WORD)

AL = Reg(RegName.RAX, BYTE)
BL = Reg(RegName.RBX, BYTE)
CL = Reg(RegName.RCX, BYTE)
DL = Reg(RegName.RDX, BYTE)
DIL = Reg(RegName.RDI, BYTE)
SIL = Reg(RegName.RSI, BYTE)
BPL = Reg(RegName.RBP, BYTE)
SPL = Reg(RegName.RSP, BYTE)
R8B = Reg(RegName.R8,  BYTE)
R9B = Reg(RegName.R9,  BYTE)
R10B = Reg(RegName.R10, BYTE)
R11B = Reg(RegName.R11, BYTE)
R12B = Reg(RegName.R12, BYTE)
R13B = Reg(RegName.R13, BYTE)
R14B = Reg(RegName.R14, BYTE)
R15B = Reg(RegName.R15, BYTE)

REG_IDS = {
    RegName.RAX: 0,  RegName.RCX: 1,  RegName.RDX: 2,  RegName.RBX: 3,
    RegName.RSP: 4,  RegName.RBP: 5,  RegName.RSI: 6,  RegName.RDI: 7,
    RegName.R8:  8,  RegName.R9:  9,  RegName.R10: 10, RegName.R11: 11,
    RegName.R12: 12, RegName.R13: 13, RegName.R14: 14, RegName.R15: 15,
}

def reg_id(reg: Reg) -> int:
    return REG_IDS[reg.name]

def signed_bytes(value: int, size: int) -> bytes | None:
    min_value = -(1 << (size * 8 - 1))
    max_value = (1 << (size * 8 - 1)) - 1
    if value < min_value or value > max_value:
        return None
    return value.to_bytes(size, 'little', signed=True)

@dataclass
class Xmm:
    id: int

XMM0 = Xmm(0)
XMM1 = Xmm(1)
XMM2 = Xmm(2)
XMM3 = Xmm(3)
XMM4 = Xmm(4)
XMM5 = Xmm(5)
XMM6 = Xmm(6)
XMM7 = Xmm(7)
XMM8 = Xmm(8)
XMM9 = Xmm(9)
XMM10 = Xmm(10)
XMM11 = Xmm(11)
XMM12 = Xmm(12)
XMM13 = Xmm(13)
XMM14 = Xmm(14)
XMM15 = Xmm(15)

@dataclass
class Sib: # r64 + r64 * scale + offset
    base: Reg | None = None
    index: Reg | None = None
    scale: int = 1
    offset: int = 0

def validate_sib(sib: Sib) -> None:
    if sib.scale not in (1, 2, 4, 8):
        raise EmitterError('invalid SIB scale')
    if signed_bytes(sib.offset, 4) is None:
        raise EmitterError('invalid SIB displacement')
    if sib.base is None and sib.index is None:
        raise EmitterError('SIB must have a base or index register')
    if sib.base is not None and (sib.base.size != QWORD or sib.base.name == RegName.RIP):
        raise EmitterError('invalid SIB base register')
    if sib.index is not None and (sib.index.size != QWORD or sib.index.name == RegName.RIP):
        raise EmitterError('invalid SIB index register')
    if sib.index is not None and sib.index.name == RegName.RSP:
        raise EmitterError('rsp cannot be used as a SIB index register')
    if sib.index is None and sib.scale != 1:
        raise EmitterError('SIB scale requires an index register')

@dataclass
class Rel: # relative to rip
    label: str

@dataclass
class Mem:
    size: WordSize
    addr: Reg | Sib | Rel

class Section(Enum):
    TEXT  = 'text'
    DATA  = 'data'

@dataclass
class LabelRef:
    position: int
    rip: int

# str is label, int and float is imm
type Operand = Reg | Mem | Xmm | int | float | str

class Emitter:
    def __init__(self):
        self.text: bytearray = bytearray(b'')
        self.data: bytearray = bytearray(b'')
        self.section: Section = Section.TEXT
        self.labels: dict[str, tuple[Section, int]] = {}
        self.label_refs: dict[str, list[LabelRef]] ={}
        self.mapping: mmap.mmap | None = None
        self.symbols: dict[str, int] | None

    def add_label_ref(self, name:str, pos: int, rip: int) -> None:
        self.label_refs.setdefault(name, []).append(LabelRef(pos, rip))

    def symbol(self, s: str) -> int:
        if self.symbols is None or s not in self.symbols:
            raise EmitterError('symbol not found')
        return self.symbols[s]

    def emit_bytes(self, b: bytes):
        if self.section == Section.TEXT:
            self.text.extend(b)
        if self.section == Section.DATA:
            self.data.extend(b)

    def label(self, name: str) -> None:
        if self.section == Section.TEXT:
            self.labels[name] = (Section.TEXT, self.section_offset())
        elif self.section == Section.DATA:
            self.labels[name] = (Section.DATA, self.section_offset())
        else:
            raise EmitterError('invalid section')

    def set_section(self, s: Section):
        self.section = s

    def section_offset(self) -> int:
        if self.section == Section.TEXT:
            return len(self.text)
        return len(self.data)

    def emit_mem_op(
        self,
        reg: Reg,
        mem: Mem,
        opcode: bytes,
        rex_w: bool,
        legacy_prefix: bytes = b'',
    ) -> None:
        reg_field = reg_id(reg)
        rex = (0x48 if rex_w else 0x40) | ((reg_field >> 3) << 2)
        suffix = bytearray()
        label_name: str | None = None

        match mem.addr:
            case Reg() as base:
                if base == RIP or base.size != QWORD:
                    raise EmitterError('invalid base register type')
                base_id = reg_id(base)
                rex |= base_id >> 3
                rm = base_id & 7
                if rm == 4:
                    mod_rm = ((reg_field & 7) << 3) | 4
                    suffix.append(0x20 | rm)
                elif rm == 5:
                    mod_rm = 0x40 | ((reg_field & 7) << 3) | rm
                    suffix.append(0)
                else:
                    mod_rm = ((reg_field & 7) << 3) | rm

            case Rel(label):
                mod_rm = ((reg_field & 7) << 3) | 5
                suffix.extend(b'\x00\x00\x00\x00')
                label_name = label

            case Sib(base, index, scale, offset):
                validate_sib(mem.addr)
                if index is None:
                    index_bits = 4
                else:
                    index_id = reg_id(index)
                    index_bits = index_id & 7
                    rex |= (index_id >> 3) << 1

                scale_bits = {1: 0, 2: 1, 4: 2, 8: 3}[scale]
                if base is None:
                    displacement = signed_bytes(offset, 4)
                    if displacement is None:
                        raise EmitterError('invalid displacement')
                    mod = 0
                    base_bits = 5
                else:
                    base_id = reg_id(base)
                    base_bits = base_id & 7
                    rex |= base_id >> 3
                    if offset == 0 and base_bits != 5:
                        mod = 0
                        displacement = b''
                    else:
                        displacement = signed_bytes(offset, 1)
                        if displacement is not None:
                            mod = 1
                        else:
                            displacement = signed_bytes(offset, 4)
                            if displacement is None:
                                raise EmitterError('invalid displacement')
                            mod = 2

                mod_rm = (mod << 6) | ((reg_field & 7) << 3) | 4
                suffix.insert(0, (scale_bits << 6) | (index_bits << 3) | base_bits)
                suffix.extend(displacement)

        emit_rex = rex != 0x40 or (mem.size == BYTE and reg_field >= 4)
        rex_prefix = bytes((rex,)) if emit_rex else b''
        instruction_start = self.section_offset()
        self.emit_bytes(legacy_prefix + rex_prefix + opcode + bytes((mod_rm,)) + suffix)
        if label_name is not None:
            disp_pos = instruction_start + len(legacy_prefix) + len(rex_prefix) + len(opcode) + 1
            self.add_label_ref(label_name, disp_pos, len(self.text))

    def emit_mov_mem(self, op1: Reg | Mem, op2: Reg | Mem) -> None:
        match (op1, op2):
            case (Reg() as reg, Mem() as mem):
                opcode = b'\x8b'
            case (Mem() as mem, Reg() as reg):
                opcode = b'\x88' if mem.size == BYTE else b'\x89'
            case _:
                raise EmitterError("op type error in emit_mov_mem")

        legacy_prefix = b'\x66' if mem.size == WORD else b''
        self.emit_mem_op(reg, mem, opcode, mem.size == QWORD, legacy_prefix)

    def mov(self, op1: Operand, op2: Operand) -> None:
        if self.section == Section.DATA:
            raise EmitterError('mov: cannot emit code at data section')
        match(op1, op2):
            case (Reg(), Reg()):
                if op1 == RIP or op2 == RIP or op1.size != QWORD or op2.size != QWORD:
                    raise EmitterError('mov: register must be qword and cannot be rip')
                dst = reg_id(op1)
                src = reg_id(op2)
                rex = 0x48 | ((src >> 3) << 2) | (dst >> 3)
                mod_rm = 0xC0 | ((src & 7) << 3) | (dst & 7)
                self.emit_bytes(bytes((rex, 0x89, mod_rm)))
            case (Reg(), int()):
                if op1 == RIP or op1.size != QWORD or not -(1 << 63) <= op2 < (1 << 65):
                    raise EmitterError('mov: register must be qword and cannot be rip, imm must be 64 bit number')
                dst = reg_id(op1)
                rex = 0x48 | (dst >> 3)
                immediate = (op2 & ((1 << 64) - 1)).to_bytes(8, 'little')
                self.emit_bytes(bytes((rex, 0xB8 | (dst & 7))) + immediate)
            case (Reg(), Mem()):
                if op1 == RIP or op1.size != QWORD or op2.size != QWORD:
                    raise EmitterError('mov: register must be qword and cannot be rip')
                self.emit_mov_mem(op1, op2)
            case (Mem(), Reg()):
                if op2 == RIP or op2.size != QWORD:
                    raise EmitterError('mov: register must be qword and cannot be rip')
                self.emit_mov_mem(op1, op2)
            case _:
                raise EmitterError('mov: invalid form')

    def movzx(self, op1: Operand, op2: Operand) -> None:
        if self.section == Section.DATA:
            raise EmitterError('movzx: cannot emit code at data section')
        if not isinstance(op1, Reg) or op1 == RIP or op1.size != QWORD:
            raise EmitterError('movzx: destination must be a qword register')

        dst = reg_id(op1)
        match op2:
            case Reg() as src:
                if src == RIP or src.size not in (BYTE, WORD, DWORD):
                    raise EmitterError('movzx: source must be a byte, word, or dword register')
                src_id = reg_id(src)
                if src.size == DWORD:
                    rex = 0x40 | ((dst >> 3) << 2) | (src_id >> 3)
                    rex_prefix = bytes((rex,)) if rex != 0x40 else b''
                    mod_rm = 0xC0 | ((dst & 7) << 3) | (src_id & 7)
                    self.emit_bytes(rex_prefix + bytes((0x8B, mod_rm)))
                else:
                    opcode = 0xB6 if src.size == BYTE else 0xB7
                    rex = 0x48 | ((dst >> 3) << 2) | (src_id >> 3)
                    mod_rm = 0xC0 | ((dst & 7) << 3) | (src_id & 7)
                    self.emit_bytes(bytes((rex, 0x0F, opcode, mod_rm)))

            case Mem() as mem:
                if mem.size not in (BYTE, WORD, DWORD):
                    raise EmitterError('movzx: source must be byte, word, or dword memory')
                if mem.size == DWORD:
                    self.emit_mov_mem(op1, mem)
                    return
                opcode = 0xB6 if mem.size == BYTE else 0xB7
                self.emit_mem_op(op1, mem, bytes((0x0F, opcode)), True)

            case _:
                raise EmitterError('movzx: invalid form')

    def ret(self) -> None:
        self.emit_bytes(b'\xc3')

    def finalize(self) -> None:
        page_size = mmap.PAGESIZE
        text_size = max(page_size, (len(self.text) + page_size - 1) // page_size * page_size)
        data_size = max(page_size, (len(self.data) + page_size - 1) // page_size * page_size)
        mapping = mmap.mmap(
            -1,
            text_size + data_size,
            flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
            prot=mmap.PROT_READ | mmap.PROT_WRITE,
        )
        mapping_address = ctypes.addressof(ctypes.c_char.from_buffer(mapping))
        text_address = mapping_address
        data_address = mapping_address + text_size

        patches: list[tuple[int, bytes]] = []
        for name, references in self.label_refs.items():
            label = self.labels.get(name)
            if label is None:
                mapping.close()
                raise EmitterError('link error: label not found')
            label_section, label_offset = label
            if label_section == Section.TEXT:
                label_address = text_address + label_offset
            else:
                label_address = data_address + label_offset
            for ref in references:
                displacement = label_address - (text_address + ref.rip)
                encoded = signed_bytes(displacement, 4)
                if encoded is None or ref.position < 0 or ref.position + 4 > len(self.text):
                    mapping.close()
                    raise EmitterError('link error: offset out of range')
                patches.append((ref.position, encoded))

        for reference_offset, encoded in patches:
            self.text[reference_offset:reference_offset + 4] = encoded

        mapping[:len(self.text)] = self.text
        mapping[text_size:text_size + len(self.data)] = self.data

        libc = ctypes.CDLL(None, use_errno=True)
        mprotect = libc.mprotect
        mprotect.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int)
        mprotect.restype = ctypes.c_int
        if mprotect(text_address, text_size, mmap.PROT_READ | mmap.PROT_EXEC) != 0:
            mapping.close()
            raise EmitterError('link error: mprotect failed')

        if self.mapping is not None:
            self.mapping.close()
        self.mapping = mapping

        symbols: dict[str, int] = {}
        for name, (section, offset) in self.labels.items():
            if not name.startswith('.'):
                base_address = text_address if section == Section.TEXT else data_address
                symbols[name] = base_address + offset
        self.symbols = symbols
