from __future__ import annotations
import logging
import os
import re
import zipfile
from abc import ABC, abstractmethod
from configparser import ConfigParser
from itertools import chain
from pathlib import Path
from tempfile import mkdtemp
from distlib.scripts import ScriptMaker, enquote_executable
from virtualenv.util.path import safe_delete


class PipInstall(ABC):

    def __init__(self, wheel, creator, image_folder) ->None:
        self._wheel = wheel
        self._creator = creator
        self._image_dir = image_folder
        self._extracted = False
        self.__dist_info = None
        self._console_entry_points = None


class ScriptMakerCustom(ScriptMaker):

    def __init__(self, target_dir, version_info, executable, name) ->None:
        super().__init__(None, str(target_dir))
        self.clobber = True
        self.set_mode = True
        self.executable = enquote_executable(str(executable))
        self.version_info = version_info.major, version_info.minor
        self.variants = {'', 'X', 'X.Y'}
        self._name = name


__all__ = ['PipInstall']
