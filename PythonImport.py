from abc import ABC, abstractmethod
import logging
from collections import defaultdict

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PythonImport(ABC):
    """
    This is an abstract base class for Python imports.
    It follows a Bridge (Structural) design pattern.
    """
    def __init__(self):
        self._libs = {}

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
            pass
            self.libs[lib].add(method)
            pass
        else:
            # For adding the full lib, like "import sys"
            self.libs[lib] = set()
        return self.libs