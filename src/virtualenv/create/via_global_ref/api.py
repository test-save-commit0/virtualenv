from __future__ import annotations
import logging
import os
from abc import ABC
from pathlib import Path
from virtualenv.create.creator import Creator, CreatorMeta
from virtualenv.info import fs_supports_symlink


class ViaGlobalRefMeta(CreatorMeta):

    def __init__(self) ->None:
        super().__init__()
        self.copy_error = None
        self.symlink_error = None
        if not fs_supports_symlink():
            self.symlink_error = 'the filesystem does not supports symlink'


class ViaGlobalRefApi(Creator, ABC):

    def __init__(self, options, interpreter) ->None:
        super().__init__(options, interpreter)
        self.symlinks = self._should_symlink(options)
        self.enable_system_site_package = options.system_site

    def env_patch_text(self):
        """Patch the distutils package to not be derailed by its configuration files."""
        pass


__all__ = ['ViaGlobalRefApi', 'ViaGlobalRefMeta']
