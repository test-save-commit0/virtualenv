"""A Python specification is an abstract requirement definition of an interpreter."""
from __future__ import annotations
import os
import re
PATTERN = re.compile(
    '^(?P<impl>[a-zA-Z]+)?(?P<version>[0-9.]+)?(?:-(?P<arch>32|64))?$')


class PythonSpec:
    """Contains specification about a Python Interpreter."""

    def __init__(self, str_spec: str, implementation: (str | None), major:
        (int | None), minor: (int | None), micro: (int | None),
        architecture: (int | None), path: (str | None)) ->None:
        self.str_spec = str_spec
        self.implementation = implementation
        self.major = major
        self.minor = minor
        self.micro = micro
        self.architecture = architecture
        self.path = path

    def generate_re(self, *, windows: bool) ->re.Pattern:
        """Generate a regular expression for matching against a filename."""
        pattern = r""
        if self.implementation:
            pattern += rf"{re.escape(self.implementation)}"
        if self.major is not None:
            pattern += rf"{self.major}"
            if self.minor is not None:
                pattern += rf"\.{self.minor}"
                if self.micro is not None:
                    pattern += rf"\.{self.micro}"
        if self.architecture:
            pattern += rf"-{self.architecture}"
        if windows:
            pattern += r"\.exe"
        return re.compile(pattern, re.IGNORECASE)

    def satisfies(self, spec):
        """Called when there's a candidate metadata spec to see if compatible - e.g. PEP-514 on Windows."""
        if self.implementation and spec.implementation and self.implementation.lower() != spec.implementation.lower():
            return False
        if self.major is not None and spec.major is not None and self.major != spec.major:
            return False
        if self.minor is not None and spec.minor is not None and self.minor != spec.minor:
            return False
        if self.micro is not None and spec.micro is not None and self.micro != spec.micro:
            return False
        if self.architecture and spec.architecture and self.architecture != spec.architecture:
            return False
        return True

    def __repr__(self) ->str:
        name = type(self).__name__
        params = ('implementation', 'major', 'minor', 'micro',
            'architecture', 'path')
        return (
            f"{name}({', '.join(f'{k}={getattr(self, k)}' for k in params if getattr(self, k) is not None)})"
            )


__all__ = ['PythonSpec']
