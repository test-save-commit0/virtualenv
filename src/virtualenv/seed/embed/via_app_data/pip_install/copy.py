from __future__ import annotations
import os
from pathlib import Path
from virtualenv.util.path import copy
from .base import PipInstall


class CopyPipInstall(PipInstall):
    def __init__(self, wheel):
        super().__init__(wheel)

    def _sync(self, src, dst):
        dst_folder = os.path.dirname(dst)
        if not os.path.isdir(dst_folder):
            os.makedirs(dst_folder)
        if src != dst:
            copy(src, dst)

    def install(self, creator):
        for src in self.wheel.src_files:
            dst = os.path.join(creator.purelib, self.wheel.name, os.path.basename(src))
            self._sync(src, dst)

    def clear(self, creator):
        pass  # No need to clear anything for copy installation


__all__ = ['CopyPipInstall']
