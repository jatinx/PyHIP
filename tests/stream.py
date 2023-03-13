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
    for i in range(count):
        res[i] = i + 1
    return res


def create_res_array(count):
    res = (ctypes.c_int * count)()
    for i in range(count):
        res[i] = 0
    return res


def test_hipStreamCreation():
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
    (hres,) = hip.hipMemcpyAsync_htod(ptr, in_val, size, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipMemcpyAsync_dtoh(res, ptr, size, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipStreamSynchronize(stream)
    ASSERT_DRV(hres)
    for i in repeat(0, count):
        assert res[i] == in_val[i]
    (hres,) = hip.hipFree(ptr)
    ASSERT_DRV(hres)
    (hres,) = hip.hipStreamDestroy(stream)
    ASSERT_DRV(hres)
