from __future__ import annotations
import os
from pathlib import Path
from virtualenv.util.path import copy
from .base import PipInstall


class CopyPipInstall(PipInstall):
    pass


__all__ = ['CopyPipInstall']
