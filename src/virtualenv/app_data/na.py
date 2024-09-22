from __future__ import annotations
from contextlib import contextmanager
from .base import AppData, ContentStore


class AppDataDisabled(AppData):
    """No application cache available (most likely as we don't have write permissions)."""
    transient = True
    can_update = False

    def __init__(self) ->None:
        pass
    error = RuntimeError(
        'no app data folder available, probably no write access to the folder')

    def close(self):
        """Do nothing."""
        pass

    def reset(self):
        """Do nothing."""
        pass

    @contextmanager
    def locked(self, path):
        """Do nothing."""
        pass

    def py_info_clear(self):
        """Nothing to clear."""
        pass


class ContentStoreNA(ContentStore):

    def read(self):
        """Nothing to read."""
        pass

    def write(self, content):
        """Nothing to write."""
        pass

    def remove(self):
        """Nothing to remove."""
        pass


__all__ = ['AppDataDisabled', 'ContentStoreNA']
