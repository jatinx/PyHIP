"""
Python interface to hiprtc
"""

import sys
import ctypes

_libhiprtc_libname = 'libhiprtc.so'
_libhiprtc_fallback_libname = 'libamdhip64.so'  # Fall back library
_libhiprtc_nv_libname = 'libnvhip64.so'

_libhiprtc = None
if 'linux' in sys.platform:
    try:
        _libhiprtc = ctypes.cdll.LoadLibrary(_libhiprtc_libname)
    except:
        try:
            _libhiprtc = ctypes.cdll.LoadLibrary(_libhiprtc_fallback_libname)
        except:
            _libhiprtc = ctypes.cdll.LoadLibrary(_libhiprtc_nv_libname)
    if _libhiprtc == None:
        _libhiprtc = ctypes.cdll.LoadLibrary(_libhiprtc_fallback_libname)

else:
    # Currently we do not support windows, mainly because I do not have a windows build of hip
    raise RuntimeError('Only linux is supported')

if _libhiprtc == None:
    raise OSError('hiprtc library not found')


def POINTER(obj):
    """
    ctype pointer to object
    """
    p = ctypes.POINTER(obj)
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p


_libhiprtc.hiprtcGetErrorString.restype = ctypes.c_char_p
_libhiprtc.hiprtcGetErrorString.argtypes = [ctypes.c_int]


def hiprtcGetErrorString(e):
    """
    Retrieve hiprtc error string.

    Return the string associated with the specified hiprtc error status
    code.

    Parameters
    ----------
    e : int
        Error number.

    Returns
    -------
    s : str
        Error string.

    """

    return _libhiprtc.hiprtcGetErrorString(e)

# Generic hiprtc Error


class hiprtcError(Exception):
    """hiprtc error."""
    pass


class hiprtcErrorOutOfMemory(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(1)
    pass


class hiprtcErrorProgramCreationFailure(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(2)
    pass


class hiprtcErrorInvalidInput(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(3)
    pass


class hiprtcErrorInvalidProgram(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(4)
    pass


class hiprtcErrorInvalidOption(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(5)
    pass


class hiprtcErrorCompilation(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(6)
    pass


class hiprtcErrorBuiltinOperationFailure(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(7)
    pass


class hiprtcErrorNoNameExpressionAfterCompilation(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(8)
    pass


class hiprtcErrorNoLoweredNamesBeforeCompilation(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(9)
    pass


class hiprtcErrorNameExpressionNotValid(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(10)
    pass


class hiprtcErrorInternalError(hiprtcError):
    __doc__ = _libhiprtc.hiprtcGetErrorString(11)
    pass


hiprtcExceptions = {
    1: hiprtcErrorOutOfMemory,
    2: hiprtcErrorProgramCreationFailure,
    3: hiprtcErrorInvalidInput,
    4: hiprtcErrorInvalidProgram,
    5: hiprtcErrorInvalidOption,
    6: hiprtcErrorCompilation,
    7: hiprtcErrorBuiltinOperationFailure,
    8: hiprtcErrorNoNameExpressionAfterCompilation,
    9: hiprtcErrorNoLoweredNamesBeforeCompilation,
    10: hiprtcErrorNameExpressionNotValid,
    11: hiprtcErrorInternalError
}


def hiprtcCheckStatus(status):
    if status != 0:
        try:
            e = hiprtcExceptions[status]
        except KeyError:
            raise hiprtcError('unknown hiprtc error %s' % status)
        else:
            raise e


_libhiprtc.hiprtcCreateProgram.restype = int
_libhiprtc.hiprtcCreateProgram.argtypes = [ctypes.POINTER(ctypes.c_void_p),  # hiprtcProgram
                                           ctypes.POINTER(
                                               ctypes.c_char),   # Source
                                           ctypes.POINTER(
                                               ctypes.c_char),   # Name
                                           ctypes.c_int,                    # numberOfHeaders
                                           ctypes.POINTER(
                                               ctypes.c_char_p),  # header
                                           ctypes.POINTER(ctypes.c_char_p)]  # headerNames


def hiprtcCreateProgram(source, name, header_names, header_sources):
    """
    Create hiprtcProgram

    Parameters
    ----------
    source : string
        Source in python string
    name : string
        Program name
    header_names: list of string
        list of headernames
    header_sources: list of string
        list of headernames

    Returns
    -------
    prog : ctypes pointer
        hiprtc program handle
    """

    # Encode strings to utf-8
    e_source = source.encode('utf-8')
    e_name = name.encode('utf-8')
    e_header_names = list()
    e_header_sources = list()
    for header_name in header_names:
        e_header_name = header_name.encode('utf-8')
        e_header_names.append(e_header_name)
    for header_source in header_sources:
        e_header_source = header_source.encode('utf-8')
        e_header_sources.append(e_header_source)

    prog = ctypes.c_void_p()
    c_header_names = (ctypes.c_char_p * len(e_header_names))()
    c_header_names[:] = e_header_names
    c_header_sources = (ctypes.c_char_p * len(e_header_sources))()
    c_header_sources[:] = e_header_sources

    status = _libhiprtc.hiprtcCreateProgram(ctypes.byref(
        prog), e_source, e_name, len(e_header_names), c_header_sources, c_header_names)
    hiprtcCheckStatus(status)
    return prog


_libhiprtc.hiprtcDestroyProgram.restype = int
_libhiprtc.hiprtcDestroyProgram.argtypes = [
    ctypes.POINTER(ctypes.c_void_p)]  # hiprtcProgram


def hiprtcDestroyProgram(prog):
    """
    Destroy hiprtcProgram

    Parameters
    ----------
    prog : ctypes pointer
        hiprtc program handle
    """
    status = _libhiprtc.hiprtcDestroyProgram(ctypes.byref(prog))
    hiprtcCheckStatus(status)


_libhiprtc.hiprtcAddNameExpression.restype = int
_libhiprtc.hiprtcAddNameExpression.argtypes = [ctypes.c_void_p,                 # hiprtcProgram
                                               ctypes.POINTER(ctypes.c_char)]   # expression


def hiprtcAddNameExpression(prog, expression):
    """
    Tracks expression name through hiprtc compilation unit

    Parameters
    ----------
    prog : ctypes pointer
        hiprtc program handle
    expression : string
        expression name
    """
    e_expression = expression.encode('utf-8')
    status = _libhiprtc.hiprtcAddNameExpression(prog, e_expression)
    hiprtcCheckStatus(status)


_libhiprtc.hiprtcCompileProgram.restype = int
_libhiprtc.hiprtcCompileProgram.argtypes = [ctypes.c_void_p,                 # hiprtcProgram
                                            ctypes.c_int,                    # num of options
                                            ctypes.POINTER(ctypes.c_char_p)]  # options


def hiprtcCompileProgram(prog, options):
    """
    Compiles the hiprtc program

    Parameters
    ----------
    prog : ctypes pointer
        hiprtc program handle
    options : list of string
        option list to be passed to compilation
    """

    e_options = list()
    for option in options:
        e_options.append(option.encode('utf-8'))
    c_options = (ctypes.c_char_p * len(e_options))()
    c_options[:] = e_options
    status = _libhiprtc.hiprtcCompileProgram(prog, len(c_options), c_options)
    hiprtcCheckStatus(status)


_libhiprtc.hiprtcGetProgramLogSize.restype = int
_libhiprtc.hiprtcGetProgramLogSize.argtypes = [ctypes.c_void_p,                 # hiprtcProgram
                                               ctypes.POINTER(ctypes.c_size_t)]  # Size of log
_libhiprtc.hiprtcGetProgramLog.restype = int
_libhiprtc.hiprtcGetProgramLog.argtypes = [ctypes.c_void_p,               # hiprtcProgram
                                           ctypes.POINTER(ctypes.c_char)]  # log


def hiprtcGetProgramLog(prog):
    """
    Gets the hiprtc Log

    Parameters
    ----------
    prog : ctypes pointer
        hiprtc program handle

    Returns
    -------
    log : string
        program compilation log (warnings/errors)
    """
    log_size = ctypes.c_size_t()
    status = _libhiprtc.hiprtcGetProgramLogSize(prog, ctypes.byref(log_size))
    hiprtcCheckStatus(status)

    log = "0" * log_size.value
    e_log = log.encode('utf-8')
    status = _libhiprtc.hiprtcGetProgramLog(prog, e_log)
    hiprtcCheckStatus(status)
    return e_log.decode('utf-8')


_libhiprtc.hiprtcGetCodeSize.restype = int
_libhiprtc.hiprtcGetCodeSize.argtypes = [ctypes.c_void_p,                 # hiprtcProgram
                                         ctypes.POINTER(ctypes.c_size_t)]  # Size of log
_libhiprtc.hiprtcGetCode.restype = int
_libhiprtc.hiprtcGetCode.argtypes = [ctypes.c_void_p,               # hiprtcProgram
                                     ctypes.POINTER(ctypes.c_char)]  # log


def hiprtcGetCode(prog):
    """
    Gets the hiprtc compiled code

    Parameters
    ----------
    prog : ctypes pointer
        hiprtc program handle

    Returns
    -------
    code : string
        hiprtc module code
    """
    code_size = ctypes.c_size_t()
    status = _libhiprtc.hiprtcGetCodeSize(prog, ctypes.byref(code_size))
    hiprtcCheckStatus(status)

    code = "0" * code_size.value
    e_code = code.encode('utf-8')
    status = _libhiprtc.hiprtcGetCode(prog, e_code)
    hiprtcCheckStatus(status)
    return e_code
