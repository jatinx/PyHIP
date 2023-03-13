from pyhip import hip, hiprtc


def ASSERT_DRV(err):
    if isinstance(err, hip.hipError):
        if err != hip.hipError.hipSuccess:
            raise RuntimeError("HIP Error: {}".format(err))
    elif isinstance(err, hiprtc.hiprtcError):
        if err != hiprtc.hiprtcError.hiprtcSuccess:
            raise RuntimeError("HIPRTC Error: {}".format(err))
    else:
        raise RuntimeError("Unknown error type: {}".format(err))


def test_hipGetDeviceCount():
    (hres, device_count) = hip.hipGetDeviceCount()
    ASSERT_DRV(hres)
    assert device_count != 0


def test_hipDeviceGetAttribute():
    (hres, device_count) = hip.hipGetDeviceCount()
    ASSERT_DRV(hres)
    assert device_count != 0
    for i in range(0, device_count):
        (hres, major) = hip.hipDeviceGetAttribute(
            hip.hipDeviceAttributeComputeCapabilityMajor, i)
        ASSERT_DRV(hres)
        (hres, minor) = hip.hipDeviceGetAttribute(
            hip.hipDeviceAttributeComputeCapabilityMinor, i)
        ASSERT_DRV(hres)
        assert major != 0
        assert minor != 0


def test_hipDeviceSetLimit():
    (hres, device_count) = hip.hipGetDeviceCount()
    ASSERT_DRV(hres)
    assert device_count != 0
    for _ in range(0, device_count):
        (hres, ) = hip.hipDeviceSetLimit(hip.hipLimitMallocHeapSize, 0)
        ASSERT_DRV(hres)


def test_hipVersion():
    (hres, driver_version) = hip.hipDriverGetVersion()
    ASSERT_DRV(hres)
    assert driver_version != 0
    (hres, runtime_version) = hip.hipRuntimeGetVersion()
    ASSERT_DRV(hres)
    runtime_version != 0
