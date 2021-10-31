# PyHIP - Python Interface of [HIP](https://github.com/ROCm-Developer-Tools/HIP)

## Introduction
This small python lib which hooks into HIP library and provides pythonic interface to it.

There are two parts of it, hip library and hiprtc library.

## Sample Usage
```python
import ctypes, hip
prog = hip.hiprtc.hiprtcCreateProgram('extern "C" __global__ void set(int *a) { *a = 10; }', 'set', [], [])
hip.hiprtc.hiprtcCompileProgram(prog, ['--offload-arch=gfx906'])
code = hip.hiprtc.hiprtcGetCode(prog)
module = hip.hip.hipModuleLoadData(code)
kernel = hip.hip.hipModuleGetFunction(module, 'set')
ptr = hip.hip.hipMalloc(4)

class SSS(ctypes.Structure):
  _fields_ = [("a", ctypes.c_void_p)]


struct = SSS(ptr)
hip.hip.hipModuleLaunchKernel(kernel, 1, 1, 1, 1, 1, 1, 0, 0, struct)
res = ctypes.c_int(0)
hip.hip.hipMemcpy_dtoh(ctypes.byref(res), ptr, 4)
print(res.value)
```
