from __future__ import annotations
from abc import ABC, abstractmethod


class Discover(ABC):
    """Discover and provide the requested Python interpreter."""

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        Add CLI arguments for this discovery mechanisms.

        :param parser: the CLI parser
        """
        pass

    def __init__(self, options) ->None:
        """
        Create a new discovery mechanism.

        :param options: the parsed options as defined within :meth:`add_parser_arguments`
        """
        self._has_run = False
        self._interpreter = None
        self._env = options.env

    @abstractmethod
    def run(self):
        """
        Discovers an interpreter.

        :return: the interpreter ready to use for virtual environment creation
        """
        pass

    @property
    def interpreter(self):
        """:return: the interpreter as returned by :meth:`run`, cached"""
        pass


__all__ = ['Discover']
