from pyhip import hip, hiprtc
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


def test_hipMalloc():
    (hres, ptr) = hip.hipMalloc(4)
    ASSERT_DRV(hres)
    assert ptr != None
    (hres,) = hip.hipFree(ptr)
    ASSERT_DRV(hres)


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
    (hres, ptr) = hip.hipMalloc(size)
    ASSERT_DRV(hres)
    print(ptr)
    assert ptr != None
    res = create_array(count)
    (hres,) = hip.hipMemcpy_htod(ptr, ctypes.byref(res), size)
    ASSERT_DRV(hres)
    res1 = (ctypes.c_int * count)()
    (hres,) = hip.hipMemcpy_dtoh(ctypes.byref(res1), ptr, size)
    ASSERT_DRV(hres)
    for i in repeat(0, count):
        assert res[i] == res1[i]


def test_hipMemcpyAsync():
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
    (hres,) = hip.hipMemcpyAsync(
        ptr, in_val, size, hip.hipMemcpyKind.hipMemcpyHostToDevice, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipMemcpyAsync(
        res, ptr, size, hip.hipMemcpyKind.hipMemcpyDeviceToHost, stream)
    ASSERT_DRV(hres)
    (hres,) = hip.hipStreamSynchronize(stream)
    ASSERT_DRV(hres)
    for i in repeat(0, count):
        assert res[i] == in_val[i]
    (hres,) = hip.hipFree(ptr)
    ASSERT_DRV(hres)
    (hres,) = hip.hipStreamDestroy(stream)
    ASSERT_DRV(hres)
