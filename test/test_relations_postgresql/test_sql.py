import unittest
import unittest.mock

from relations_postgresql import *


class TestSQL(unittest.TestCase):

    maxDiff = None

    def test_class(self):

        self.assertEqual(SQL.QUOTE, """\"""")
        self.assertEqual(SQL.STR, """'""")
        self.assertEqual(SQL.SEPARATOR, """.""")
        self.assertEqual(SQL.PLACEHOLDER, """%s""")
        self.assertEqual(SQL.JSONIFY, """(%s)::JSONB""")
        self.assertEqual(SQL.PATH, """%s#>>%s""")
