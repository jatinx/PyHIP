from pyhip import hip
import ctypes
from itertools import repeat
import unittest

class TestEvent(unittest.TestCase):
    def create_array(self, count):
        res = (ctypes.c_int * count)()
        j = 1
        for i in repeat(0, count):
            res[j-1] = j
            j = j + 1
        return res


    def create_res_array(self, count):
        res = (ctypes.c_int * count)()
        j = 1
        for i in repeat(0, count):
            res[i] = 0
        return res


    def test_hipEvents(self):
        stream = hip.hipStreamCreate()
        self.assertIsNotNone(stream)
        count = 10
        size = 4 * count
        ptr = hip.hipMalloc(size)
        self.assertIsNotNone(ptr)
        in_val = self.create_array(count)
        res = self.create_res_array(count)
        start = hip.hipEventCreate()
        end = hip.hipEventCreate()
        hip.hipEventRecord(start, stream)
        hip.hipMemcpyAsync_htod(ptr, in_val, size, stream)
        hip.hipMemcpyAsync_dtoh(res, ptr, size, stream)
        hip.hipEventRecord(end, stream)
        
        hip.hipEventSynchronize(end)
        self.assertTrue(hip.hipEventQuery(end))
        time = hip.hipEventElapsedTime(start, end)
        self.assertGreater(time, 0)
        for i in repeat(0, count):
            self.assertEqual(res[i], in_val[i])
        hip.hipFree(ptr)
        hip.hipStreamDestroy(stream)
        hip.hipEventDestroy(start)
        hip.hipEventDestroy(end)

if __name__ == "__main__":
    unittest.main()