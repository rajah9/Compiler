import logging
from unittest import mock, TestCase, main
from EmitterUtil import EmitterUtil
from LogitUtil import logit
from CollectionUtil import CollectionUtil
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Interesting Python features:
"""

class Test_EmitterUtil(TestCase):
    def setUp(self):
        self._eu = EmitterUtil()

    @logit()
    def test_emit(self):
        self._eu.emit()

    @logit()
    def test_preamble(self):
        cu = CollectionUtil()
        currentYear = datetime.today().strftime("%Y")
        exp = f'Copyright {currentYear}'
        act = self._eu.preamble()
        self.assertTrue(cu.any_string_contains(lines=act, find_me=exp))

    @logit()
    def test_emit_body(self):
        # Test 1, empty list (header only)
        act1 = self._eu.emit_body()
        self.assertTrue("body" in act1[2], "fail test 1")
        # Test 2, add several lines.
        lines = ['one', 'two', 'three', 'four']
        array_len = len(lines)
        self._eu.add_to_body(lines)
        act2 = self._eu.emit_body()
        for i in range(array_len):
            self.assertEqual(lines.pop(), act2.pop(), f'fail test 2 (item {array_len - i}')

    @logit()
    def test_add_to_body(self):
        # Test 1. Single line.
        line = 'First'
        exp = [line]
        self._eu.add_to_body(line)
        act1 = self._eu.emit_body()
        self.assertTrue(line in act1[5], 'fail test 1')
        # Test 2. Add 2 lines.
        lines = ['second', 'third']
        self._eu.add_to_body(lines)
        act2 = self._eu.emit_body()
        self.assertEqual(lines.pop(), act2.pop(), 'fail test 2 (last item)')
        self.assertEqual(lines.pop(), act2.pop(), 'fail test 2 (penultimate item)')


if __name__ == '__main__':
    main()
