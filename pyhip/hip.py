"""
Python interface to hip library
"""

import sys, ctypes

_libhip_libname = 'libamdhip64.so'

_libhip = None
if 'linux' in sys.platform:
    _libhip = ctypes.cdll.LoadLibrary(_libhip_libname)
else:
    # Currently we do not support windows, mainly because I do not have a windows build of hip
    raise RuntimeError('Only linux is supported')

if _libhip == None:
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

_libhip.hipGetErrorString.restype = ctypes.c_char_p
_libhip.hipGetErrorString.argtypes = [ctypes.c_int]
def hiprtcGetErrorString(e):
    """
    Retrieve hip error string.

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

    return _libhip.hipGetErrorString(e)

# Generic hip error
class hipError(Exception):
    """hip error"""
    pass

class hipErrorInvalidValue(hipError):
    __doc__ = _libhip.hipGetErrorString(1)
    pass

class hipErrorOutOfMemory(hipError):
    __doc__ = _libhip.hipGetErrorString(2)
    pass

class hipErrorNotInitialized(hipError):
    __doc__ = _libhip.hipGetErrorString(3)
    pass

class hipErrorDeinitialized(hipError):
    __doc__ = _libhip.hipGetErrorString(4)
    pass

class hipErrorProfilerDisabled(hipError):
    __doc__ = _libhip.hipGetErrorString(5)
    pass

class hipErrorProfilerNotInitialized(hipError):
    __doc__ = _libhip.hipGetErrorString(6)
    pass

class hipErrorProfilerAlreadyStarted(hipError):
    __doc__ = _libhip.hipGetErrorString(7)
    pass

class hipErrorProfilerAlreadyStopped(hipError):
    __doc__ = _libhip.hipGetErrorString(8)
    pass

class hipErrorInvalidConfiguration(hipError):
    __doc__ = _libhip.hipGetErrorString(9)
    pass

class hipErrorInvalidSymbol(hipError):
    __doc__ = _libhip.hipGetErrorString(13)
    pass

class hipErrorInvalidDevicePointer(hipError):
    __doc__ = _libhip.hipGetErrorString(17)
    pass

class hipErrorInvalidMemcpyDirection(hipError):
    __doc__ = _libhip.hipGetErrorString(21)
    pass

class hipErrorInsufficientDriver(hipError):
    __doc__ = _libhip.hipGetErrorString(35)
    pass

class hipErrorMissingConfiguration(hipError):
    __doc__ = _libhip.hipGetErrorString(52)
    pass

class hipErrorPriorLaunchFailure(hipError):
    __doc__ = _libhip.hipGetErrorString(53)
    pass

class hipErrorInvalidDeviceFunction(hipError):
    __doc__ = _libhip.hipGetErrorString(98)
    pass

class hipErrorNoDevice(hipError):
    __doc__ = _libhip.hipGetErrorString(100)
    pass

class hipErrorInvalidDevice(hipError):
    __doc__ = _libhip.hipGetErrorString(101)
    pass

class hipErrorInvalidImage(hipError):
    __doc__ = _libhip.hipGetErrorString(200)
    pass

class hipErrorInvalidContext(hipError):
    __doc__ = _libhip.hipGetErrorString(201)
    pass

class hipErrorContextAlreadyCurrent(hipError):
    __doc__ = _libhip.hipGetErrorString(202)
    pass

class hipErrorMapFailed(hipError):
    __doc__ = _libhip.hipGetErrorString(205)
    pass

class hipErrorUnmapFailed(hipError):
    __doc__ = _libhip.hipGetErrorString(206)
    pass

class hipErrorArrayIsMapped(hipError):
    __doc__ = _libhip.hipGetErrorString(207)
    pass

class hipErrorAlreadyMapped(hipError):
    __doc__ = _libhip.hipGetErrorString(208)
    pass

class hipErrorNoBinaryForGpu(hipError):
    __doc__ = _libhip.hipGetErrorString(209)
    pass

class hipErrorAlreadyAcquired(hipError):
    __doc__ = _libhip.hipGetErrorString(210)
    pass

class hipErrorNotMapped(hipError):
    __doc__ = _libhip.hipGetErrorString(211)
    pass

class hipErrorNotMappedAsArray(hipError):
    __doc__ = _libhip.hipGetErrorString(212)
    pass

class hipErrorNotMappedAsPointer(hipError):
    __doc__ = _libhip.hipGetErrorString(213)
    pass

class hipErrorECCNotCorrectable(hipError):
    __doc__ = _libhip.hipGetErrorString(214)
    pass

class hipErrorUnsupportedLimit(hipError):
    __doc__ = _libhip.hipGetErrorString(215)
    pass

class hipErrorContextAlreadyInUse(hipError):
    __doc__ = _libhip.hipGetErrorString(216)
    pass

class hipErrorPeerAccessUnsupported(hipError):
    __doc__ = _libhip.hipGetErrorString(217)
    pass

class hipErrorInvalidKernelFile(hipError):
    __doc__ = _libhip.hipGetErrorString(218)
    pass

class hipErrorInvalidGraphicsContext(hipError):
    __doc__ = _libhip.hipGetErrorString(219)
    pass

class hipErrorInvalidSource(hipError):
    __doc__ = _libhip.hipGetErrorString(300)
    pass

class hipErrorFileNotFound(hipError):
    __doc__ = _libhip.hipGetErrorString(301)
    pass

class hipErrorSharedObjectSymbolNotFound(hipError):
    __doc__ = _libhip.hipGetErrorString(302)
    pass

class hipErrorSharedObjectInitFailed(hipError):
    __doc__ = _libhip.hipGetErrorString(303)
    pass

class hipErrorOperatingSystem(hipError):
    __doc__ = _libhip.hipGetErrorString(304)
    pass

class hipErrorInvalidHandle(hipError):
    __doc__ = _libhip.hipGetErrorString(400)
    pass

class hipErrorNotFound(hipError):
    __doc__ = _libhip.hipGetErrorString(500)
    pass

class hipErrorNotReady(hipError):
    __doc__ = _libhip.hipGetErrorString(600)
    pass

class hipErrorIllegalAddress(hipError):
    __doc__ = _libhip.hipGetErrorString(700)
    pass

class hipErrorLaunchOutOfResources(hipError):
    __doc__ = _libhip.hipGetErrorString(701)
    pass

class hipErrorLaunchTimeOut(hipError):
    __doc__ = _libhip.hipGetErrorString(702)
    pass

class hipErrorPeerAccessAlreadyEnabled(hipError):
    __doc__ = _libhip.hipGetErrorString(704)
    pass

class hipErrorPeerAccessNotEnabled(hipError):
    __doc__ = _libhip.hipGetErrorString(705)
    pass

class hipErrorSetOnActiveProcess(hipError):
    __doc__ = _libhip.hipGetErrorString(708)
    pass

class hipErrorAssert(hipError):
    __doc__ = _libhip.hipGetErrorString(710)
    pass

class hipErrorHostMemoryAlreadyRegistered(hipError):
    __doc__ = _libhip.hipGetErrorString(712)
    pass

class hipErrorHostMemoryNotRegistered(hipError):
    __doc__ = _libhip.hipGetErrorString(713)
    pass

class hipErrorLaunchFailure(hipError):
    __doc__ = _libhip.hipGetErrorString(719)
    pass

class hipErrorCooperativeLaunchTooLarge(hipError):
    __doc__ = _libhip.hipGetErrorString(720)
    pass

class hipErrorNotSupported(hipError):
    __doc__ = _libhip.hipGetErrorString(801)
    pass

class hipErrorUnknown(hipError):
    __doc__ = _libhip.hipGetErrorString(999)
    pass

class hipErrorRuntimeMemory(hipError):
    __doc__ = _libhip.hipGetErrorString(1052)
    pass

class hipErrorRuntimeOther(hipError):
    __doc__ = _libhip.hipGetErrorString(1053)
    pass


hipExceptions = {
    1: hipErrorInvalidValue,
    2: hipErrorOutOfMemory,
    3: hipErrorNotInitialized,
    4: hipErrorDeinitialized,
    5: hipErrorProfilerDisabled,
    6: hipErrorProfilerNotInitialized,
    7: hipErrorProfilerAlreadyStarted,
    8: hipErrorProfilerAlreadyStopped,
    9: hipErrorInvalidConfiguration,
    13: hipErrorInvalidSymbol,
    17: hipErrorInvalidDevicePointer,
    21: hipErrorInvalidMemcpyDirection,
    35: hipErrorInsufficientDriver,
    52: hipErrorMissingConfiguration,
    53: hipErrorPriorLaunchFailure,
    98: hipErrorInvalidDeviceFunction,
    100: hipErrorNoDevice,
    101: hipErrorInvalidDevice,
    200: hipErrorInvalidImage,
    201: hipErrorInvalidContext,
    202: hipErrorContextAlreadyCurrent,
    205: hipErrorMapFailed,
    206: hipErrorUnmapFailed,
    207: hipErrorArrayIsMapped,
    208: hipErrorAlreadyMapped,
    209: hipErrorNoBinaryForGpu,
    210: hipErrorAlreadyAcquired,
    211: hipErrorNotMapped,
    212: hipErrorNotMappedAsArray,
    213: hipErrorNotMappedAsPointer,
    214: hipErrorECCNotCorrectable,
    215: hipErrorUnsupportedLimit,
    216: hipErrorContextAlreadyInUse,
    217: hipErrorPeerAccessUnsupported,
    218: hipErrorInvalidKernelFile,
    219: hipErrorInvalidGraphicsContext,
    300: hipErrorInvalidSource,
    301: hipErrorFileNotFound,
    302: hipErrorSharedObjectSymbolNotFound,
    303: hipErrorSharedObjectInitFailed,
    304: hipErrorOperatingSystem,
    400: hipErrorInvalidHandle,
    500: hipErrorNotFound,
    600: hipErrorNotReady,
    700: hipErrorIllegalAddress,
    701: hipErrorLaunchOutOfResources,
    702: hipErrorLaunchTimeOut,
    704: hipErrorPeerAccessAlreadyEnabled,
    705: hipErrorPeerAccessNotEnabled,
    708: hipErrorSetOnActiveProcess,
    710: hipErrorAssert,
    712: hipErrorHostMemoryAlreadyRegistered,
    713: hipErrorHostMemoryNotRegistered,
    719: hipErrorLaunchFailure,
    720: hipErrorCooperativeLaunchTooLarge,
    801: hipErrorNotSupported,
    999: hipErrorUnknown,
    1052: hipErrorRuntimeMemory,
    1053: hipErrorRuntimeOther
    }

def hipCheckStatus(status):
    """
    Raise hip exception.

    Raise an exception corresponding to the specified hip runtime error
    code.

    Parameters
    ----------
    status : int
        hip runtime error code.

    See Also
    --------
    hipExceptions
    """

    if status != 0:
        try:
            e = hipExceptions[status]
        except KeyError:
            raise hipError('unknown hip error %s' % status)
        else:
            raise e

# Memory allocation functions (adapted from pystream):
_libhip.hipMalloc.restype = int
_libhip.hipMalloc.argtypes = [ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.c_size_t]
def hipMalloc(count, ctype=None):
    """
    Allocate device memory.

    Allocate memory on the device associated with the current active
    context.

    Parameters
    ----------
    count : int
        Number of bytes of memory to allocate
    ctype : _ctypes.SimpleType, optional
        ctypes type to cast returned pointer.

    Returns
    -------
    ptr : ctypes pointer
        Pointer to allocated device memory.

    """

    ptr = ctypes.c_void_p()
    status = _libhip.hipMalloc(ctypes.byref(ptr), count)
    hipCheckStatus(status)
    if ctype != None:
        ptr = ctypes.cast(ptr, ctypes.POINTER(ctype))
    return ptr

_libhip.hipFree.restype = int
_libhip.hipFree.argtypes = [ctypes.c_void_p]
def hipFree(ptr):
    """
    Free device memory.

    Free allocated memory on the device associated with the current active
    context.

    Parameters
    ----------
    ptr : ctypes pointer
        Pointer to allocated device memory.

    """

    status = _libhip.hipFree(ptr)
    hipCheckStatus(status)

_libhip.hipMallocPitch.restype = int
_libhip.hipMallocPitch.argtypes = [ctypes.POINTER(ctypes.c_void_p),
                                       ctypes.POINTER(ctypes.c_size_t),
                                       ctypes.c_size_t, ctypes.c_size_t]
def hipMallocPitch(pitch, rows, cols, elesize):
    """
    Allocate pitched device memory.

    Allocate pitched memory on the device associated with the current active
    context.

    Parameters
    ----------
    pitch : int
        Pitch for allocation.
    rows : int
        Requested pitched allocation height.
    cols : int
        Requested pitched allocation width.
    elesize : int
        Size of memory element.

    Returns
    -------
    ptr : ctypes pointer
        Pointer to allocated device memory.

    """

    ptr = ctypes.c_void_p()
    status = _libhip.hipMallocPitch(ctypes.byref(ptr),
                                        ctypes.c_size_t(pitch), cols*elesize,
                                        rows)
    hipCheckStatus(status)
    return ptr, pitch

# Memory copy modes:
hipMemcpyHostToHost = 0
hipMemcpyHostToDevice = 1
hipMemcpyDeviceToHost = 2
hipMemcpyDeviceToDevice = 3
hipMemcpyDefault = 4

_libhip.hipMemcpy.restype = int
_libhip.hipMemcpy.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                  ctypes.c_size_t, ctypes.c_int]
def hipMemcpy_htod(dst, src, count):
    """
    Copy memory from host to device.

    Copy data from host memory to device memory.

    Parameters
    ----------
    dst : ctypes pointer
        Device memory pointer.
    src : ctypes pointer
        Host memory pointer.
    count : int
        Number of bytes to copy.

    """

    status = _libhip.hipMemcpy(dst, src,
                                   ctypes.c_size_t(count),
                                   hipMemcpyHostToDevice)
    hipCheckStatus(status)

def hipMemcpy_dtoh(dst, src, count):
    """
    Copy memory from device to host.

    Copy data from device memory to host memory.

    Parameters
    ----------
    dst : ctypes pointer
        Host memory pointer.
    src : ctypes pointer
        Device memory pointer.
    count : int
        Number of bytes to copy.

    """

    status = _libhip.hipMemcpy(dst, src,
                                   ctypes.c_size_t(count),
                                   hipMemcpyDeviceToHost)
    hipCheckStatus(status)

_libhip.hipMemGetInfo.restype = int
_libhip.hipMemGetInfo.argtypes = [ctypes.c_void_p,
                                      ctypes.c_void_p]
def hipMemGetInfo():
    """
    Return the amount of free and total device memory.

    Returns
    -------
    free : long
        Free memory in bytes.
    total : long
        Total memory in bytes.

    """

    free = ctypes.c_size_t()
    total = ctypes.c_size_t()
    status = _libhip.hipMemGetInfo(ctypes.byref(free),
                                       ctypes.byref(total))
    hipCheckStatus(status)
    return free.value, total.value

_libhip.hipSetDevice.restype = int
_libhip.hipSetDevice.argtypes = [ctypes.c_int]
def hipSetDevice(dev):
    """
    Set current hip device.

    Select a device to use for subsequent hip operations.

    Parameters
    ----------
    dev : int
        Device number.

    """

    status = _libhip.hipSetDevice(dev)
    hipCheckStatus(status)

_libhip.hipGetDevice.restype = int
_libhip.hipGetDevice.argtypes = [ctypes.POINTER(ctypes.c_int)]
def hipGetDevice():
    """
    Get current hip device.

    Return the identifying number of the device currently used to
    process hip operations.

    Returns
    -------
    dev : int
        Device number.

    """

    dev = ctypes.c_int()
    status = _libhip.hipGetDevice(ctypes.byref(dev))
    hipCheckStatus(status)
    return dev.value


class hipDeviceArch(ctypes.Structure):
    _fields_ = [
        # *32-bit Atomics*
        # 32-bit integer atomics for global memory.
        ('hasGlobalInt32Atomics', ctypes.c_uint, 1),

        # 32-bit float atomic exch for global memory.
        ('hasGlobalFloatAtomicExch', ctypes.c_uint, 1),

        # 32-bit integer atomics for shared memory.
        ('hasSharedInt32Atomics', ctypes.c_uint, 1),

        # 32-bit float atomic exch for shared memory.
        ('hasSharedFloatAtomicExch', ctypes.c_uint, 1),

        # 32-bit float atomic add in global and shared memory.
        ('hasFloatAtomicAdd', ctypes.c_uint, 1),

        # *64-bit Atomics*
        # 64-bit integer atomics for global memory.
        ('hasGlobalInt64Atomics', ctypes.c_uint, 1),

        # 64-bit integer atomics for shared memory.
        ('hasSharedInt64Atomics', ctypes.c_uint, 1),

        # *Doubles*
        # Double-precision floating point.
        ('hasDoubles', ctypes.c_uint, 1),

        # *Warp cross-lane operations*
        # Warp vote instructions (__any, __all).
        ('hasWarpVote', ctypes.c_uint, 1),

        # Warp ballot instructions (__ballot).
        ('hasWarpBallot', ctypes.c_uint, 1),

        # Warp shuffle operations. (__shfl_*).
        ('hasWarpShuffle', ctypes.c_uint, 1),

        # Funnel two words into one with shift&mask caps.
        ('hasFunnelShift', ctypes.c_uint, 1),

        # *Sync*
        # __threadfence_system.
        ('hasThreadFenceSystem', ctypes.c_uint, 1),

        # __syncthreads_count, syncthreads_and, syncthreads_or.
        ('hasSyncThreadsExt', ctypes.c_uint, 1),

        # *Misc*
        # Surface functions.
        ('hasSurfaceFuncs', ctypes.c_uint, 1),

        # Grid and group dims are 3D (rather than 2D).
        ('has3dGrid', ctypes.c_uint, 1),

        # Dynamic parallelism.
        ('hasDynamicParallelism', ctypes.c_uint, 1),
    ]


class hipDeviceProperties(ctypes.Structure):
    _fields_ = [
        # Device name
        ('_name', ctypes.c_char * 256),

        # Size of global memory region (in bytes)
        ('totalGlobalMem', ctypes.c_size_t),

        # Size of shared memory region (in bytes).
        ('sharedMemPerBlock', ctypes.c_size_t),

        # Registers per block.
        ('regsPerBlock', ctypes.c_int),

        # Warp size.
        ('warpSize', ctypes.c_int),

        # Max work items per work group or workgroup max size.
        ('maxThreadsPerBlock', ctypes.c_int),

        # Max number of threads in each dimension (XYZ) of a block.
        ('maxThreadsDim', ctypes.c_int * 3),

        # Max grid dimensions (XYZ).
        ('maxGridSize', ctypes.c_int * 3),

        # Max clock frequency of the multiProcessors in khz.
        ('clockRate', ctypes.c_int),

        # Max global memory clock frequency in khz.
        ('memoryClockRate', ctypes.c_int),

        # Global memory bus width in bits.
        ('memoryBusWidth', ctypes.c_int),

        # Size of shared memory region (in bytes).
        ('totalConstMem', ctypes.c_size_t),

        # Major compute capability.  On HCC, this is an approximation and features may
        # differ from CUDA CC.  See the arch feature flags for portable ways to query
        # feature caps.
        ('major', ctypes.c_int),

        # Minor compute capability.  On HCC, this is an approximation and features may
        # differ from CUDA CC.  See the arch feature flags for portable ways to query
        # feature caps.
        ('minor', ctypes.c_int),

        # Number of multi-processors (compute units).
        ('multiProcessorCount', ctypes.c_int),

        # L2 cache size.
        ('l2CacheSize', ctypes.c_int),

        # Maximum resident threads per multi-processor.
        ('maxThreadsPerMultiProcessor', ctypes.c_int),

        # Compute mode.
        ('computeMode', ctypes.c_int),

        # Frequency in khz of the timer used by the device-side "clock*"
        # instructions.  New for HIP.
        ('clockInstructionRate', ctypes.c_int),

        # Architectural feature flags.  New for HIP.
        ('arch', hipDeviceArch),

        # Device can possibly execute multiple kernels concurrently.
        ('concurrentKernels', ctypes.c_int),

        # PCI Domain ID
        ('pciDomainID', ctypes.c_int),

        # PCI Bus ID.
        ('pciBusID', ctypes.c_int),

        # PCI Device ID.
        ('pciDeviceID', ctypes.c_int),

        # Maximum Shared Memory Per Multiprocessor.
        ('maxSharedMemoryPerMultiProcessor', ctypes.c_size_t),

        # 1 if device is on a multi-GPU board, 0 if not.
        ('isMultiGpuBoard', ctypes.c_int),

        # Check whether HIP can map host memory
        ('canMapHostMemory', ctypes.c_int),

        # DEPRECATED: use gcnArchName instead
        ('gcnArch', ctypes.c_int),

        # AMD GCN Arch Name.
        ('_gcnArchName', ctypes.c_char * 256),

        # APU vs dGPU
        ('integrated', ctypes.c_int),

        # HIP device supports cooperative launch
        ('cooperativeLaunch', ctypes.c_int),

        # HIP device supports cooperative launch on multiple devices
        ('cooperativeMultiDeviceLaunch', ctypes.c_int),

        # Maximum size for 1D textures bound to linear memory
        ('maxTexture1DLinear', ctypes.c_int),

        # Maximum number of elements in 1D images
        ('maxTexture1D', ctypes.c_int),

        # Maximum dimensions (width, height) of 2D images, in image elements
        ('maxTexture2D', ctypes.c_int * 2),

        # Maximum dimensions (width, height, depth) of 3D images, in image elements
        ('maxTexture3D', ctypes.c_int * 3),

        # Addres of HDP_MEM_COHERENCY_FLUSH_CNTL register
        ('hdpMemFlushCntl', POINTER(ctypes.c_uint)),

        # Addres of HDP_REG_COHERENCY_FLUSH_CNTL register
        ('hdpRegFlushCntl', POINTER(ctypes.c_uint)),

        # Maximum pitch in bytes allowed by memory copies
        ('memPitch', ctypes.c_size_t),

        # Alignment requirement for textures
        ('textureAlignment', ctypes.c_size_t),

        # Pitch alignment requirement for texture references bound to pitched memory
        ('texturePitchAlignment', ctypes.c_size_t),

        # Run time limit for kernels executed on the device
        ('kernelExecTimeoutEnabled', ctypes.c_int),

        # Device has ECC support enabled
        ('ECCEnabled', ctypes.c_int),

        # 1:If device is Tesla device using TCC driver, else 0
        ('tccDriver', ctypes.c_int),

        # HIP device supports cooperative launch on multiple
        # devices with unmatched functions
        ('cooperativeMultiDeviceUnmatchedFunc', ctypes.c_int),

        # HIP device supports cooperative launch on multiple
        # devices with unmatched grid dimensions
        ('cooperativeMultiDeviceUnmatchedGridDim', ctypes.c_int),

        # HIP device supports cooperative launch on multiple
        # devices with unmatched block dimensions
        ('cooperativeMultiDeviceUnmatchedBlockDim', ctypes.c_int),

        # HIP device supports cooperative launch on multiple
        # devices with unmatched shared memories
        ('cooperativeMultiDeviceUnmatchedSharedMem', ctypes.c_int),

        # 1: if it is a large PCI bar device, else 0
        ('isLargeBar', ctypes.c_int),

        # Revision of the GPU in this device
        ('asicRevision', ctypes.c_int),

        # Device supports allocating managed memory on this system
        ('managedMemory', ctypes.c_int),

        # Host can directly access managed memory on the device without migration
        ('directManagedMemAccessFromHost', ctypes.c_int),

        # Device can coherently access managed memory concurrently with the CPU
        ('concurrentManagedAccess', ctypes.c_int),

        # Device supports coherently accessing pageable memory
        # without calling hipHostRegister on it
        ('pageableMemoryAccess', ctypes.c_int),

        # Device accesses pageable memory via the host's page tables
        ('pageableMemoryAccessUsesHostPageTables', ctypes.c_int),
    ]

    @property
    def name(self):
        return self._name.decode('utf-8')

    @property
    def gcnArchName(self):
        return self._gcnArchName.decode('utf-8')


_libhip.hipGetDeviceProperties.restype = int
_libhip.hipGetDeviceProperties.argtypes = [POINTER(hipDeviceProperties), ctypes.c_int]
def hipGetDeviceProperties(deviceId: int):
    """
    Populates hipGetDeviceProperties with information for the specified device.
    Returns device properties of the specified device.
    Parameters
    ----------
    deviceId : int
        Which device to query for information
    Returns
    -------
    device_properties : hipDeviceProperties
       Information for the specified device
    """
    device_properties = hipDeviceProperties()
    status = _libhip.hipGetDeviceProperties(ctypes.pointer(device_properties),
                                            deviceId)
    hipCheckStatus(status)
    return device_properties


# Memory types:
hipMemoryTypeHost = 1
hipMemoryTypeDevice = 2
hipMemoryTypeArray = 3
hipMemoryTypeUnified = 4  # Not used currently

class hipPointerAttributes(ctypes.Structure):
    _fields_ = [
        ('memoryType', ctypes.c_int),
        ('device', ctypes.c_int),
        ('devicePointer', ctypes.c_void_p),
        ('hostPointer', ctypes.c_void_p)
        ]

_libhip.hipPointerGetAttributes.restype = int
_libhip.hipPointerGetAttributes.argtypes = [ctypes.c_void_p,
                                                ctypes.c_void_p]
def hipPointerGetAttributes(ptr):
    """
    Get memory pointer attributes.

    Returns attributes of the specified pointer.

    Parameters
    ----------
    ptr : ctypes pointer
        Memory pointer to examine.

    Returns
    -------
    memory_type : int
        Memory type; 1 indicates host memory, 2 indicates device
        memory.
    device : int
        Number of device associated with pointer.
    """

    attributes = hipPointerAttributes()
    status = \
        _libhip.hipPointerGetAttributes(ctypes.byref(attributes), ptr)
    hipCheckStatus(status)
    return attributes.memoryType, attributes.device

_libhip.hipModuleLoadData.restype = int
_libhip.hipModuleLoadData.argtypes = [ctypes.POINTER(ctypes.c_void_p), # Module
                                      ctypes.c_void_p]                 # Image
def hipModuleLoadData(data):
    """
    Load hip module data

    Parameters
    ----------
    data : ctypes pointer
        Memory pointer to load.

    Returns
    -------
    module : ctypes ptr
        hip module
    """

    module = ctypes.c_void_p()
    status = _libhip.hipModuleLoadData(ctypes.byref(module), data)
    hipCheckStatus(status)
    return module


_libhip.hipModuleGetFunction.restype = int
_libhip.hipModuleGetFunction.argtypes = [ctypes.POINTER(ctypes.c_void_p), # Kernel
                                      ctypes.c_void_p,                    # Module
                                      ctypes.POINTER(ctypes.c_char)]      # kernel name
def hipModuleGetFunction(module, func_name):
    """
    gets the kernel from module

    Parameters
    ----------
    module : ctypes ptr
        pointer to created module
    func_name : string
        name of function to be retrived from module

    Returns
    -------
    kernel : ctypes ptr
        pointer to kernel type
    """
    e_func_name = func_name.encode('utf-8')
    kernel = ctypes.c_void_p()
    status = _libhip.hipModuleGetFunction(ctypes.byref(kernel), module, e_func_name)
    hipCheckStatus(status)
    return kernel

_libhip.hipModuleUnload.restype = int
_libhip.hipModuleUnload.argtypes = [ctypes.c_void_p]
def hipModuleUnload(module):
    """
    gets the kernel from module

    Parameters
    ----------
    module : ctypes ptr
        pointer to created module
    """
    status = _libhip.hipModuleUnload(module)
    hipCheckStatus(status)

_libhip.hipModuleLaunchKernel.restype = int
_libhip.hipModuleLaunchKernel.argtypes = [ctypes.c_void_p,                 # kernel
                                          ctypes.c_uint,                   # block x
                                          ctypes.c_uint,                   # block y
                                          ctypes.c_uint,                   # block z
                                          ctypes.c_uint,                   # thread x
                                          ctypes.c_uint,                   # thread y
                                          ctypes.c_uint,                   # thread z
                                          ctypes.c_uint,                   # shared mem
                                          ctypes.c_void_p,                 # stream
                                          ctypes.POINTER(ctypes.c_void_p), # kernel params
                                          ctypes.POINTER(ctypes.c_void_p)] # extra
def hipModuleLaunchKernel(kernel, bx, by, bz, tx, ty, tz, shared, stream, struct):
    """
    Launch the kernel

    Parameters
    ----------
    kernel : ctypes ptr
        kernel from loaded module
    bx : int
        dim x
    by : int
        dim y
    bz : int
        dim z
    tx : int
        dim x
    ty : int
        dim y
    tz : int
        dim z
    shared : int
        shared mem
    stream : ctype void ptr
        stream object
    struct : ctypes structure
        struct of packed up arguments of kernel
    """
    c_bx = ctypes.c_uint(bx)
    c_by = ctypes.c_uint(by)
    c_bz = ctypes.c_uint(bz)
    c_tx = ctypes.c_uint(tx)
    c_ty = ctypes.c_uint(ty)
    c_tz = ctypes.c_uint(tz)
    c_shared = ctypes.c_uint(shared)

    ctypes.sizeof(struct)
    hip_launch_param_buffer_ptr = ctypes.c_void_p(1)
    hip_launch_param_buffer_size = ctypes.c_void_p(2)
    hip_launch_param_buffer_end = ctypes.c_void_p(3)
    size = ctypes.c_size_t(ctypes.sizeof(struct))
    p_size = ctypes.c_void_p(ctypes.addressof(size))
    p_struct = ctypes.c_void_p(ctypes.addressof(struct))
    config = (ctypes.c_void_p * 5)(hip_launch_param_buffer_ptr, p_struct, hip_launch_param_buffer_size, p_size, hip_launch_param_buffer_end)
    nullptr = ctypes.POINTER(ctypes.c_void_p)(ctypes.c_void_p(0))

    status = _libhip.hipModuleLaunchKernel(kernel, c_bx, c_by, c_bz, c_tx, c_ty, c_tz, c_shared, stream, None, config)
    hipCheckStatus(status)

_libhip.hipDeviceSynchronize.restype = int
_libhip.hipDeviceSynchronize.argtypes = []
def hipDeviceSynchronize():
    """
    Device level sync
    """
    status = _libhip.hipDeviceSynchronize()
    hipCheckStatus(status)


_libhip.hipInit.restype = int
_libhip.hipInit.argtypes = [ctypes.c_uint]  # flags
def hipInit(flags):
    """
    Explicitly initializes the HIP runtime.

    Most HIP APIs implicitly initialize the HIP runtime.
    This API provides control over the timing of the initialization.

    Parameters
    ----------
    flags : int
    """
    c_flags = ctypes.c_uint(flags)
    status = _libhip.hipInit(c_flags)
    hipCheckStatus(status)
