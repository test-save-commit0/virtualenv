"""
Activate virtualenv for current interpreter:

import runpy
runpy.run_path(this_file)

This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
"""
from __future__ import annotations
import os
import site
import sys
try:
    abs_file = os.path.abspath(__file__)
except NameError as exc:
    msg = 'You must use import runpy; runpy.run_path(this_file)'
    raise AssertionError(msg) from exc
bin_dir = os.path.dirname(abs_file)
base = bin_dir[:-len('__BIN_NAME__') - 1]
os.environ['PATH'] = os.pathsep.join([bin_dir, *os.environ.get('PATH', '').
    split(os.pathsep)])
os.environ['VIRTUAL_ENV'] = base
os.environ['VIRTUAL_ENV_PROMPT'] = '__VIRTUAL_PROMPT__' or os.path.basename(
    base)
prev_length = len(sys.path)
for lib in '__LIB_FOLDERS__'.split(os.pathsep):
    path = os.path.realpath(os.path.join(bin_dir, lib))
    site.addsitedir(path.decode('utf-8') if '__DECODE_PATH__' else path)
sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]
sys.real_prefix = sys.prefix
sys.prefix = base
