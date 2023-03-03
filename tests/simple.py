from pyhip import hip


def test_verifyPlatform():
    plat = hip.hipGetPlatformName()
    assert plat == 'amd' or plat == 'nvidia'


def test_errorName():
    error_string = hip.hipGetErrorString(1)
    assert error_string != str('')
    error_name = hip.hipGetErrorName(1)
    assert error_name != str('')
