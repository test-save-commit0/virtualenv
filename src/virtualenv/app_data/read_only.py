from __future__ import annotations
import os.path
from virtualenv.util.lock import NoOpFileLock
from .via_disk_folder import AppDataDiskFolder, PyInfoStoreDisk


class ReadOnlyAppData(AppDataDiskFolder):
    can_update = False

    def __init__(self, folder: str) ->None:
        if not os.path.isdir(folder):
            msg = f'read-only app data directory {folder} does not exist'
            raise RuntimeError(msg)
        super().__init__(folder)
        self.lock = NoOpFileLock(folder)


class _PyInfoStoreDiskReadOnly(PyInfoStoreDisk):
    def __init__(self, folder):
        super().__init__(folder)

    def read(self, path):
        return super().read(path)

    def write(self, path, content):
        raise PermissionError(f"Cannot write to read-only app data: {path}")

    def remove(self, path):
        raise PermissionError(f"Cannot remove from read-only app data: {path}")


__all__ = ['ReadOnlyAppData']
