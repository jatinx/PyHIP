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
device_properties = hip.hipGetDeviceProperties(0)
print(f"Compiling kernel for {device_properties.gcnArchName}")
hiprtc.hiprtcCompileProgram(prog, [f'--offload-arch={device_properties.gcnArchName}'])
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

## Testing
Testing is in it's infancy. I'll try to add more as and when I get some time. Any help here is appreciated :)

### How to run tests
Make sure you have ```pytest``` package installed.

From the project folder run ```pytest ./tests/* -v -r A```

## Common Problems
 - Unable to load hip or hiprtc library - OSError: libamdhip64.so: cannot open shared object file: No such file or directory.

    - Make sure that LD_LIBRARY_PATH has hip path on it (/opt/rocm/lib or a custom installation path)

 - Getting error and need to debug

   - Set AMD_LOG_LEVEL=7 for maximum verbosity of HIP APIs.