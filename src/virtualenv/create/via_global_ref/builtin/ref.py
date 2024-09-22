"""
Virtual environments in the traditional sense are built as reference to the host python. This file allows declarative
references to elements on the file system, allowing our system to automatically detect what modes it can support given
the constraints: e.g. can the file system symlink, can the files be read, executed, etc.
"""
from __future__ import annotations
import os
from abc import ABC, abstractmethod
from collections import OrderedDict
from stat import S_IXGRP, S_IXOTH, S_IXUSR
from virtualenv.info import fs_is_case_sensitive, fs_supports_symlink
from virtualenv.util.path import copy, make_exe, symlink


class RefMust:
    NA = 'NA'
    COPY = 'copy'
    SYMLINK = 'symlink'


class RefWhen:
    ANY = 'ANY'
    COPY = 'copy'
    SYMLINK = 'symlink'


class PathRef(ABC):
    """Base class that checks if a file reference can be symlink/copied."""
    FS_SUPPORTS_SYMLINK = fs_supports_symlink()
    FS_CASE_SENSITIVE = fs_is_case_sensitive()

    def __init__(self, src, must=RefMust.NA, when=RefWhen.ANY) ->None:
        self.must = must
        self.when = when
        self.src = src
        try:
            self.exists = src.exists()
        except OSError:
            self.exists = False
        self._can_read = None if self.exists else False
        self._can_copy = None if self.exists else False
        self._can_symlink = None if self.exists else False

    def __repr__(self) ->str:
        return f'{self.__class__.__name__}(src={self.src})'


class ExePathRef(PathRef, ABC):
    """Base class that checks if a executable can be references via symlink/copy."""

    def __init__(self, src, must=RefMust.NA, when=RefWhen.ANY) ->None:
        super().__init__(src, must, when)
        self._can_run = None


class PathRefToDest(PathRef):
    """Link a path on the file system."""

    def __init__(self, src, dest, must=RefMust.NA, when=RefWhen.ANY) ->None:
        super().__init__(src, must, when)
        self.dest = dest


class ExePathRefToDest(PathRefToDest, ExePathRef):
    """Link a exe path on the file system."""

    def __init__(self, src, targets, dest, must=RefMust.NA, when=RefWhen.ANY
        ) ->None:
        ExePathRef.__init__(self, src, must, when)
        PathRefToDest.__init__(self, src, dest, must, when)
        if not self.FS_CASE_SENSITIVE:
            targets = list(OrderedDict((i.lower(), None) for i in targets).
                keys())
        self.base = targets[0]
        self.aliases = targets[1:]
        self.dest = dest

    def __repr__(self) ->str:
        return (
            f'{self.__class__.__name__}(src={self.src}, alias={self.aliases})')


__all__ = ['ExePathRef', 'ExePathRefToDest', 'PathRef', 'PathRefToDest',
    'RefMust', 'RefWhen']
