import unittest
import unittest.mock

from relations_postgresql import *


class TestDDL(unittest.TestCase):

    maxDiff = None

    def test_class(self):

        self.assertEqual(DDL.QUOTE, """\"""")
        self.assertEqual(DDL.STR, """'""")
        self.assertEqual(DDL.SEPARATOR, """.""")
        self.assertEqual(DDL.PLACEHOLDER, """%s""")
        self.assertEqual(DDL.JSONIFY, """(%s)::JSONB""")
        self.assertEqual(DDL.PATH, """%s#>>%s""")
