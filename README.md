# PyHIP - Python Interface of [HIP](https://github.com/ROCm-Developer-Tools/HIP)

## Introduction
This small python lib which hooks into HIP library and provides pythonic interface to it.

There are two parts of it, hip library and hiprtc library.

## Example Usage
```python
import ctypes
from pyhip import hip, hiprtc
source = """
extern "C" __global__ void set(int *a) {
  *a = 10;
}
"""
prog = hiprtc.hiprtcCreateProgram(source, 'set', [], [])
hiprtc.hiprtcCompileProgram(prog, ['--offload-arch=gfx906'])
code = hiprtc.hiprtcGetCode(prog)
module = hip.hipModuleLoadData(code)
kernel = hip.hipModuleGetFunction(module, 'set')
ptr = hip.hipMalloc(4)

class PackageStruct(ctypes.Structure):
  _fields_ = [("a", ctypes.c_void_p)]

struct = PackageStruct(ptr)
hip.hipModuleLaunchKernel(kernel, 1, 1, 1, 1, 1, 1, 0, 0, struct)
res = ctypes.c_int(0)
hip.hipMemcpy_dtoh(ctypes.byref(res), ptr, 4)
print(res.value)
```
