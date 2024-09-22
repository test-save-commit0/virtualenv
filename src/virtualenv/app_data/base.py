"""Application data stored by virtualenv."""
from __future__ import annotations
from abc import ABC, abstractmethod
from contextlib import contextmanager
from virtualenv.info import IS_ZIPAPP


class AppData(ABC):
    """Abstract storage interface for the virtualenv application."""

    @abstractmethod
    def close(self):
        """Called before virtualenv exits."""
        pass

    @abstractmethod
    def reset(self):
        """Called when the user passes in the reset app data."""
        pass

    @contextmanager
    def ensure_extracted(self, path, to_folder=None):
        """Some paths might be within the zipapp, unzip these to a path on the disk."""
        pass


class ContentStore(ABC):
    pass


__all__ = ['AppData', 'ContentStore']
