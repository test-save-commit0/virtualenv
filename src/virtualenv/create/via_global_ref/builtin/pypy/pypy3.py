from __future__ import annotations
import abc
from pathlib import Path
from virtualenv.create.describe import PosixSupports, Python3Supports, WindowsSupports
from virtualenv.create.via_global_ref.builtin.ref import PathRefToDest
from .common import PyPy


class PyPy3(PyPy, Python3Supports, abc.ABC):
    @classmethod
    def exe_stem(cls):
        return "pypy3"

    @classmethod
    def can_describe(cls, interpreter):
        return interpreter.implementation == "PyPy" and interpreter.version_info[0] == 3


class PyPy3Posix(PyPy3, PosixSupports):
    """PyPy 3 on POSIX."""
    
    @classmethod
    def sources(cls, interpreter):
        for src in super().sources(interpreter):
            yield src
        # Add POSIX-specific sources if needed
        yield PathRefToDest(interpreter.prefix / "bin" / "python3", dest=cls.bin_dir / "python")


class Pypy3Windows(PyPy3, WindowsSupports):
    """PyPy 3 on Windows."""
    
    @classmethod
    def sources(cls, interpreter):
        for src in super().sources(interpreter):
            yield src
        # Add Windows-specific sources if needed
        yield PathRefToDest(interpreter.prefix / "python.exe", dest=cls.bin_dir / "python.exe")
        yield PathRefToDest(interpreter.prefix / "pythonw.exe", dest=cls.bin_dir / "pythonw.exe")


__all__ = ['PyPy3', 'PyPy3Posix', 'Pypy3Windows']
