from __future__ import annotations
import logging
import os
import platform
import sys
import tempfile
IMPLEMENTATION = platform.python_implementation()
IS_PYPY = IMPLEMENTATION == 'PyPy'
IS_CPYTHON = IMPLEMENTATION == 'CPython'
IS_WIN = sys.platform == 'win32'
IS_MAC_ARM64 = sys.platform == 'darwin' and platform.machine() == 'arm64'
ROOT = os.path.realpath(os.path.join(os.path.abspath(__file__), os.path.
    pardir, os.path.pardir))
IS_ZIPAPP = os.path.isfile(ROOT)
_CAN_SYMLINK = _FS_CASE_SENSITIVE = _CFG_DIR = _DATA_DIR = None
__all__ = ('IS_CPYTHON', 'IS_MAC_ARM64', 'IS_PYPY', 'IS_WIN', 'IS_ZIPAPP',
    'ROOT', 'fs_is_case_sensitive', 'fs_path_id', 'fs_supports_symlink')
