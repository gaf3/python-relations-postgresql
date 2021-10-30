import unittest
import unittest.mock

import relations_sql

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

    def test_walk(self):

        column, path = relations_sql.SQL.split("things__a__b__0____1")
        self.assertEqual(SQL.walk(path), '{a,b,0,"1"}')
