from pyhip import hip
import sys
import unittest


class TestDevice(unittest.TestCase):
    def test_hipGetDeviceCount(self):
        device_count = hip.hipGetDeviceCount()
        self.assertNotEqual(device_count, 0)

    def test_hipDeviceGetAttribute(self):
        device_count = hip.hipGetDeviceCount()
        self.assertNotEqual(device_count, 0)
        for i in range(0, device_count):
            major = hip.hipDeviceGetAttribute(
                hip.hipDeviceAttributeComputeCapabilityMajor, i
            )
            self.assertNotEqual(major, 0)
            # Do not check minor since minor can be 0, for example gfx1100

    @unittest.skipIf(hip.hipDriverGetVersion() >= 50200000, "Mostly unsupported API on AMDGPUs")
    def test_hipDeviceSetLimit(self):
        device_count = hip.hipGetDeviceCount()
        self.assertNotEqual(device_count, 0)
        for _ in range(0, device_count):
            hip.hipDeviceSetLimit(hip.hipLimitMallocHeapSize, 0)

    def test_hipVersion(self):
        driver_version = hip.hipDriverGetVersion()
        self.assertNotEqual(driver_version, 0)
        runtime_version = hip.hipRuntimeGetVersion()
        runtime_version != 0


if __name__ == "__main__":
    unittest.main()
