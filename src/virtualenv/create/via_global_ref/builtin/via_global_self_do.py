from __future__ import annotations
from abc import ABC
from virtualenv.create.via_global_ref.api import ViaGlobalRefApi, ViaGlobalRefMeta
from virtualenv.create.via_global_ref.builtin.ref import ExePathRefToDest, RefMust, RefWhen
from virtualenv.util.path import ensure_dir
from .builtin_way import VirtualenvBuiltin


class BuiltinViaGlobalRefMeta(ViaGlobalRefMeta):

    def __init__(self) ->None:
        super().__init__()
        self.sources = []


class ViaGlobalRefVirtualenvBuiltin(ViaGlobalRefApi, VirtualenvBuiltin, ABC):

    def __init__(self, options, interpreter) ->None:
        super().__init__(options, interpreter)
        self._sources = getattr(options.meta, 'sources', None)

    @classmethod
    def can_create(cls, interpreter):
        """By default, all built-in methods assume that if we can describe it we can create it."""
        pass

    def set_pyenv_cfg(self):
        """
        We directly inject the base prefix and base exec prefix to avoid site.py needing to discover these
        from home (which usually is done within the interpreter itself).
        """
        pass


__all__ = ['BuiltinViaGlobalRefMeta', 'ViaGlobalRefVirtualenvBuiltin']
