"""Periodically update bundled versions."""
from __future__ import annotations
import json
import logging
import os
import ssl
import sys
from datetime import datetime, timedelta, timezone
from itertools import groupby
from pathlib import Path
from shutil import copy2
from subprocess import DEVNULL, Popen
from textwrap import dedent
from threading import Thread
from urllib.error import URLError
from urllib.request import urlopen
from virtualenv.app_data import AppDataDiskFolder
from virtualenv.seed.wheels.embed import BUNDLE_SUPPORT
from virtualenv.seed.wheels.util import Wheel
from virtualenv.util.subprocess import CREATE_NO_WINDOW
GRACE_PERIOD_CI = timedelta(hours=1)
GRACE_PERIOD_MINOR = timedelta(days=28)
UPDATE_PERIOD = timedelta(days=14)
UPDATE_ABORTED_DELAY = timedelta(hours=1)
DATETIME_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'


class NewVersion:

    def __init__(self, filename, found_date, release_date, source) ->None:
        self.filename = filename
        self.found_date = found_date
        self.release_date = release_date
        self.source = source

    def __repr__(self) ->str:
        return (
            f'{self.__class__.__name__}(filename={self.filename}), found_date={self.found_date}, release_date={self.release_date}, source={self.source})'
            )

    def __eq__(self, other):
        return type(self) == type(other) and all(getattr(self, k) ==
            getattr(other, k) for k in ['filename', 'release_date',
            'found_date', 'source'])

    def __ne__(self, other):
        return not self == other


class UpdateLog:

    def __init__(self, started, completed, versions, periodic) ->None:
        self.started = started
        self.completed = completed
        self.versions = versions
        self.periodic = periodic


_PYPI_CACHE = {}
__all__ = ['NewVersion', 'UpdateLog', 'add_wheel_to_update_log',
    'do_update', 'dump_datetime', 'load_datetime', 'manual_upgrade',
    'periodic_update', 'release_date_for_wheel_path', 'trigger_update']
