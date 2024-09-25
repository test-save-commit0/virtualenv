from __future__ import annotations
import abc
from pathlib import Path
from virtualenv.create.via_global_ref.builtin.ref import PathRefToDest, RefMust, RefWhen
from virtualenv.create.via_global_ref.builtin.via_global_self_do import ViaGlobalRefVirtualenvBuiltin


class PyPy(ViaGlobalRefVirtualenvBuiltin, abc.ABC):
    @property
    def stdlib(self):
        return self.dest / "lib-python" / f"{self.interpreter.version_info.major}.{self.interpreter.version_info.minor}"

    @property
    def site_packages(self):
        return self.dest / "site-packages"

    @property
    def exe(self):
        return self.dest / self.interpreter.exe.name

    @property
    def bin_dir(self):
        return self.dest / "bin"

    def ensure_directories(self):
        dirs = [self.stdlib, self.site_packages, self.bin_dir]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

    def set_pypy_exe(self):
        src = self.interpreter.exe
        dst = self.exe
        if not dst.exists():
            dst.symlink_to(src)

    def create(self):
        self.ensure_directories()
        self.set_pypy_exe()
        super().create()

    @property
    def sources(self):
        return {
            "stdlib": RefMust(self.interpreter.stdlib, self.stdlib, RefWhen.ANY),
            "site-packages": RefMust(self.interpreter.site_packages, self.site_packages, RefWhen.ANY),
            "executable": PathRefToDest(self.interpreter.exe, self.exe),
        }


__all__ = ['PyPy']
