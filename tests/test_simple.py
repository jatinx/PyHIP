from pyhip import hip
import unittest

class TestSimple(unittest.TestCase):
    def test_verifyPlatform(self):
        plat = hip.hipGetPlatformName()
        assert plat == 'amd' or plat == 'nvidia'


    def test_errorName(self):
        error_string = hip.hipGetErrorString(1)
        self.assertNotEqual(error_string, str(''))
        error_name = hip.hipGetErrorName(1)
        self.assertNotEqual(error_name, str(''))

if __name__ == "__main__":
    unittest.main()
