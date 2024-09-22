"""Patches that are applied at runtime to the virtual environment."""
from __future__ import annotations
import os
import sys
VIRTUALENV_PATCH_FILE = os.path.join(__file__)


def patch_dist(dist):
    """
    Distutils allows user to configure some arguments via a configuration file:
    https://docs.python.org/3/install/index.html#distutils-configuration-files.

    Some of this arguments though don't make sense in context of the virtual environment files, let's fix them up.
    """
    pass


_DISTUTILS_PATCH = 'distutils.dist', 'setuptools.dist'


class _Finder:
    """A meta path finder that allows patching the imported distutils modules."""
    fullname = None
    lock = []


sys.meta_path.insert(0, _Finder())
