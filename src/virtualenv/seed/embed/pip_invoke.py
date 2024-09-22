from __future__ import annotations
import logging
from contextlib import contextmanager
from subprocess import Popen
from virtualenv.discovery.cached_py_info import LogCmd
from virtualenv.seed.embed.base_embed import BaseEmbed
from virtualenv.seed.wheels import Version, get_wheel, pip_wheel_env_run


class PipInvoke(BaseEmbed):

    def __init__(self, options) ->None:
        super().__init__(options)


__all__ = ['PipInvoke']
