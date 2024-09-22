from __future__ import annotations
from .base import ComponentBuilder


class SeederSelector(ComponentBuilder):

    def __init__(self, interpreter, parser) ->None:
        possible = self.options('virtualenv.seed')
        super().__init__(interpreter, parser, 'seeder', possible)


__all__ = ['SeederSelector']
