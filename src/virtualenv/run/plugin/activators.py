from __future__ import annotations
from argparse import ArgumentTypeError
from collections import OrderedDict
from .base import ComponentBuilder


class ActivationSelector(ComponentBuilder):

    def __init__(self, interpreter, parser) ->None:
        self.default = None
        possible = OrderedDict((k, v) for k, v in self.options(
            'virtualenv.activate').items() if v.supports(interpreter))
        super().__init__(interpreter, parser, 'activators', possible)
        self.parser.description = 'options for activation scripts'
        self.active = None


__all__ = ['ActivationSelector']
