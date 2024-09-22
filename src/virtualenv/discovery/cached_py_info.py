"""

We acquire the python information by running an interrogation script via subprocess trigger. This operation is not
cheap, especially not on Windows. To not have to pay this hefty cost every time we apply multiple levels of
caching.
"""
from __future__ import annotations
import logging
import os
import random
import sys
from collections import OrderedDict
from pathlib import Path
from shlex import quote
from string import ascii_lowercase, ascii_uppercase, digits
from subprocess import Popen
from virtualenv.app_data import AppDataDisabled
from virtualenv.discovery.py_info import PythonInfo
from virtualenv.util.subprocess import subprocess
_CACHE = OrderedDict()
_CACHE[Path(sys.executable)] = PythonInfo()
COOKIE_LENGTH: int = 32


class LogCmd:

    def __init__(self, cmd, env=None) ->None:
        self.cmd = cmd
        self.env = env

    def __repr__(self) ->str:
        cmd_repr = ' '.join(quote(str(c)) for c in self.cmd)
        if self.env is not None:
            cmd_repr = f'{cmd_repr} env of {self.env!r}'
        return cmd_repr


___all___ = ['from_exe', 'clear', 'LogCmd']
