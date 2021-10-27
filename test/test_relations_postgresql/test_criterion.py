import unittest
import unittest.mock

from relations_postgresql import *



class TestNULL(unittest.TestCase):

    def test_generate(self):

        criterion = NULL("totes", True)

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes" IS NULL""")
        self.assertEqual(criterion.args, [])

        criterion = NULL(totes__a=False)

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB IS NOT NULL""")
        self.assertEqual(criterion.args, ['{a}'])


class TestEQ(unittest.TestCase):

    def test_generate(self):

        criterion = EQ("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes"=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = EQ("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes"!=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = EQ(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB=(%s)::JSONB""")
        self.assertEqual(criterion.args, ['{a}', '"maigoats"'])


class TestGT(unittest.TestCase):

    def test_generate(self):

        criterion = GT("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes">%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = GT(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB>(%s)::JSONB""")
        self.assertEqual(criterion.args, ['{a}', '"maigoats"'])


class TestGTE(unittest.TestCase):

    def test_generate(self):

        criterion = GTE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes">=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = GTE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB>=(%s)::JSONB""")
        self.assertEqual(criterion.args, ['{a}', '"maigoats"'])


class TestLT(unittest.TestCase):

    def test_generate(self):

        criterion = LT("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes"<%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = LT(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB<(%s)::JSONB""")
        self.assertEqual(criterion.args, ['{a}', '"maigoats"'])


class TestLTE(unittest.TestCase):

    def test_generate(self):

        criterion = LTE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes"<=%s""")
        self.assertEqual(criterion.args, ["maigoats"])

        criterion = LTE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB<=(%s)::JSONB""")
        self.assertEqual(criterion.args, ['{a}', '"maigoats"'])


class TestLIKE(unittest.TestCase):

    def test_generate(self):

        criterion = LIKE("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::VARCHAR(255) LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ["%maigoats%"])

        criterion = LIKE("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::VARCHAR(255) NOT LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ["%maigoats%"])

        criterion = LIKE(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::VARCHAR(255) LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ['{a}', '%maigoats%'])


class TestSTART(unittest.TestCase):

    def test_generate(self):

        criterion = START("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::VARCHAR(255) LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ["maigoats%"])

        criterion = START("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::VARCHAR(255) NOT LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ["maigoats%"])

        criterion = START(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::VARCHAR(255) LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ['{a}', 'maigoats%'])


class TestEND(unittest.TestCase):

    def test_generate(self):

        criterion = END("totes", "maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::VARCHAR(255) LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ["%maigoats"])

        criterion = END("totes", "maigoats", invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::VARCHAR(255) NOT LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ["%maigoats"])

        criterion = END(totes__a="maigoats")

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::VARCHAR(255) LIKE (%s)::VARCHAR(255)""")
        self.assertEqual(criterion.args, ['{a}', '%maigoats'])


class TestIN(unittest.TestCase):

    def test_generate(self):

        criterion = IN("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes" IN (%s,%s)""")
        self.assertEqual(criterion.args, ["mai", "goats"])

        criterion = IN("totes", ["mai", "goats"], invert=True)

        criterion.generate()
        self.assertEqual(criterion.sql, """"totes" NOT IN (%s,%s)""")
        self.assertEqual(criterion.args, ["mai", "goats"])

        criterion = IN(totes__a=["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes"#>>%s)::JSONB IN ((%s)::JSONB,(%s)::JSONB)""")
        self.assertEqual(criterion.args, ['{a}', '"mai"', '"goats"'])

        criterion = IN(totes__a=[])

        criterion.generate()
        self.assertEqual(criterion.sql, """%s""")
        self.assertEqual(criterion.args, [False])


class TestCONTAINS(unittest.TestCase):

    def test_generate(self):

        criterion = CONTAINS("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """("totes")::JSONB @> (%s)::JSONB""")
        self.assertEqual(criterion.args, ['["mai", "goats"]'])


class TestLENGTHS(unittest.TestCase):

    def test_generate(self):

        criterion = LENGTHS("totes", ["mai", "goats"])

        criterion.generate()
        self.assertEqual(criterion.sql, """jsonb_array_length(("totes")::JSONB)=jsonb_array_length((%s)::JSONB)""")
        self.assertEqual(criterion.args, ['["mai", "goats"]'])
