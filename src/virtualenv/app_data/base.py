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
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def reset(self):
        """Called when the user passes in the reset app data."""
        raise NotImplementedError("Subclasses must implement this method")

    @contextmanager
    def ensure_extracted(self, path, to_folder=None):
        """Some paths might be within the zipapp, unzip these to a path on the disk."""
        if IS_ZIPAPP:
            import tempfile
            import shutil
            import os

            temp_dir = to_folder or tempfile.mkdtemp()
            try:
                extracted_path = os.path.join(temp_dir, os.path.basename(path))
                shutil.copy(path, extracted_path)
                yield extracted_path
            finally:
                if not to_folder:
                    shutil.rmtree(temp_dir)
        else:
            yield path


class ContentStore(ABC):
    pass


__all__ = ['AppData', 'ContentStore']
