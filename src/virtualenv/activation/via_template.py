from __future__ import annotations
import os
import sys
from abc import ABC, abstractmethod
from .activator import Activator
if sys.version_info >= (3, 10):
    from importlib.resources import files
else:
    from importlib.resources import read_binary


class ViaTemplateActivator(Activator, ABC):
    pass


__all__ = ['ViaTemplateActivator']
