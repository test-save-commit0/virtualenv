from __future__ import annotations
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentTypeError
from ast import literal_eval
from collections import OrderedDict
from pathlib import Path
from virtualenv.discovery.cached_py_info import LogCmd
from virtualenv.util.path import safe_delete
from virtualenv.util.subprocess import run_cmd
from virtualenv.version import __version__
from .pyenv_cfg import PyEnvCfg
HERE = Path(os.path.abspath(__file__)).parent
DEBUG_SCRIPT = HERE / 'debug.py'


class CreatorMeta:

    def __init__(self) ->None:
        self.error = None


class Creator(ABC):
    """A class that given a python Interpreter creates a virtual environment."""

    def __init__(self, options, interpreter) ->None:
        """
        Construct a new virtual environment creator.

        :param options: the CLI option as parsed from :meth:`add_parser_arguments`
        :param interpreter: the interpreter to create virtual environment from
        """
        self.interpreter = interpreter
        self._debug = None
        self.dest = Path(options.dest)
        self.clear = options.clear
        self.no_vcs_ignore = options.no_vcs_ignore
        self.pyenv_cfg = PyEnvCfg.from_folder(self.dest)
        self.app_data = options.app_data
        self.env = options.env

    def __repr__(self) ->str:
        return (
            f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self._args())})"
            )

    def _copy_python_executable(self):
        """Copy the Python executable to the virtual environment."""
        src = Path(sys.executable)
        dst = self.dest / "bin" / src.name
        dst.write_bytes(src.read_bytes())
        dst.chmod(0o755)

    def _create_activation_scripts(self):
        """Create activation scripts for different shells."""
        activate_this = f"""
# This file must be used with "source bin/activate" *from bash*
# you cannot run it directly

deactivate () {{
    unset -f pydoc >/dev/null 2>&1 || true

    # reset old environment variables
    if [ -n "${{_OLD_VIRTUAL_PATH:-}}" ] ; then
        PATH="${{_OLD_VIRTUAL_PATH:-}}"
        export PATH
        unset _OLD_VIRTUAL_PATH
    fi
    if [ -n "${{_OLD_VIRTUAL_PYTHONHOME:-}}" ] ; then
        PYTHONHOME="${{_OLD_VIRTUAL_PYTHONHOME:-}}"
        export PYTHONHOME
        unset _OLD_VIRTUAL_PYTHONHOME
    fi

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "${{BASH:-}}" -o -n "${{ZSH_VERSION:-}}" ] ; then
        hash -r 2> /dev/null
    fi

    if [ -n "${{_OLD_VIRTUAL_PS1:-}}" ] ; then
        PS1="${{_OLD_VIRTUAL_PS1:-}}"
        export PS1
        unset _OLD_VIRTUAL_PS1
    fi

    unset VIRTUAL_ENV
    unset VIRTUAL_ENV_PROMPT
    if [ ! "${{1:-}}" = "nondestructive" ] ; then
    # Self destruct!
        unset -f deactivate
    fi
}}

# unset irrelevant variables
deactivate nondestructive

VIRTUAL_ENV="{self.dest}"
export VIRTUAL_ENV

_OLD_VIRTUAL_PATH="$PATH"
PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

# unset PYTHONHOME if set
# this will fail if PYTHONHOME is set to the empty string (which is bad anyway)
# could use `if (set -u; : $PYTHONHOME) ;` in bash
if [ -n "${{PYTHONHOME:-}}" ] ; then
    _OLD_VIRTUAL_PYTHONHOME="${{PYTHONHOME:-}}"
    unset PYTHONHOME
fi

if [ -z "${{VIRTUAL_ENV_DISABLE_PROMPT:-}}" ] ; then
    _OLD_VIRTUAL_PS1="${{PS1:-}}"
    PS1="({self.dest.name}) ${{PS1:-}}"
    export PS1
    VIRTUAL_ENV_PROMPT="({self.dest.name}) "
    export VIRTUAL_ENV_PROMPT
fi

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "${{BASH:-}}" -o -n "${{ZSH_VERSION:-}}" ] ; then
    hash -r 2> /dev/null
fi
"""
        (self.dest / "bin" / "activate").write_text(activate_this)

    @classmethod
    def can_create(cls, interpreter):
        """
        Determine if we can create a virtual environment.

        :param interpreter: the interpreter in question
        :return: ``None`` if we can't create, any other object otherwise that will be forwarded to                   :meth:`add_parser_arguments`
        """
        return True  # Assume we can always create a virtual environment

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, meta, app_data):
        """
        Add CLI arguments for the creator.

        :param parser: the CLI parser
        :param app_data: the application data folder
        :param interpreter: the interpreter we're asked to create virtual environment for
        :param meta: value as returned by :meth:`can_create`
        """
        parser.add_argument(
            "--dest",
            help="The destination directory to create the virtual environment in",
            required=True,
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the destination directory if it already exists",
        )
        parser.add_argument(
            "--no-vcs-ignore",
            action="store_true",
            help="Don't create VCS ignore files",
        )

    @abstractmethod
    def create(self):
        """Perform the virtual environment creation."""
        if self.clear and self.dest.exists():
            safe_delete(self.dest)
        
        self.dest.mkdir(parents=True, exist_ok=True)
        
        self.setup_ignore_vcs()
        
        # Create necessary directories
        (self.dest / "bin").mkdir(exist_ok=True)
        (self.dest / "lib").mkdir(exist_ok=True)
        (self.dest / "include").mkdir(exist_ok=True)
        
        # Create pyvenv.cfg file
        self.pyenv_cfg.write()
        
        # Copy python executable
        self._copy_python_executable()
        
        # Create activation scripts
        self._create_activation_scripts()
        
        return self.dest

    @classmethod
    def validate_dest(cls, raw_value):
        """No path separator in the path, valid chars and must be write-able."""
        try:
            path = Path(raw_value).resolve()
            if not path.parent.exists():
                raise ArgumentTypeError(f"Parent directory {path.parent} does not exist")
            if path.exists() and not os.access(path, os.W_OK):
                raise ArgumentTypeError(f"Destination {path} is not writable")
            return path
        except Exception as e:
            raise ArgumentTypeError(f"Invalid destination path: {e}")

    def setup_ignore_vcs(self):
        """Generate ignore instructions for version control systems."""
        if not self.no_vcs_ignore:
            vcs_ignore_contents = "# created by virtualenv automatically\n*"
            ignore_files = [".gitignore", ".bzrignore", ".hgignore"]
            
            for ignore_file in ignore_files:
                ignore_path = self.dest / ignore_file
                if not ignore_path.exists():
                    ignore_path.write_text(vcs_ignore_contents)

    @property
    def debug(self):
        """:return: debug information about the virtual environment (only valid after :meth:`create` has run)"""
        if self._debug is None:
            self._debug = self._get_debug_info()
        return self._debug

    def _get_debug_info(self):
        debug_info = OrderedDict()
        debug_info["creator"] = self.__class__.__name__
        debug_info["interpreter"] = self.interpreter.executable
        debug_info["dest"] = str(self.dest)
        debug_info["version"] = __version__
        
        # Add more debug information as needed
        return debug_info


__all__ = ['Creator', 'CreatorMeta']
