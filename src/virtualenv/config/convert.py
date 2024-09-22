from __future__ import annotations
import logging
import os
from typing import ClassVar


class TypeData:

    def __init__(self, default_type, as_type) ->None:
        self.default_type = default_type
        self.as_type = as_type

    def __repr__(self) ->str:
        return (
            f'{self.__class__.__name__}(base={self.default_type}, as={self.as_type})'
            )


class BoolType(TypeData):
    BOOLEAN_STATES: ClassVar[dict[str, bool]] = {'1': True, 'yes': True,
        'true': True, 'on': True, '0': False, 'no': False, 'false': False,
        'off': False}


class NoneType(TypeData):
    pass


class ListType(TypeData):

    def _validate(self):
        """no op."""
        pass

    def split_values(self, value):
        """
        Split the provided value into a list.

        First this is done by newlines. If there were no newlines in the text,
        then we next try to split by comma.
        """
        pass


def convert(value, as_type, source):
    """Convert the value as a given type where the value comes from the given source."""
    pass


_CONVERT = {bool: BoolType, type(None): NoneType, list: ListType}
__all__ = ['convert', 'get_type']
