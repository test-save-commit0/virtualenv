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
        if not isinstance(self.as_type, (list, tuple)):
            raise ValueError("as_type must be a list or tuple")

    def split_values(self, value):
        """
        Split the provided value into a list.

        First this is done by newlines. If there were no newlines in the text,
        then we next try to split by comma.
        """
        if isinstance(value, str):
            if '\n' in value:
                return [v.strip() for v in value.split('\n') if v.strip()]
            return [v.strip() for v in value.split(',') if v.strip()]
        elif isinstance(value, (list, tuple)):
            return list(value)
        else:
            return [value]


def convert(value, as_type, source):
    """Convert the value as a given type where the value comes from the given source."""
    if as_type is bool:
        return _convert_bool(value, source)
    elif as_type is None:
        return None
    elif isinstance(as_type, (list, tuple)):
        return _convert_list(value, as_type, source)
    else:
        try:
            return as_type(value)
        except ValueError as e:
            raise ValueError(f"failed to convert {value!r} to {as_type.__name__} via {source}: {e}")

def _convert_bool(value, source):
    if isinstance(value, bool):
        return value
    try:
        return BoolType.BOOLEAN_STATES[str(value).lower()]
    except KeyError:
        raise ValueError(f"failed to convert {value!r} to bool via {source}")

def _convert_list(value, as_type, source):
    list_type = _CONVERT[list](list, as_type)
    values = list_type.split_values(value)
    return [convert(v, as_type[0], source) for v in values]


_CONVERT = {bool: BoolType, type(None): NoneType, list: ListType}
__all__ = ['convert', 'get_type']
