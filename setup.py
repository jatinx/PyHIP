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
    name='pyhip-interface',
    version=version,
    author='Jatin Chaudhary',
    description='Python Interface to HIP and hiprtc Library',
    packages=['pyhip'],
    py_modules=['hip', 'hiprtc'],
    keywords='HIP GPU parallel computing scientific computing Python wrapper',
    author_email='ndjatin@gmail.com',
    project_urls={
        "Source": "https://github.com/jatinx/PyHIP"
    },
    long_description=readme(),
    long_description_content_type='text/markdown',
)