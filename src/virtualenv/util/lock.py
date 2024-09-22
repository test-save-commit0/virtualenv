"""holds locking functionality that works across processes."""
from __future__ import annotations
import logging
import os
from abc import ABC, abstractmethod
from contextlib import contextmanager, suppress
from pathlib import Path
from threading import Lock, RLock
from filelock import FileLock, Timeout


class _CountedFileLock(FileLock):

    def __init__(self, lock_file) ->None:
        parent = os.path.dirname(lock_file)
        if not os.path.isdir(parent):
            with suppress(OSError):
                os.makedirs(parent)
        super().__init__(lock_file)
        self.count = 0
        self.thread_safe = RLock()


_lock_store = {}
_store_lock = Lock()


class PathLockBase(ABC):

    def __init__(self, folder) ->None:
        path = Path(folder)
        self.path = path.resolve() if path.exists() else path

    def __repr__(self) ->str:
        return f'{self.__class__.__name__}({self.path})'

    def __truediv__(self, other):
        return type(self)(self.path / other)

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class ReentrantFileLock(PathLockBase):

    def __init__(self, folder) ->None:
        super().__init__(folder)
        self._lock = None

    def __del__(self) ->None:
        self._del_lock(self._lock)

    def __enter__(self):
        self._lock = self._create_lock()
        self._lock_file(self._lock)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release(self._lock)
        self._del_lock(self._lock)
        self._lock = None


class NoOpFileLock(PathLockBase):

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


__all__ = ['NoOpFileLock', 'ReentrantFileLock', 'Timeout']
