from __future__ import annotations
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
from subprocess import PIPE, Popen
from virtualenv.util.path import safe_delete, set_tree
from .base import PipInstall


class SymlinkPipInstall(PipInstall):
    def __init__(self, wheel, creator, app_data):
        super().__init__(wheel, creator, app_data)
        self.symlink_path = None

    def _sync(self, src, dst):
        safe_delete(dst)
        os.symlink(src, dst)
        self.symlink_path = dst

    def _generate_new_files(self):
        # Create a symlink instead of copying files
        src = str(self.wheel.path)
        dst = str(self.dest_dir / self.wheel.path.name)
        self._sync(src, dst)

    def clear(self):
        if self.symlink_path:
            safe_delete(self.symlink_path)
        super().clear()

    def install(self, version_info):
        self._generate_new_files()
        # Set read-only permissions for the symlink
        os.chmod(self.symlink_path, S_IREAD | S_IRGRP | S_IROTH)
        return super().install(version_info)


__all__ = ['SymlinkPipInstall']
