from pyhip import hip


def test_verifyPlatform():
    plat = hip.hipGetPlatformName()
    assert plat == 'amd' or plat == 'nvidia'
