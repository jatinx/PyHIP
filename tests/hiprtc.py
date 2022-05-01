from pyhip import hiprtc, hip

def test_hiprtcCompileProgram():
    source = """
    extern "C" __global__ void kernel(int *a) { *a = 10; }
    """
    prog = hiprtc.hiprtcCreateProgram(source, 'kernel', [], [])
    assert prog != None
    device_properties = hip.hipGetDeviceProperties(0)
    assert device_properties != None
    hiprtc.hiprtcCompileProgram(prog, [f'--offload-arch={device_properties.gcnArchName}'])
    code = hiprtc.hiprtcGetCode(prog)
    assert code != None
    module = hip.hipModuleLoadData(code)
    assert module != None
    kernel = hip.hipModuleGetFunction(module, 'kernel')
    assert kernel != None
    hiprtc.hiprtcDestroyProgram(prog)
