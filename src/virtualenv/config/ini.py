from __future__ import annotations
import logging
import os
from configparser import ConfigParser
from pathlib import Path
from typing import ClassVar
from platformdirs import user_config_dir
from .convert import convert


class IniConfig:
    VIRTUALENV_CONFIG_FILE_ENV_VAR: ClassVar[str] = 'VIRTUALENV_CONFIG_FILE'
    STATE: ClassVar[dict[bool | None, str]] = {None: 'failed to parse', (
        True): 'active', (False): 'missing'}
    section = 'virtualenv'

    def __init__(self, env=None) ->None:
        env = os.environ if env is None else env
        config_file = env.get(self.VIRTUALENV_CONFIG_FILE_ENV_VAR, None)
        self.is_env_var = config_file is not None
        if config_file is None:
            config_file = Path(user_config_dir(appname='virtualenv',
                appauthor='pypa')) / 'virtualenv.ini'
        else:
            config_file = Path(config_file)
        self.config_file = config_file
        self._cache = {}
        exception = None
        self.has_config_file = None
        try:
            self.has_config_file = self.config_file.exists()
        except OSError as exc:
            exception = exc
        else:
            if self.has_config_file:
                self.config_file = self.config_file.resolve()
                self.config_parser = ConfigParser()
                try:
                    self._load()
                    self.has_virtualenv_section = (self.config_parser.
                        has_section(self.section))
                except Exception as exc:
                    exception = exc
        if exception is not None:
            logging.error('failed to read config file %s because %r',
                config_file, exception)

    def __bool__(self) ->bool:
        return bool(self.has_config_file) and bool(self.has_virtualenv_section)
