from pyhip import hip
import ctypes
from itertools import repeat


def create_array(count):
    res = (ctypes.c_int * count)()
    for i in range(count):
        res[i] = i + 1
    return res


def create_res_array(count):
    res = (ctypes.c_int * count)()
    for i in range(count):
        res[i] = 0
    return res


def test_hipStreamCreation():
    stream = hip.hipStreamCreate()
    assert stream != None
    count = 10
    size = 4 * count
    ptr = hip.hipMalloc(size)
    assert ptr != None
    in_val = create_array(count)
    res = create_res_array(count)
    hip.hipMemcpyAsync_htod(ptr, in_val, size, stream)
    hip.hipMemcpyAsync_dtoh(res, ptr, size, stream)
    hip.hipStreamSynchronize(stream)
    for i in repeat(0, count):
        assert res[i] == in_val[i]
    hip.hipFree(ptr)
    hip.hipStreamDestroy(stream)
