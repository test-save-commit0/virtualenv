"""Bootstrap."""
from __future__ import annotations
import logging
import sys
from operator import eq, lt
from pathlib import Path
from subprocess import PIPE, CalledProcessError, Popen
from .bundle import from_bundle
from .periodic_update import add_wheel_to_update_log
from .util import Version, Wheel, discover_wheels


def get_wheel(distribution, version, for_py_version, search_dirs, download,
    app_data, do_periodic_update, env):
    """Get a wheel with the given distribution-version-for_py_version trio, by using the extra search dir + download."""
    # First, try to find the wheel in the search directories
    for search_dir in search_dirs:
        wheels = discover_wheels(Path(search_dir), distribution, version, for_py_version)
        if wheels:
            return wheels[0]

    # If not found in search dirs, try to get it from the bundle
    bundle_wheel = from_bundle(distribution, version, for_py_version, search_dirs)
    if bundle_wheel:
        return bundle_wheel

    # If not in bundle, try to download
    if download:
        downloaded_wheel = download_wheel(distribution, version, for_py_version, app_data, env)
        if downloaded_wheel:
            if do_periodic_update:
                add_wheel_to_update_log(app_data, distribution, downloaded_wheel)
            return downloaded_wheel

    # If we couldn't find or download the wheel, raise an exception
    raise ValueError(f"Unable to find or download wheel for {distribution} {version} (Python {for_py_version})")


def download_wheel(distribution, version, for_py_version, app_data, env):
    """Download a wheel for the given distribution, version, and Python version."""
    logging.info(f"Downloading wheel for {distribution} {version} (Python {for_py_version})")
    
    cmd = [
        sys.executable,
        "-m", "pip",
        "download",
        "--only-binary=:all:",
        "--no-deps",
        "--python-version", for_py_version,
        f"{distribution}=={version}"
    ]

    try:
        result = pip_wheel_env_run(cmd, env)
        wheel_file = Path(result.strip())
        if wheel_file.exists() and wheel_file.is_file():
            return str(wheel_file)
    except CalledProcessError as e:
        logging.error(f"Failed to download wheel: {e}")
    
    return None

__all__ = ['download_wheel', 'get_wheel', 'pip_wheel_env_run']
