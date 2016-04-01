from setuptools import setup

setup(
    name='fbsd_gpio',
    version='0.4.1',
    url='https://github.com/evadot/fbsd_gpio_py',
    license='BSD',
    author='Emmanuel Vadot',
    author_email='manu@bidouilliste.com',
    description='cffi-based Python bindings for FreeBSD GPIO',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='FreeBSD GPIO',
    packages=['fbsd_gpio'],
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["generate.py:ffi"],
    install_requires=['cffi'],
)
