from __future__ import annotations
import abc
from pathlib import Path
from virtualenv.create.via_global_ref.builtin.ref import PathRefToDest, RefMust, RefWhen
from virtualenv.create.via_global_ref.builtin.via_global_self_do import ViaGlobalRefVirtualenvBuiltin


class PyPy(ViaGlobalRefVirtualenvBuiltin, abc.ABC):
    pass


__all__ = ['PyPy']
