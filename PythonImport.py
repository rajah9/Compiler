import sys
from abc import ABC, abstractmethod
import logging
from collections import defaultdict
sys.path.insert(0, '../../Utilities') # Fix for where your Utilities dir is.
from StringUtil import LineAccmulator

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PythonImport(ABC):
    """
    This is an abstract base class for Python imports.
    It follows a Bridge (Structural) design pattern.
    """
    def __init__(self):
        self._libs = {}
        self._emitter = LineAccmulator()

    @property
    def libs(self) -> dict:
        return self._libs

    @libs.setter
    def libs(self, d: dict):
        self._libs = d

    @abstractmethod
    def add_lib_method(self, lib: str):
        """
        Add the library
        :return:
        """
        raise NotImplementedError('Must be implemented by concrete classes')

    @abstractmethod
    def emit(self):
        """
        Emit the contents to LineAccumulator. (You may access the contents through emission().)
        :return:
        """
        raise NotImplementedError('Must be implemented by concrete classes')

    def emission(self) -> list:
        """
        (Call emit() first.)
        Provide the contents of the LineAccumlator.
        :return:
        """
        return self._emitter.contents

    def add_line_to_emission(self, line: str):
        """
        Add the given line to the LineAccumulator.
        :param line: line to append, such as 'import pandas as pd'
        :return:
        """
        self._emitter.add_line(line)


class PandasStyleImport(PythonImport):
    """
    This class is for a Pandas style import with an alias, like
      import pandas as pd
      import numpy as np
    """
    def __init__(self):
        super(PandasStyleImport, self).__init__()

    def add_lib_method(self, lib: str, alias: str) -> dict:
        """
        Add the method to the dictionary.
        :param lib: library name, like numpy
        :param alias: library alias, like np
        :return: dict with the new entry.
        """
        self.libs[lib] = alias
        return self.libs

    def emit(self):
        d = self.libs
        for lib, alias in d.items():
            line = f'import {lib} as {alias}'
            logger.debug(f'emitting Pandas-style import: <{line}>')
            self.add_line_to_emission(line)


class PythonStyleImport(PythonImport):
    """
    This class is for the traditional Python import, like
      import sys
      from collections import defaultdict
    """
    def __init__(self):
        super(PythonStyleImport, self).__init__()
        self.libs = defaultdict(lambda: set())

    def add_lib_method(self, lib: str, method: str = None):
        """
        Add the method to the library (or just the lib, if method is not specified).
        :param lib: library name, like collections
        :param method: method name, like defaultdict
        :return: dict with the new entry.
        """
        if method:
            # For adding a method to the lib, like "from collections import defaultdict"
            self.libs[lib].add(method)
        else:
            # For adding the full lib, like "import sys"
            self.libs[lib] = set()
        return self.libs

    def emit(self):
        for lib, methods in self.libs.items():
            if methods == set():
                # Empty set. import the whole lib.
                line = f'import {lib}'
            else:
                # Non-empty set. import the given methods.
                sorted_methods = list(methods)
                sorted_methods.sort()
                methods_str = ", ".join(sorted_methods)
                line = f'from {lib} import {methods_str}'
            logger.debug(f'emitting Python-style import: <{line}>')
            self.add_line_to_emission(line)
