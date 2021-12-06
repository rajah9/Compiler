import logging
import sys
from unittest import TestCase, main

from ParserUtil import SasParser

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Interesting Python features:
"""

_PROC_TYPE = 'MEANS'
class Test_SasParser(TestCase):
    def setUp(self):
        pass

    def test_proc_data(self):
        s = SasParser()
        s.input_lines = '** comment **;\nPROC MEANS data=Hello; /* comment */\nRUN;'
        s.run()