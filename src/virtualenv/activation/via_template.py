from __future__ import annotations
import os
import sys
from abc import ABC, abstractmethod
from .activator import Activator
if sys.version_info >= (3, 10):
    from importlib.resources import files
else:
    from importlib.resources import read_binary


class ViaTemplateActivator(Activator, ABC):
    @abstractmethod
    def templates(self):
        pass

    def generate(self, creator):
        dest_folder = creator.bin_dir
        replacements = self.replacements(creator, dest_folder)
        generated = {}
        for template in self.templates():
            text = self.instantiate_template(replacements, template, creator)
            dest = os.path.join(dest_folder, self.as_name(template))
            generated[dest] = text
        return generated

    @abstractmethod
    def replacements(self, creator, dest_folder):
        pass

    def instantiate_template(self, replacements, template, creator):
        if sys.version_info >= (3, 10):
            text = files(self.__class__).joinpath(template).read_text()
        else:
            text = read_binary(self.__class__, template).decode('utf-8')
        for key, value in replacements.items():
            text = text.replace(key.encode('utf-8'), value.encode('utf-8')).decode('utf-8')
        return text

    @staticmethod
    def as_name(template):
        return template


__all__ = ['ViaTemplateActivator']
