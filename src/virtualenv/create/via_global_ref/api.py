from __future__ import annotations
import logging
import os
import textwrap
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
        return textwrap.dedent(
            """
            import distutils.dist
            import distutils.sysconfig
            from distutils import log
            from distutils.command import install

            # Patch distutils to ignore user configuration files
            distutils.dist.Distribution.parse_config_files = lambda self, *args, **kwargs: None
            distutils.sysconfig.get_config_vars = lambda *args, **kwargs: {}
            distutils.sysconfig.get_config_var = lambda *args, **kwargs: None

            # Patch distutils to not write to the user's home directory
            def _dont_write_bytecode(self):
                self.byte_compile = 0
            install.install._dont_write_bytecode = _dont_write_bytecode
            install.install.finalize_options = _dont_write_bytecode

            # Suppress distutils warnings
            log.set_threshold(log.ERROR)
            """
        )


__all__ = ['ViaGlobalRefApi', 'ViaGlobalRefMeta']
