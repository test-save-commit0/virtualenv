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
    # Reset the prefix and exec_prefix to empty strings
    dist.prefix = ''
    dist.exec_prefix = ''

    # Set install_lib to None to use the default
    dist.install_lib = None

    # Reset the install directories
    dist.install_platlib = None
    dist.install_purelib = None
    dist.install_headers = None
    dist.install_scripts = None
    dist.install_data = None


_DISTUTILS_PATCH = 'distutils.dist', 'setuptools.dist'


class _Finder:
    """A meta path finder that allows patching the imported distutils modules."""
    fullname = None
    lock = []

    @classmethod
    def find_spec(cls, fullname, path, target=None):
        if fullname in _DISTUTILS_PATCH:
            return cls._create_spec(fullname)
        return None

    @classmethod
    def _create_spec(cls, fullname):
        from importlib.util import spec_from_loader
        return spec_from_loader(fullname, cls())

    @classmethod
    def load_module(cls, fullname):
        with cls.lock:
            if fullname != cls.fullname:
                cls.fullname = fullname
                module = cls._load_module(fullname)
                sys.modules[fullname] = module
                return module
        return sys.modules[fullname]

    @staticmethod
    def _load_module(fullname):
        import importlib
        module = importlib.import_module(fullname)
        if fullname.startswith('distutils'):
            patch_dist(module.Distribution)
        return module

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        fullname = module.__spec__.name
        self.load_module(fullname)


sys.meta_path.insert(0, _Finder())
