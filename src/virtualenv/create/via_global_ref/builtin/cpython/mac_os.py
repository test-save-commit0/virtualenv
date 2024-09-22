"""The Apple Framework builds require their own customization."""
from __future__ import annotations
import logging
import os
import struct
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent
from virtualenv.create.via_global_ref.builtin.ref import ExePathRefToDest, PathRefToDest, RefMust
from virtualenv.create.via_global_ref.builtin.via_global_self_do import BuiltinViaGlobalRefMeta
from .common import CPython, CPythonPosix, is_mac_os_framework, is_macos_brew
from .cpython3 import CPython3


class CPythonmacOsFramework(CPython, ABC):
    pass


class CPython3macOsFramework(CPythonmacOsFramework, CPython3, CPythonPosix):
    pass


def fix_mach_o(exe, current, new, max_size):
    """
    https://en.wikipedia.org/wiki/Mach-O.

    Mach-O, short for Mach object file format, is a file format for executables, object code, shared libraries,
    dynamically-loaded code, and core dumps. A replacement for the a.out format, Mach-O offers more extensibility and
    faster access to information in the symbol table.

    Each Mach-O file is made up of one Mach-O header, followed by a series of load commands, followed by one or more
    segments, each of which contains between 0 and 255 sections. Mach-O uses the REL relocation format to handle
    references to symbols. When looking up symbols Mach-O uses a two-level namespace that encodes each symbol into an
    'object/symbol name' pair that is then linearly searched for by first the object and then the symbol name.

    The basic structure—a list of variable-length "load commands" that reference pages of data elsewhere in the file—was
    also used in the executable file format for Accent. The Accent file format was in turn, based on an idea from Spice
    Lisp.

    With the introduction of Mac OS X 10.6 platform the Mach-O file underwent a significant modification that causes
    binaries compiled on a computer running 10.6 or later to be (by default) executable only on computers running Mac
    OS X 10.6 or later. The difference stems from load commands that the dynamic linker, in previous Mac OS X versions,
    does not understand. Another significant change to the Mach-O format is the change in how the Link Edit tables
    (found in the __LINKEDIT section) function. In 10.6 these new Link Edit tables are compressed by removing unused and
    unneeded bits of information, however Mac OS X 10.5 and earlier cannot read this new Link Edit table format.
    """
    pass


class CPython3macOsBrew(CPython3, CPythonPosix):
    pass


__all__ = ['CPython3macOsBrew', 'CPython3macOsFramework',
    'CPythonmacOsFramework']
