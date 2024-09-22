from __future__ import annotations
import sys
from collections import OrderedDict
if sys.version_info >= (3, 8):
    from importlib.metadata import entry_points
    importlib_metadata_version = ()
else:
    from importlib_metadata import entry_points, version
    importlib_metadata_version = tuple(int(i) for i in version(
        'importlib_metadata').split('.')[:2])


class PluginLoader:
    _OPTIONS = None
    _ENTRY_POINTS = None


class ComponentBuilder(PluginLoader):

    def __init__(self, interpreter, parser, name, possible) ->None:
        self.interpreter = interpreter
        self.name = name
        self._impl_class = None
        self.possible = possible
        self.parser = parser.add_argument_group(title=name)
        self.add_selector_arg_parse(name, list(self.possible))


__all__ = ['ComponentBuilder', 'PluginLoader']
