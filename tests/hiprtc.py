from pyhip import hiprtc, hip
import ctypes


def test_hiprtcCompileProgram():
    source = """
    __device__ int myGlobalVar;
    extern "C" __global__ void kernel(int *a) { *a = myGlobalVar; }
    """
    prog = hiprtc.hiprtcCreateProgram(source, 'kernel', [], [])
    assert prog != None
    device_properties = hip.hipGetDeviceProperties(0)
    assert device_properties != None
    plat = hip.hipGetPlatformName()
    if plat == "amd":
        hiprtc.hiprtcCompileProgram(
            prog, [f'--offload-arch={device_properties.gcnArchName}'])
    else:
        hiprtc.hiprtcCompileProgram(prog, [])
    code = hiprtc.hiprtcGetCode(prog)
    assert code != None
    module = hip.hipModuleLoadData(code)
    assert module != None
    kernel = hip.hipModuleGetFunction(module, 'kernel')
    assert kernel != None
    global_var, global_var_size = hip.hipModuleGetGlobal(module, 'myGlobalVar')
    assert global_var != None
    assert global_var_size == 4
    set_global_var = res = (ctypes.c_int * 1)()
    set_global_var[0] = 10
    hip.hipMemcpy_htod(global_var, ctypes.byref(set_global_var), 4)
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
