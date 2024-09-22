from __future__ import annotations
import logging
from copy import copy
from virtualenv.create.via_global_ref.store import handle_store_python
from virtualenv.discovery.py_info import PythonInfo
from virtualenv.util.error import ProcessCallFailedError
from virtualenv.util.path import ensure_dir
from virtualenv.util.subprocess import run_cmd
from .api import ViaGlobalRefApi, ViaGlobalRefMeta
from .builtin.cpython.mac_os import CPython3macOsBrew
from .builtin.pypy.pypy3 import Pypy3Windows


class Venv(ViaGlobalRefApi):

    def __init__(self, options, interpreter) ->None:
        self.describe = options.describe
        super().__init__(options, interpreter)
        current = PythonInfo.current()
        self.can_be_inline = (interpreter is current and interpreter.
            executable == interpreter.system_executable)
        self._context = None

    def executables_for_win_pypy_less_v37(self):
        """
        PyPy <= 3.6 (v7.3.3) for Windows contains only pypy3.exe and pypy3w.exe
        Venv does not handle non-existing exe sources, e.g. python.exe, so this
        patch does it.
        """
        pass

    def __getattribute__(self, item):
        describe = object.__getattribute__(self, 'describe')
        if describe is not None and hasattr(describe, item):
            element = getattr(describe, item)
            if not callable(element) or item == 'script':
                return element
        return object.__getattribute__(self, item)


__all__ = ['Venv']
