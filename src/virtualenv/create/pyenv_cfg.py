from __future__ import annotations
import logging
import os
from collections import OrderedDict


class PyEnvCfg:

    def __init__(self, content, path) ->None:
        self.content = content
        self.path = path

    def __setitem__(self, key, value) ->None:
        self.content[key] = value

    def __getitem__(self, key):
        return self.content[key]

    def __contains__(self, item) ->bool:
        return item in self.content

    def __repr__(self) ->str:
        return f'{self.__class__.__name__}(path={self.path})'


__all__ = ['PyEnvCfg']
