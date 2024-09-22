from __future__ import annotations
from operator import attrgetter
from zipfile import ZipFile


class Wheel:

    def __init__(self, path) ->None:
        self.path = path
        self._parts = path.stem.split('-')

    def __repr__(self) ->str:
        return f'{self.__class__.__name__}({self.path})'

    def __str__(self) ->str:
        return str(self.path)


class Version:
    bundle = 'bundle'
    embed = 'embed'
    non_version = bundle, embed


__all__ = ['Version', 'Wheel', 'discover_wheels']
