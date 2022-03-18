from itertools import repeat
import time

size = 50000000
x = 2
y = 3


def create_array():
    cpu = list()
    gpu = (ctypes.c_int * size)()
    j = 1
    for i in repeat(0, size):
        cpu.append(j)
        gpu[j-1] = j
        j = j + 1
    return cpu, gpu

def cpu_axpy(a):
    result = list()
    j = 0
    for i in repeat(0, size):
        result.append(a[j] * x + y)
        j = j + 1
    return result

from pyhip import hip, hiprtc
import ctypes
def gpu_axpy(res):
    source = """
    #include <hip/hip_runtime.h> // Needed for older ROCm versions (at least 4.2) to access blockDim / blockIdx / threadIdx
    extern "C" __global__ void axpy(int *a, int x, int y, size_t size) {
      int i = blockDim.x * blockIdx.x + threadIdx.x;
      if(i < size) {
        a[i] = a[i] * x + y;
      }
    }
    """
    prog = hiprtc.hiprtcCreateProgram(source, 'axpy', [], [])
    device_properties = hip.hipGetDeviceProperties(0)
    print(f"Compiling kernel for {device_properties.name}")
    hiprtc.hiprtcCompileProgram(prog, [f'--offload-arch={device_properties.gcnArchName}'])
    code = hiprtc.hiprtcGetCode(prog)
    module = hip.hipModuleLoadData(code)
    kernel = hip.hipModuleGetFunction(module, 'axpy')
    ptr = hip.hipMalloc(4 * size)

    class PackageStruct(ctypes.Structure):
        _fields_ = [("a", ctypes.c_void_p),
                    ("x", ctypes.c_int),
                    ("y", ctypes.c_int),
                    ("size", ctypes.c_size_t)]

    hip.hipMemcpy_htod(ptr, ctypes.byref(res), ctypes.sizeof(ctypes.c_int) * size)
    struct = PackageStruct(ptr, 2, 3, size)
    block = int(size/1024) + 1
    hip.hipModuleLaunchKernel(kernel, block, 1, 1, 1024, 1, 1, 0, 0, struct)
    hip.hipMemcpy_dtoh(ctypes.byref(res), ptr, ctypes.sizeof(ctypes.c_int) * size)
    hip.hipFree(ptr)
    return res

if __name__ == "__main__":
    cpu_array, gpu_array = create_array()

    start = time.time()
    cpu_result = cpu_axpy(cpu_array)
    cend = time.time()
    gres = gpu_axpy(gpu_array)
    gend = time.time()
    gpu_result = list()

    # Copy back for comparision
    for i in gres:
        gpu_result.append(i)

    if cpu_result != gpu_result:
        print("Error in vaidation: ", cpu_result, gpu_result)
    else:
        print("Passed")
        print("CPU Time: ", (cend - start), " Gpu time: ", (gend - cend))

