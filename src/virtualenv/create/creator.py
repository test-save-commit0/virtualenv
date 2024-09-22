from __future__ import annotations
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentTypeError
from ast import literal_eval
from collections import OrderedDict
from pathlib import Path
from virtualenv.discovery.cached_py_info import LogCmd
from virtualenv.util.path import safe_delete
from virtualenv.util.subprocess import run_cmd
from virtualenv.version import __version__
from .pyenv_cfg import PyEnvCfg
HERE = Path(os.path.abspath(__file__)).parent
DEBUG_SCRIPT = HERE / 'debug.py'


class CreatorMeta:

    def __init__(self) ->None:
        self.error = None


class Creator(ABC):
    """A class that given a python Interpreter creates a virtual environment."""

    def __init__(self, options, interpreter) ->None:
        """
        Construct a new virtual environment creator.

        :param options: the CLI option as parsed from :meth:`add_parser_arguments`
        :param interpreter: the interpreter to create virtual environment from
        """
        self.interpreter = interpreter
        self._debug = None
        self.dest = Path(options.dest)
        self.clear = options.clear
        self.no_vcs_ignore = options.no_vcs_ignore
        self.pyenv_cfg = PyEnvCfg.from_folder(self.dest)
        self.app_data = options.app_data
        self.env = options.env

    def __repr__(self) ->str:
        return (
            f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self._args())})"
            )

    @classmethod
    def can_create(cls, interpreter):
        """
        Determine if we can create a virtual environment.

        :param interpreter: the interpreter in question
        :return: ``None`` if we can't create, any other object otherwise that will be forwarded to                   :meth:`add_parser_arguments`
        """
        pass

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, meta, app_data):
        """
        Add CLI arguments for the creator.

        :param parser: the CLI parser
        :param app_data: the application data folder
        :param interpreter: the interpreter we're asked to create virtual environment for
        :param meta: value as returned by :meth:`can_create`
        """
        pass

    @abstractmethod
    def create(self):
        """Perform the virtual environment creation."""
        pass

    @classmethod
    def validate_dest(cls, raw_value):
        """No path separator in the path, valid chars and must be write-able."""
        pass

    def setup_ignore_vcs(self):
        """Generate ignore instructions for version control systems."""
        pass

    @property
    def debug(self):
        """:return: debug information about the virtual environment (only valid after :meth:`create` has run)"""
        pass


__all__ = ['Creator', 'CreatorMeta']
