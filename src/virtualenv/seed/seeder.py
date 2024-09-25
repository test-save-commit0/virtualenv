from __future__ import annotations
from abc import ABC, abstractmethod


class Seeder(ABC):
    """A seeder will install some seed packages into a virtual environment."""

    def __init__(self, options, enabled) ->None:
        """
        Create.

        :param options: the parsed options as defined within :meth:`add_parser_arguments`
        :param enabled: a flag weather the seeder is enabled or not
        """
        self.enabled = enabled
        self.env = options.env

    @classmethod
    def add_parser_arguments(cls, parser, interpreter, app_data):
        """
        Add CLI arguments for this seed mechanisms.

        :param parser: the CLI parser
        :param app_data: the CLI parser
        :param interpreter: the interpreter this virtual environment is based of
        """
        parser.add_argument(
            "--seed-packages",
            nargs="*",
            help="Specify additional packages to install when seeding the environment",
        )

    @abstractmethod
    def run(self, creator):
        """
        Perform the seed operation.

        :param creator: the creator (based of :class:`virtualenv.create.creator.Creator`) we used to create this         virtual environment
        """
        if not self.enabled:
            return

        packages = self.env.get("seed_packages", [])
        if packages:
            self._install_packages(creator, packages)

    def _install_packages(self, creator, packages):
        """
        Install specified packages in the virtual environment.

        :param creator: the creator of the virtual environment
        :param packages: list of packages to install
        """
        pip_path = creator.bin_path / "pip"
        if not pip_path.exists():
            raise RuntimeError("pip not found in the virtual environment")

        import subprocess

        cmd = [str(pip_path), "install"] + packages
        subprocess.check_call(cmd, env=self.env)


__all__ = ['Seeder']
