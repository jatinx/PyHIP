from pyhip import hip
import ctypes
from itertools import repeat
import unittest
class TestStream(unittest.TestCase):
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


    def test_hipStreamCreation(self):
        stream = hip.hipStreamCreate()
        self.assertIsNotNone(stream)
        count = 10
        size = 4 * count
        ptr = hip.hipMalloc(size)
        self.assertIsNotNone(ptr)
        in_val = self.create_array(count)
        res = self.create_res_array(count)
        hip.hipMemcpyAsync_htod(ptr, in_val, size, stream)
        hip.hipMemcpyAsync_dtoh(res, ptr, size, stream)
        hip.hipStreamSynchronize(stream)
        for i in repeat(0, count):
            self.assertEqual(res[i], in_val[i])
        hip.hipFree(ptr)
        hip.hipStreamDestroy(stream)

if __name__ == "__main__":
    unittest.main()