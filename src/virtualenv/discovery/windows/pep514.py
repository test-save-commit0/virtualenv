"""Implement https://www.python.org/dev/peps/pep-0514/ to discover interpreters - Windows only."""
from __future__ import annotations
import os
import re
import winreg
from logging import basicConfig, getLogger
LOGGER = getLogger(__name__)
if __name__ == '__main__':
    _run()
