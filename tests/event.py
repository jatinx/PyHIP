from pyhip import hip
import ctypes
from itertools import repeat


def ASSERT_DRV(err):
    if isinstance(err, hip.hipError):
        if err != hip.hipError.hipSuccess:
            raise RuntimeError("HIP Error: {}".format(err))
    elif isinstance(err, hiprtc.hiprtcError):
        if err != hiprtc.hiprtcError.hiprtcSuccess:
            raise RuntimeError("HIPRTC Error: {}".format(err))
    else:
        raise RuntimeError("Unknown error type: {}".format(err))


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
    (hres, stream) = hip.hipStreamCreate()
    ASSERT_DRV(hres)
    assert stream != None
    count = 10
    size = 4 * count
    (hres, ptr) = hip.hipMalloc(size)
    ASSERT_DRV(hres)
    assert ptr != None
    in_val = create_array(count)
    res = create_res_array(count)
    (hres, start) = hip.hipEventCreate()
    ASSERT_DRV(hres)
    (hres, end) = hip.hipEventCreate()
    ASSERT_DRV(hres)
    (hres,) = hip.hipEventRecord(start, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipMemcpyAsync_htod(ptr, in_val, size, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipMemcpyAsync_dtoh(res, ptr, size, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipEventRecord(end, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipEventSynchronize(end)
    ASSERT_DRV(hres)
    (hres, time) = hip.hipEventElapsedTime(start, end)
    ASSERT_DRV(hres)
    assert time > 0
    for i in repeat(0, count):
        assert res[i] == in_val[i]
    (hres,) = hip.hipFree(ptr)
    ASSERT_DRV(hres)
    (hres,) = hip.hipStreamDestroy(stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipEventDestroy(start)
    ASSERT_DRV(hres)
    (hres,) = hip.hipEventDestroy(end)
    ASSERT_DRV(hres)
