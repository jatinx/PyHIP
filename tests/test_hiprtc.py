from pyhip import hiprtc, hip
import ctypes
import unittest


class TestHiprtc(unittest.TestCase):
    def test_hiprtcCompileProgram(self):
        source = """
        __device__ int myGlobalVar;
        extern "C" __global__ void kernel(int *a) { *a = myGlobalVar; }
        """
        prog = hiprtc.hiprtcCreateProgram(source, "kernel", [], [])
        self.assertIsNotNone(prog)
        device_properties = hip.hipGetDeviceProperties(0)
        self.assertIsNotNone(device_properties)
        plat = hip.hipGetPlatformName()
        if plat == "amd":
            hiprtc.hiprtcCompileProgram(
                prog, [f"--offload-arch={device_properties.gcnArchName}"]
            )
        else:
            hiprtc.hiprtcCompileProgram(prog, [])
        code = hiprtc.hiprtcGetCode(prog)
        self.assertIsNotNone(code)
        module = hip.hipModuleLoadData(code)
        self.assertIsNotNone(module)
        kernel = hip.hipModuleGetFunction(module, "kernel")
        self.assertIsNotNone(kernel)
        global_var, global_var_size = hip.hipModuleGetGlobal(module, "myGlobalVar")
        self.assertIsNotNone(global_var)
        self.assertEqual(global_var_size, 4)
        set_global_var = (ctypes.c_int * 1)()
        set_global_var[0] = 10
        hip.hipMemcpy_htod(global_var, ctypes.byref(set_global_var), 4)
        ptr = hip.hipMalloc(4)
        self.assertIsNotNone(ptr)

        class PackageStruct(ctypes.Structure):
            _fields_ = [("a", ctypes.c_void_p)]

        struct = PackageStruct(ptr)
        hip.hipModuleLaunchKernel(kernel, 1, 1, 1, 1, 1, 1, 0, 0, struct)
        res = (ctypes.c_int * 1)()
        res[0] = 0
        hip.hipMemcpy_dtoh(ctypes.byref(res), ptr, 4)
        self.assertEqual(res[0], 10)
        hip.hipFree(ptr)
        hiprtc.hiprtcDestroyProgram(prog)


if __name__ == "__main__":
    unittest.main()
