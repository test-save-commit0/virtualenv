from __future__ import annotations
from collections import OrderedDict, defaultdict
from typing import TYPE_CHECKING, NamedTuple
from virtualenv.create.describe import Describe
from virtualenv.create.via_global_ref.builtin.builtin_way import VirtualenvBuiltin
from .base import ComponentBuilder
if TYPE_CHECKING:
    from virtualenv.create.creator import Creator, CreatorMeta


class CreatorInfo(NamedTuple):
    key_to_class: dict[str, type[Creator]]
    key_to_meta: dict[str, CreatorMeta]
    describe: type[Describe] | None
    builtin_key: str


class CreatorSelector(ComponentBuilder):

    def __init__(self, interpreter, parser) ->None:
        creators, self.key_to_meta, self.describe, self.builtin_key = (self
            .for_interpreter(interpreter))
        super().__init__(interpreter, parser, 'creator', creators)


__all__ = ['CreatorInfo', 'CreatorSelector']
