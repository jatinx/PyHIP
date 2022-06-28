from pyhip import hip
import ctypes
from itertools import repeat


def create_array(count):
    res = (ctypes.c_int * count)()
    j = 1
    for i in repeat(0, count):
        res[j-1] = j
        j = j + 1
    return res


def create_res_array(count):
    res = (ctypes.c_int * count)()
    j = 1
    for i in repeat(0, count):
        res[i] = 0
    return res


def test_hipEvents():
    stream = hip.hipStreamCreate()
    assert stream != None
    count = 10
    size = 4 * count
    ptr = hip.hipMalloc(size)
    assert ptr != None
    in_val = create_array(count)
    res = create_res_array(count)
    start = hip.hipEventCreate()
    end = hip.hipEventCreate()
    hip.hipEventRecord(start, stream)
    hip.hipMemcpyAsync_htod(ptr, in_val, size, stream)
    hip.hipMemcpyAsync_dtoh(res, ptr, size, stream)
    hip.hipEventRecord(end, stream)
    hip.hipEventSynchronize(end)
    time = hip.hipEventElapsedTime(start, end)
    assert time > 0
    for i in repeat(0, count):
        assert res[i] == in_val[i]
    hip.hipFree(ptr)
    hip.hipStreamDestroy(stream)
    hip.hipEventDestroy(start)
    hip.hipEventDestroy(end)
