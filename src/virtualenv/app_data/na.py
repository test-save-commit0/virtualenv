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
        return

    def reset(self):
        """Do nothing."""
        return

    @contextmanager
    def locked(self, path):
        """Do nothing."""
        yield

    def py_info_clear(self):
        """Nothing to clear."""
        return


class ContentStoreNA(ContentStore):

    def read(self):
        """Nothing to read."""
        return None

    def write(self, content):
        """Nothing to write."""
        return

    def remove(self):
        """Nothing to remove."""
        return


__all__ = ['AppDataDisabled', 'ContentStoreNA']
