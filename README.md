# jitasm

A Python x86-64 JIT assembler

## Example

The following example creates an `int max(void)` function equivalent to:

```c
int64_t max(int64_t a, int64_t b) {
    if (a >= b) return a;
    return b;
}
```

The generated instructions are:

```asm
max:
    mov rax, rdi
    cmp rdi, rsi
    jge .done
    mov rax, rsi
.done:
    ret
```

And we provide a peudo-instruction `branch.cc` to do `CMP` and `Jcc`:

```asm
max:
    mov rax, rdi
    branch.ge rdi, rsi, .done
    mov rax, rsi
.done:
    ret
```

And we implement it in Python using `jitasm`:

```python
from jitasm.x86_64 import *
from jitasm.utils import ccall

e = Emitter()
(e.label("max"),
    e.mov(RAX, RDI),
    e.branch(GE, RDI, RSI, ".done"),
    e.mov(RAX, RSI),
 e.label(".done"),
    e.ret())
e.finalize()
max_fn_ptr = e.symbol("max")

assert ccall(max_fn_ptr, 3, 7)   == 7
assert ccall(max_fn_ptr, 42, -1) == 42
```

`finalize()` allocates executable memory and resolves labels. `symbol()` returns
the address of a public label, and `ctypes.CFUNCTYPE` converts that address into
a callable Python object. Call `unmap()` when the generated code is no longer
needed. Functions created from `symbol()` must not be called after unmapping.
The emitter can be finalized again to create a fresh mapping.

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

Only an essential subset of x86-64 instruction set with several pseodo-intructions are implemented. No SIMD support yet.

- `MOV`:    `mov r64, r64`
- `MOV`:    `mov r64, imm64`                  // zero uses `XOR r64, r64`
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
- `BITAND`: `bitand r64, r64`
- `BITAND`: `bitand r64, simm32`
- `BITOR`:  `bitor r64, r64`
- `BITOR`:  `bitor r64, simm32`
- `XOR`:    `xor r64, r64`
- `XOR`:    `xor r64, simm32`
- `BITNOT`: `bitnot r64`                      // `XOR r64, -1`
- `NEG`:    `neg r64`
- `IMUL`:   `imul r64, r64`
- `IMUL`:   `imul r64, simm32`
- `IDIV`:   `idiv r64, r64`                  // op1 = quotient, op2 = remainder; clobbers RAX and RDX
- `DIV`:    `div r64, r64`                   // op1 = quotient, op2 = remainder; clobbers RAX and RDX
- `ADDSD`:  `addsd xmm, xmm`
- `SUBSD`:  `subsd xmm, xmm`
- `MULSD`:  `mulsd xmm, xmm`
- `DIVSD`:  `divsd xmm, xmm`
- `CVTSI2SD`:  `cvtsi2sd xmm, r64`
- `CVTTSD2SI`: `cvttsd2si r64, xmm`
- `ROUND`:  `round xmm, xmm`                  // round to nearest, ties to even
- `CEIL`:   `ceil xmm, xmm`
- `FLOOR`:  `floor xmm, xmm`
- `TRUNC`:  `trunc xmm, xmm`
- `SHL`:    `shl r64, r64`                   // pseudo-instruction, clobbers RCX
- `SHL`:    `shl r64, uimm8`
- `SAR`:    `sar r64, r64`                   // pseudo-instruction, clobbers RCX
- `SAR`:    `sar r64, uimm8`
- `SHR`:    `shr r64, r64`                   // pseudo-instruction, clobbers RCX
- `SHR`:    `shr r64, uimm8`
- `ROR`:    `ror r64, r64`                   // pseudo-instruction, clobbers RCX
- `ROR`:    `ror r64, uimm8`
- `ROL`:    `rol r64, r64`                   // pseudo-instruction, clobbers RCX
- `ROL`:    `rol r64, uimm8`
- `PUSH`:   `push r64`                        // pseudo-instruction
- `POP`:    `pop r64`                         // pseudo-instruction
- `BEGIN`:  `begin`                           // `PUSH RBP` + `MOV RBP, RSP`
- `END`:    `end`                             // `MOV RSP, RBP` + `POP RBP` + `RET`
- `CALL`:   `call rel32`                      // SysV ABI
- `CALL`:   `call r64`                        // SysV ABI
- `JMP`:    `jmp rel32`
- `JMP`:    `jmp r64`
- `BRANCH`: `branch cond, r64, r64, rel32`    // `CMP` + `Jcc`
- `BRANCH`: `branch cond, r64, simm32, rel32` // `CMP` + `Jcc`
- `BRANCH`: `branch cond, xmm, xmm, rel32`    // `UCOMISD` + `Jcc`
- `CSET`:   `cset cond, r64, r64, r8`         // `CMP` + `SETcc`
- `CSET`:   `cset cond, r64, simm32, r8`      // `CMP` + `SETcc`
- `CSET`:   `cset cond, xmm, xmm, r8`         // `UCOMISD` + `SETcc`
- `RET`:    `ret`
- `ALIGN`:  `align bytes`                     // DATA section zero-padding
