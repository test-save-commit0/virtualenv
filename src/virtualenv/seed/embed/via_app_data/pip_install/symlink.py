from __future__ import annotations
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
from subprocess import PIPE, Popen
from virtualenv.util.path import safe_delete, set_tree
from .base import PipInstall


class SymlinkPipInstall(PipInstall):
    pass


__all__ = ['SymlinkPipInstall']
