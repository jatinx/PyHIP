import re
from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()
    
# Extract the version number from the package's __init__.py file
with open("pyhip/__init__.py") as fp:
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", fp.read())
    version = match.group(1)

setup(
    name='pyhip',
    version=version,
    author='Jatin Chaudhary',
    description='A Python Interface of the Heterogeneous Interface for Portability (HIP)',
    packages=['pyhip'],
    py_modules=['hip', 'hiprtc'],
    keywords='HIP GPU parallel computing scientific computing Python wrapper',
    author_email='ndjatin@gmail.com',
    project_urls={
        "Source": "https://github.com/jatinx/PyHIP"
    },
    long_description=readme(),
)