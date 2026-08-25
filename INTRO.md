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
from asmjit.asmjit import *

e = Emitter()

e.label("f")
e.mov(RAX, 42)
e.ret()
symbols = e.finalize()

f = ctypes.CFUNCTYPE(ctypes.c_int)(symbols["f"])
assert f() == 42
```

`finalize()` allocates executable memory and returns a mapping from public
labels to their addresses. `ctypes.CFUNCTYPE` converts the address of `f` into
a callable Python object.
