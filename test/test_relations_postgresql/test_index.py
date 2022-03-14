import unittest
import unittest.mock

import relations
from relations_postgresql import *


class TestINDEX(unittest.TestCase):

    maxDiff = None

    def test_modify(self):

        ddl = INDEX(name="people", columns=["stuff", "things"], definition={"name": "persons"})

        ddl.modify()
        self.assertEqual(ddl.sql, """ALTER INDEX "persons" RENAME TO "people\"""")

        ddl = INDEX(
            schema="people", table="stuff", name="things",
            columns=["persons", "stuff__ins"], definition={
                "name": "persons",
                "table": {
                    "name": "stuff",
                    "schema": "people"
                }
            }
        )

        ddl.modify()
        self.assertEqual(ddl.sql, """ALTER INDEX "people"."stuff_persons" RENAME TO "stuff_things\"""")

    def test_generate(self):

        ddl = INDEX(name="people", columns=["stuff", "things"])

        ddl.generate()
        self.assertEqual(ddl.sql, """INDEX "people" ("stuff","things")""")
        self.assertEqual(ddl.args, [])

        ddl = INDEX(name="people", columns=["stuff", "things"], added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD INDEX "people" ("stuff","things")""")
        self.assertEqual(ddl.args, [])

        ddl = INDEX(name="people", columns=["stuff", "things"], definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER INDEX "persons" RENAME TO "people\"""")
        self.assertEqual(ddl.args, [])

        ddl = INDEX(definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, """DROP INDEX "persons\"""")
        self.assertEqual(ddl.args, [])


class TestUNIQUE(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        ddl = UNIQUE(name="people", columns=["stuff", "things"])

        ddl.generate()
        self.assertEqual(ddl.sql, """UNIQUE INDEX "people" ("stuff","things")""")
        self.assertEqual(ddl.args, [])

        ddl = UNIQUE(name="people", columns=["stuff", "things"], added=True)

        ddl.generate()
        self.assertEqual(ddl.sql, """ADD UNIQUE INDEX "people" ("stuff","things")""")
        self.assertEqual(ddl.args, [])

        ddl = UNIQUE(name="people", columns=["stuff", "things"], definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, """ALTER INDEX "persons" RENAME TO "people\"""")
        self.assertEqual(ddl.args, [])

        ddl = UNIQUE(definition={"name": "persons"})

        ddl.generate()
        self.assertEqual(ddl.sql, """DROP INDEX "persons\"""")
        self.assertEqual(ddl.args, [])
