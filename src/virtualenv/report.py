from __future__ import annotations
import logging
import sys
LEVELS = {(0): logging.CRITICAL, (1): logging.ERROR, (2): logging.WARNING,
    (3): logging.INFO, (4): logging.DEBUG, (5): logging.NOTSET}
MAX_LEVEL = max(LEVELS.keys())
LOGGER = logging.getLogger()
__all__ = ['LEVELS', 'MAX_LEVEL', 'setup_report']
