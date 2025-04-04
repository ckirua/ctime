# Define NPY_NO_DEPRECATED_API to disable the NumPy API deprecation warning

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

extensions = [
    Extension(
        "ctime.*",
        ["ctime/*.pyx"],
        extra_compile_args=["-O2", "-march=native", "-Wno-unused-function"],
        include_dirs=[np.get_include()],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    ),
]
setup(
    name="ctime",
    packages=["ctime"]
    + [f"ctime.{pkg}" for pkg in find_packages(where="ctime")],
    ext_modules=cythonize(
        extensions,
        build_dir="src",
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
            "infer_types": True,
        },
    ),
)
