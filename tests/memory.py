from pyhip import hip
import ctypes
from itertools import repeat
import unittest

class TestMemory(unittest.TestCase):
    def test_hipMalloc(self):
        ptr = hip.hipMalloc(4)
        assert ptr != None
        hip.hipFree(ptr)


    def create_array(self, count):
        res = (ctypes.c_int * count)()
        for i in range(count):
            res[i] = i + 1
        return res


    def create_res_array(self, count):
        res = (ctypes.c_int * count)()
        for i in range(count):
            res[i] = 0
        return res


    def test_hipMemcpy(self):
        count = 10
        size = 4 * count
        ptr = hip.hipMalloc(size)
        self.assertIsNotNone(ptr)
        res = self.create_array(count)
        hip.hipMemcpy_htod(ptr, ctypes.byref(res), size)
        res1 = (ctypes.c_int * count)()
        hip.hipMemcpy_dtoh(ctypes.byref(res1), ptr, size)
        for i in repeat(0, count):
            self.assertEqual(res[i], res1[i])


    def test_hipMemcpyAsync(self):
        stream = hip.hipStreamCreate()
        self.assertIsNotNone(stream)
        count = 10
        size = 4 * count
        ptr = hip.hipMalloc(size)
        self.assertIsNotNone(ptr)
        in_val = self.create_array(count)
        res = self.create_res_array(count)
        hip.hipMemcpyAsync(ptr, in_val, size, hip.hipMemcpyHostToDevice, stream)
        hip.hipMemcpyAsync(res, ptr, size, hip.hipMemcpyDeviceToHost, stream)
        hip.hipStreamSynchronize(stream)
        for i in repeat(0, count):
            self.assertEqual(res[i], in_val[i])
        hip.hipFree(ptr)
        hip.hipStreamDestroy(stream)

    def test_memset(self):
        size = 4
        x_d = hip.hipMalloc(size)
        hip.hipMemset(x_d, 4, size)
        output = (ctypes.c_int8 * size)()
        hip.hipMemcpy_dtoh(output, x_d, size)
        assert all(output[i] == 4 for i in range(len(output)))

if __name__ == "__main__":
    unittest.main()