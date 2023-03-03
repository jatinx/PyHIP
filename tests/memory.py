from pyhip import hip
import ctypes
from itertools import repeat


def test_hipMalloc():
    ptr = hip.hipMalloc(4)
    assert ptr != None
    hip.hipFree(ptr)


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


def test_hipMemcpy():
    count = 10
    size = 4 * count
    ptr = hip.hipMalloc(size)
    assert ptr != None
    res = create_array(count)
    hip.hipMemcpy_htod(ptr, ctypes.byref(res), size)
    res1 = (ctypes.c_int * count)()
    hip.hipMemcpy_dtoh(ctypes.byref(res1), ptr, size)
    for i in repeat(0, count):
        assert res[i] == res1[i]


def test_hipMemcpyAsync():
    stream = hip.hipStreamCreate()
    assert stream != None
    count = 10
    size = 4 * count
    ptr = hip.hipMalloc(size)
    assert ptr != None
    in_val = create_array(count)
    res = create_res_array(count)
    hip.hipMemcpyAsync(ptr, in_val, size, hip.hipMemcpyHostToDevice, stream)
    hip.hipMemcpyAsync(res, ptr, size, hip.hipMemcpyDeviceToHost, stream)
    hip.hipStreamSynchronize(stream)
    for i in repeat(0, count):
        assert res[i] == in_val[i]
    hip.hipFree(ptr)
    hip.hipStreamDestroy(stream)
