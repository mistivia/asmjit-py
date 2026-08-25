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

`finalize()` allocates executable memory and returns a mapping from public
labels to their addresses. `ctypes.CFUNCTYPE` converts the address of `f` into
a callable Python object.

## Assembly Spec

```
`m8/m16/m32/m64/m*`: `[r64]` 
                   | `[r64 + r64 * scale + simm32]` (scale = 1/2/4/8)
                   | `[r64 * scale + simm32]` (scale = 1/2/4/8)
                   | `[r64 + simm32]`
                   | `[rip + rel32]`
`rel32`: label 
```

### Implemented Instructions

- `MOV`: `mov r64, r64`   
- `MOV`: `mov r64, imm64`
- `MOV`: `mov r64, m64`
- `MOV`: `mov m64, r64`
- `MOV`: `mov m32, r64`  // low bits
- `MOV`: `mov m16, r64`  // low bits
- `MOV`: `mov m8, r64`   // low bits
- `MOVZX`: `movzx r64, r8`
- `MOVZX`: `movzx r64, r16`
- `MOVZX`: `movzx r64, r32`
- `MOVZX`: `movzx r64, m8`
- `MOVZX`: `movzx r64, m16`
- `MOVZX`: `movzx r64, m32`
- `MOVSX`: `movsx r64, r8`
- `MOVSX`: `movsx r64, r16`
- `MOVSX`: `movsx r64, r32`
- `MOVSX`: `movsx r64, m8`
- `MOVSX`: `movsx r64, m16`
- `MOVSX`: `movsx r64, m32`
- `RET`: `ret`

### Planned Instructions

- `LEA`:       `lea r64, m*`
- `ADD`:       `add r64, r64`
- `ADD`:       `add r64, simm32`
- `SUB`:       `sub r64, r64`
- `SUB`:       `sub r64, simm32`
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
- `BE`:        `be r64, r64, rel32`       // CMP + Jcc
- `BE`:        `be r64, simm32, rel32`    // CMP + Jcc
- `BE`:        `be xmm, xmm, rel32`       // UCOMISD + Jcc // NaN: true
- `BNE`:       `bne r64, r64, rel32`      // CMP + Jcc
- `BNE`:       `bne r64, simm32, rel32`   // CMP + Jcc
- `BNE`:       `bne xmm, xmm, rel32`      // UCOMISD + Jcc // NaN: false
- `BL`:        `bl  r64, r64, rel32`      // CMP + Jcc
- `BL`:        `bl  r64, simm32, rel32`   // CMP + Jcc
- `BL`:        `bl  xmm, xmm, rel32`      // UCOMISD + Jcc // NaN: true
- `BLE`:       `ble r64, r64, rel32`      // CMP + Jcc
- `BLE`:       `ble r64, simm32, rel32`   // CMP + Jcc
- `BLE`:       `ble xmm, xmm, rel32`      // UCOMISD + Jcc // NaN: true
- `BG`:        `bg  r64, r64, rel32`      // CMP + Jcc
- `BG`:        `bg  r64, simm32, rel32`   // CMP + Jcc
- `BG`:        `bg  xmm, xmm, rel32`      // UCOMISD + Jcc // NaN: false
- `BGE`:       `bge r64, r64, rel32`      // CMP + Jcc
- `BGE`:       `bge r64, simm32, rel32`   // CMP + Jcc
- `BGE`:       `bge xmm, xmm, rel32`      // UCOMISD + Jcc  // NaN: false
- `BP`:        `bp  xmm, xmm, rel32`      // UCOMISD + Jcc, // when any arg is NaN
- `BLU`: `blu  r64, r64, rel32`     // CMP + Jcc
- `BLU`:       `blu  r64, simm32, rel32`  // CMP + Jcc
- `BLEU`:      `bleu r64, r64, rel32`     // CMP + Jcc
- `BLEU`:      `bleu r64, simm32, rel32`  // CMP + Jcc
- `BGU`:       `bgu  r64, r64, rel32`     // CMP + Jcc
- `BGU`:       `bgu  r64, simm32, rel32`  // CMP + Jcc
- `BGEU`:      `bgeu r64, r64, rel32`     // CMP + Jcc
- `BGEU`:      `bgeu r64, simm32, rel32`  // CMP + Jcc
- `CALL`:      `call rel32`  // SysV ABI
- `CALL`:      `call r64`    // SysV ABI
- `MOVSD`:     `movsd xmm, xmm`
- `MOVSD`:     `movsd xmm, m64`
- `MOVSD`:     `movsd m64, xmm`
- `ADDSD`:     `addsd xmm, xmm`
- `SUBSD`:     `subsd xmm, xmm`
- `MULSD`:     `mulsd xmm, xmm`
- `DIVSD`:     `divsd xmm, xmm`
- `CVTSI2SD`:  `cvtsi2sd xmm, r64`
- `CVTTSD2SI`: `cvttsd2si r64, xmm`
