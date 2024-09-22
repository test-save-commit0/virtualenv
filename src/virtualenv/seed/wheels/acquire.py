"""Bootstrap."""
from __future__ import annotations
import logging
import sys
from operator import eq, lt
from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen
from .bundle import from_bundle
from .periodic_update import add_wheel_to_update_log
from .util import Version, Wheel, discover_wheels


def get_wheel(distribution, version, for_py_version, search_dirs, download,
    app_data, do_periodic_update, env):
    """Get a wheel with the given distribution-version-for_py_version trio, by using the extra search dir + download."""
    pass


__all__ = ['download_wheel', 'get_wheel', 'pip_wheel_env_run']
