from __future__ import annotations
import abc
from pathlib import Path
from virtualenv.create.describe import PosixSupports, Python3Supports, WindowsSupports
from virtualenv.create.via_global_ref.builtin.ref import PathRefToDest
from .common import PyPy


class PyPy3(PyPy, Python3Supports, abc.ABC):
    pass


class PyPy3Posix(PyPy3, PosixSupports):
    """PyPy 3 on POSIX."""


class Pypy3Windows(PyPy3, WindowsSupports):
    """PyPy 3 on Windows."""


__all__ = ['PyPy3', 'PyPy3Posix', 'Pypy3Windows']
