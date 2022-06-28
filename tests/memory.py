from pyhip import hip
import ctypes
from itertools import repeat


def test_hipMalloc():
    ptr = hip.hipMalloc(4)
    assert ptr != None
    hip.hipFree(ptr)


def create_array(count):
    res = (ctypes.c_int * count)()
    j = 1
    for i in repeat(0, count):
        res[j-1] = j
        j = j + 1
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
