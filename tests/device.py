from pyhip import hip


def test_hipGetDeviceCount():
    device_count = hip.hipGetDeviceCount()
    assert device_count != 0


def test_hipDeviceGetAttribute():
    device_count = hip.hipGetDeviceCount()
    assert device_count != 0
    for i in range(0, device_count):
        major = hip.hipDeviceGetAttribute(
            hip.hipDeviceAttributeComputeCapabilityMajor, i)
        minor = hip.hipDeviceGetAttribute(
            hip.hipDeviceAttributeComputeCapabilityMinor, i)
        assert major != 0
        assert minor != 0


def test_hipDeviceSetLimit():
    device_count = hip.hipGetDeviceCount()
    assert device_count != 0
    for _ in range(0, device_count):
        hip.hipDeviceSetLimit(hip.hipLimitMallocHeapSize, 0)


def test_hipVersion():
    driver_version = hip.hipDriverGetVersion()
    assert driver_version != 0
    runtime_version = hip.hipRuntimeGetVersion()
    runtime_version != 0
