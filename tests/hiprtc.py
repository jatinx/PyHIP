from pyhip import hiprtc, hip
import ctypes


def test_hiprtcCompileProgram():
    source = """
    extern "C" __global__ void kernel(int *a) { *a = 10; }
    """
    prog = hiprtc.hiprtcCreateProgram(source, 'kernel', [], [])
    assert prog != None
    device_properties = hip.hipGetDeviceProperties(0)
    assert device_properties != None
    hiprtc.hiprtcCompileProgram(
        prog, [f'--offload-arch={device_properties.gcnArchName}'])
    code = hiprtc.hiprtcGetCode(prog)
    assert code != None
    module = hip.hipModuleLoadData(code)
    assert module != None
    kernel = hip.hipModuleGetFunction(module, 'kernel')
    assert kernel != None
    ptr = hip.hipMalloc(4)
    assert ptr != None
    
    class PackageStruct(ctypes.Structure):
        _fields_ = [("a", ctypes.c_void_p)]
    struct = PackageStruct(ptr)
    hip.hipModuleLaunchKernel(kernel, 1, 1, 1, 1, 1, 1, 0, 0, struct)
    res = (ctypes.c_int * 1)()
    hip.hipMemcpy_dtoh(ctypes.byref(res), ptr, 4)
    assert res[0] == 10

    hiprtc.hiprtcDestroyProgram(prog)
