# asmjit

A Python x86-64 JIT assembler

## Example

The following example creates an `int f(void)` function equivalent to:

```c
int f(void) {
    return 42;
}
```

The generated instructions are

```asm
f:
    mov rax, 42
    ret
```

```python
import ctypes
from asmjit.x86_64 import *

e = Emitter()

e.label("f")
e.mov(RAX, 42)
e.ret()
e.finalize()

f = ctypes.CFUNCTYPE(ctypes.c_int)(e.symbol('f'))
assert f() == 42
```

`finalize()` allocates executable memory and resolves labels. `symbol()` returns
the address of a public label, and `ctypes.CFUNCTYPE` converts that address into
a callable Python object.

## Assembly Spec

```
`m8/m16/m32/m64/m*`: `[r64]` 
                   | `[r64 + r64 * scale +/- simm32]` (scale = 1/2/4/8)
                   | `[r64 * scale +/- simm32]` (scale = 1/2/4/8)
                   | `[r64 +/- simm32]`
                   | `[rip + rel32]`
`rel32`: label 
`cond`: EQ | NE | LT | GT | LE | GE | LTU | GTU | GEU | LEU
```

### Implemented Instructions

- `MOV`:    `mov r64, r64`
- `MOV`:    `mov r64, imm64`
- `MOV`:    `mov r64, m64`
- `MOV`:    `mov m64, r64`
- `MOV`:    `mov m32, r64`  // low bits
- `MOV`:    `mov m16, r64`  // low bits
- `MOV`:    `mov m8, r64`   // low bits
- `MOVZX`:  `movzx r64, r8`
- `MOVZX`:  `movzx r64, r16`
- `MOVZX`:  `movzx r64, r32`
- `MOVZX`:  `movzx r64, m8`
- `MOVZX`:  `movzx r64, m16`
- `MOVZX`:  `movzx r64, m32`
- `MOVSX`:  `movsx r64, r8`
- `MOVSX`:  `movsx r64, r16`
- `MOVSX`:  `movsx r64, r32`
- `MOVSX`:  `movsx r64, m8`
- `MOVSX`:  `movsx r64, m16`
- `MOVSX`:  `movsx r64, m32`
- `LEA`:    `lea r64, m*`
- `MOVSD`:  `movsd xmm, xmm`
- `MOVSD`:  `movsd xmm, m64`
- `MOVSD`:  `movsd m64, xmm`
- `ADD`:    `add r64, r64`
- `ADD`:    `add r64, simm32`
- `SUB`:    `sub r64, r64`
- `SUB`:    `sub r64, simm32`
- `PUSH`:   `push r64`                        // pseudo-instruction
- `POP`:    `pop r64`                         // pseudo-instruction
- `BEGIN`:  `begin`                           // `PUSH RBP` + `MOV RBP, RSP`
- `END`:    `end`                             // `MOV RSP, RBP` + `POP RBP` + `RET`
- `CALL`:   `call rel32`                      // SysV ABI
- `CALL`:   `call r64`                        // SysV ABI
- `BRANCH`: `branch cond, r64, r64, rel32`    // `CMP` + `Jcc`
- `BRANCH`: `branch cond, r64, simm32, rel32` // `CMP` + `Jcc`
- `BRANCH`: `branch cond, xmm, xmm, rel32`    // `UCOMISD` + `Jcc`
- `CSET`:   `cset cond, r64, r64, r8`         // `CMP` + `SETcc`
- `CSET`:   `cset cond, r64, simm32, r8`      // `CMP` + `SETcc`
- `CSET`:   `cset cond, xmm, xmm, r8`         // `UCOMISD` + `SETcc`
- `RET`:    `ret`

### Planned Instructions

- `NEG`:       `neg r64`
- `IMUL`:      `imul r64, r64`    
- `IMUL`:      `imul r64, simm32`
- `IDIV`:      `idiv r64, r64`    // clobber: rax, rdx  // when op2=0, SIGFPE // signed overflow: SIGFPE
- `DIV`:       `div  r64, r64`    // clobber: rax, rdx  // when op2=0, SIGFPE
- `IREM`:      `irem r64, r64`    // clobber: rax, rdx  // when op2=0, SIGFPE // signed overflow: SIGFPE
- `REM`:       `rem r64, r64`     // clobber: rax, rdx  // when op2=0, SIGFPE
- `AND`:       `and r64, r64`
- `AND`:       `and r64, simm32`
- `OR`:        `or r64, r64`
- `OR`:        `or r64, simm32`
- `XOR`:       `xor r64, r64`
- `XOR`:       `xor r64, simm32`
- `SHL`:       `shl r64, r64`    // clobber: rcx // counter & 63
- `SHL`:       `shl r64, uimm8`  // counter & 63
- `SAR`:       `sar r64, r64`    // clobber: rcx // counter & 63
- `SAR`:       `sar r64, uimm8`  // counter & 63
- `SHR`:       `shr r64, r64`    // clobber: rcx // counter & 63
- `SHR`:       `shr r64, uimm8`  // counter & 63
- `ROR`:       `ror r64, r64`    // clobber: rcx // counter & 63
- `ROR`:       `ror r64, uimm8`  // counter & 63
- `ROL`:       `rol r64, r64`    // clobber: rcx // counter & 63
- `ROL`:       `rol r64, uimm8`  // counter & 63
- `JMP`:       `jmp rel32`
- `JMP`:       `jmp r64`
- `ADDSD`:     `addsd xmm, xmm`
- `SUBSD`:     `subsd xmm, xmm`
- `MULSD`:     `mulsd xmm, xmm`
- `DIVSD`:     `divsd xmm, xmm`
- `CVTSI2SD`:  `cvtsi2sd xmm, r64`
- `CVTTSD2SI`: `cvttsd2si r64, xmm`
