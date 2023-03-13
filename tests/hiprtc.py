from pyhip import hiprtc, hip
import ctypes


def ASSERT_DRV(err):
    if isinstance(err, hip.hipError):
        if err != hip.hipError.hipSuccess:
            raise RuntimeError("HIP Error: {}".format(err))
    elif isinstance(err, hiprtc.hiprtcError):
        if err != hiprtc.hiprtcError.hiprtcSuccess:
            raise RuntimeError("HIPRTC Error: {}".format(err))
    else:
        raise RuntimeError("Unknown error type: {}".format(err))


def test_hiprtcCompileProgram():
    source = """
    extern "C" __global__ void kernel(int *a) { *a = 10; }
    """
    (hres, prog) = hiprtc.hiprtcCreateProgram(source, 'kernel', [], [])
    assert prog != None
    (hres, device_properties) = hip.hipGetDeviceProperties(0)
    assert device_properties != None
    plat = hip.hipGetPlatformName()
    if plat == "amd":
        (hres,) = hiprtc.hiprtcCompileProgram(
            prog, [f'--offload-arch={device_properties.gcnArchName}'])
        ASSERT_DRV(hres)
    else:
        hiprtc.hiprtcCompileProgram(prog, [])
    (hres, code) = hiprtc.hiprtcGetCode(prog)
    ASSERT_DRV(hres)
    assert code != None
    (hres, module) = hip.hipModuleLoadData(code)
    ASSERT_DRV(hres)
    assert module != None
    (hres, kernel) = hip.hipModuleGetFunction(module, 'kernel')
    ASSERT_DRV(hres)
    assert kernel != None
    (hres, ptr) = hip.hipMalloc(4)
    ASSERT_DRV(hres)
    assert ptr != None

    class PackageStruct(ctypes.Structure):
        _fields_ = [("a", ctypes.c_void_p)]
    struct = PackageStruct(ptr)
    (hres,) = hip.hipModuleLaunchKernel(kernel, 1, 1, 1, 1, 1, 1, 0, 0, struct)
    ASSERT_DRV(hres)
    ASSERT_DRV(hres)
    res = (ctypes.c_int * 1)()
    (hres,) = hip.hipMemcpy_dtoh(ctypes.byref(res), ptr, 4)
    ASSERT_DRV(hres)
    assert res[0] == 10

    (hres,) = hiprtc.hiprtcDestroyProgram(prog)
    ASSERT_DRV(hres)
