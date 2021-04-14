import os
import sys
import unittest

# to import testdocgen package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from testdocgen.mdparser import MdParser


class TestMdparser(unittest.TestCase):
    def test_split_by_symbol(self):
        #TODO: impl

if __name__ == "__main__":
    unittest.main()