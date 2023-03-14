# PyHIP - Python Interface of [HIP](https://github.com/ROCm-Developer-Tools/HIP)

## Warning: This is a test branch to try out compatibility with CUDA Python

## Introduction

This small python lib which hooks into HIP library and provides pythonic interface to it.

There are two parts of it, hip library and hiprtc library.

## Testing

Testing is in it's infancy. I'll try to add more as and when I get some time. Any help here is appreciated :)

### How to run tests

Make sure you have ```pytest``` package installed.

From the project folder run ```pytest ./tests/* -v -r A```

## Help needed

If you are an opensource developer and want to contribute to this project, I can use your help in several places depending on your skillset.

- Packaging and release (to be able to install on machines via pip)
- Adding more tests to the project
- Adding API documentation and samples
- Improving HIP API coverage - adding meaningful APIs instead of direct mapping.

## Common Problems

- Unable to load hip or hiprtc library - OSError: libamdhip64.so: cannot open shared object file: No such file or directory.

- Make sure that LD_LIBRARY_PATH has hip path on it (/opt/rocm/lib or a custom installation path)

- Getting error and need to debug

- Set AMD_LOG_LEVEL=7 for maximum verbosity of HIP APIs (this only works on amd platform).
