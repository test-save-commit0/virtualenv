from __future__ import annotations
from virtualenv.seed.wheels.embed import get_embed_wheel
from .periodic_update import periodic_update
from .util import Version, Wheel, discover_wheels


def from_bundle(distribution, version, for_py_version, search_dirs,
    app_data, do_periodic_update, env):
    """Load the bundled wheel to a cache directory."""
    pass


def from_dir(distribution, version, for_py_version, directories):
    """Load a compatible wheel from a given folder."""
    pass


__all__ = ['from_bundle', 'load_embed_wheel']
