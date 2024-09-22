"""Bootstrap."""
from __future__ import annotations
import logging
import sys
import traceback
from contextlib import contextmanager
from pathlib import Path
from subprocess import CalledProcessError
from threading import Lock, Thread
from virtualenv.info import fs_supports_symlink
from virtualenv.seed.embed.base_embed import BaseEmbed
from virtualenv.seed.wheels import get_wheel
from .pip_install.copy import CopyPipInstall
from .pip_install.symlink import SymlinkPipInstall


class FromAppData(BaseEmbed):

    def __init__(self, options) ->None:
        super().__init__(options)
        self.symlinks = options.symlink_app_data

    def __repr__(self) ->str:
        msg = (
            f", via={'symlink' if self.symlinks else 'copy'}, app_data_dir={self.app_data}"
            )
        base = super().__repr__()
        return f'{base[:-1]}{msg}{base[-1]}'


__all__ = ['FromAppData']
