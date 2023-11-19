from pyhip import hip, hiprtc
import ctypes
from itertools import repeat
import unittest
import pytest


class TestExceptions(unittest.TestCase):
    def test_hipStreamDestroyNull(self):
        with pytest.raises(Exception):
            hip.hipStreamDestroy(None)

    def test_hiprtcDestroyProgramNull(self):
        with pytest.raises(Exception):
            prog = ctypes.c_void_p()
            hiprtc.hiprtcAddNameExpression(prog, "")


if __name__ == "__main__":
    unittest.main()
