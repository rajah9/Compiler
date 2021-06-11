import sys
from pathlib import Path
import logging
from unittest import mock, TestCase, main
from PythonImport import PandasStyleImport, PythonStyleImport
sys.path.insert(0, '../../Utilities') # Fix for where your Utilities dir is.
from LogitUtil import logit


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Interesting Python features:
"""

class Test_PythonImport(TestCase):
    pass

class Test_PandasStyleImport(Test_PythonImport):
    def setUp(self):
        self.pd = PandasStyleImport()

    @logit()
    def test_add_lib_method(self):
        # Test 1. Add a single alias. The dictionary returned must be the same as the property.
        lib1 = 'pandas'
        alias1 = 'pd'
        exp1 = {lib1: alias1}
        d = self.pd.add_lib_method(lib=lib1,alias=alias1)
        self.assertEqual(exp1, d, 'fail test 1')

class Test_PythonStyleImport(Test_PythonImport):
    def setUp(self):
        self.py = PythonStyleImport()

    @logit()
    def test_add_lib_method(self):
        # Test 1. Add a single method. Should return a set with just that method.
        lib1 = 'collections'
        method1 = 'defaultdict'
        set1 = set([method1])
        exp1 = {lib1: set1}
        act1 = self.py.add_lib_method(lib=lib1, method=method1)
        self.assertEqual(exp1, act1, 'fail test 1')
        # Test 2. Add a second method.
        method2 = 'OrderedDict'
        set2 = set([method1, method2])
        exp2 = {lib1: set2}
        act2 = self.py.add_lib_method(lib=lib1, method=method2)
        self.assertEqual(exp2, act2, 'fail test 2')
        # Test 3. Adding an identical method should not change the contents.
        act3 = self.py.add_lib_method(lib=lib1, method=method1)
        self.assertEqual(exp2, act3, 'fail test 3')
        # Test 4. Add a bare library with no method.
        lib4 = 'sys'
        exp4 = exp2
        exp4[lib4] = set()
        act4 = self.py.add_lib_method(lib=lib4)
        self.assertEqual(exp4, act4, 'fail test 4')

if __name__ == '__main__':
    main()
