import logging
import sys
from unittest import TestCase, main
from EmitUtil import EmitUtil

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Test_EmitUtil(TestCase):
    def setUp(self):
        self.eu = EmitUtil()

    def test_proc_options(self):
        self.assertTrue(True)


if __name__ == '__main__':
    main()
