from setuptools import setup

setup(
    name='renderlib',
    version='0.1.8',
    packages=['renderlib'],
    setup_requires=['cffi>=1.0.0', 'matlib>=0.1.7'],
    cffi_modules=['build.py:ffi'],
    install_requires=['cffi>=1.0.0', 'matlib>=0.1.7'],

    # metadata for PyPI
    author='Ivan Nikolaev',
    author_email='voidexp@gmail.com',
    description='Python wrapper for renderlib C library',
    license='BSD',
    keywords='3D OpenGL game rendering engine',
    url='https://github.com/RookieGameDevs/renderlib-python')

