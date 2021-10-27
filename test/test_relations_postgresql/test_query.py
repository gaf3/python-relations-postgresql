import unittest
import unittest.mock

from relations_postgresql import *


class TestSELECT(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        query = SELECT("*").OPTIONS("FAST").FROM("people").WHERE(stuff__gt="things")

        query.generate()
        self.assertEqual(query.sql, """SELECT FAST * FROM "people" WHERE "stuff">%s""")
        self.assertEqual(query.args, ["things"])

        query = SELECT(
            "*"
        ).OPTIONS(
            "FAST"
        ).FROM(
            people=SELECT(
                "a.b.c"
            ).FROM(
                "d.e"
            )
        ).WHERE(
            stuff__in=SELECT(
                "f"
            ).FROM(
                "g"
            ).WHERE(
                things__a__0___1____2_____3__gt=5
            )
        )

        query.generate()
        self.assertEqual(query.sql,
            """SELECT FAST * FROM (SELECT "a"."b"."c" FROM "d"."e") """
            """AS "people" WHERE "stuff" IN """
            """(SELECT "f" FROM "g" WHERE ("things"#>>%s)::JSONB>(%s)::JSONB)"""
        )
        self.assertEqual(query.args, ['{a,0,-1,"2","-3"}', "5"])

        query.GROUP_BY("fee", "fie").HAVING(foe="fum").ORDER_BY("yin", yang=DESC).LIMIT(1, 2)

        query.generate()
        self.assertEqual(query.sql,
            """SELECT FAST * FROM (SELECT "a"."b"."c" FROM "d"."e") """
            """AS "people" WHERE "stuff" IN """
            """(SELECT "f" FROM "g" WHERE ("things"#>>%s)::JSONB>(%s)::JSONB) """
            """GROUP BY "fee","fie" HAVING "foe"=%s """
            """ORDER BY "yin","yang" DESC LIMIT %s OFFSET %s"""
        )
        self.assertEqual(query.args, ['{a,0,-1,"2","-3"}', "5", 'fum', 1, 2])

        query.WHERE(more="stuff").HAVING(more="things")
        query.generate(indent=2)
        self.assertEqual(query.sql,"""SELECT
  FAST
  *
FROM
  (
    SELECT
      "a"."b"."c"
    FROM
      "d"."e"
  ) AS "people"
WHERE
  "stuff" IN (
    SELECT
      "f"
    FROM
      "g"
    WHERE
      ("things"#>>%s)::JSONB>(%s)::JSONB
  ) AND
  "more"=%s
GROUP BY
  "fee",
  "fie"
HAVING
  "foe"=%s AND
  "more"=%s
ORDER BY
  "yin",
  "yang" DESC
LIMIT %s OFFSET %s""")

        query.generate(indent=2, count=1)
        self.assertEqual(query.sql,"""SELECT
    FAST
    *
  FROM
    (
      SELECT
        "a"."b"."c"
      FROM
        "d"."e"
    ) AS "people"
  WHERE
    "stuff" IN (
      SELECT
        "f"
      FROM
        "g"
      WHERE
        ("things"#>>%s)::JSONB>(%s)::JSONB
    ) AND
    "more"=%s
  GROUP BY
    "fee",
    "fie"
  HAVING
    "foe"=%s AND
    "more"=%s
  ORDER BY
    "yin",
    "yang" DESC
  LIMIT %s OFFSET %s""")

        query.generate(indent=2, count=2)
        self.assertEqual(query.sql,"""SELECT
      FAST
      *
    FROM
      (
        SELECT
          "a"."b"."c"
        FROM
          "d"."e"
      ) AS "people"
    WHERE
      "stuff" IN (
        SELECT
          "f"
        FROM
          "g"
        WHERE
          ("things"#>>%s)::JSONB>(%s)::JSONB
      ) AND
      "more"=%s
    GROUP BY
      "fee",
      "fie"
    HAVING
      "foe"=%s AND
      "more"=%s
    ORDER BY
      "yin",
      "yang" DESC
    LIMIT %s OFFSET %s""")


class TestINSERT(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        query = INSERT("people").VALUES(stuff=1, things=2).VALUES(3, 4)

        query.generate()
        self.assertEqual(query.sql,"""INSERT INTO "people" ("stuff","things") VALUES (%s,%s),(%s,%s)""")
        self.assertEqual(query.args, [1, 2, 3, 4])

        query.generate(indent=2)
        self.assertEqual(query.sql,"""INSERT
INTO
  "people"
  (
    "stuff",
    "things"
  )
VALUES
  (
    %s,
    %s
  ),(
    %s,
    %s
  )""")

        query.generate(indent=2, count=1)
        self.assertEqual(query.sql,"""INSERT
  INTO
    "people"
    (
      "stuff",
      "things"
    )
  VALUES
    (
      %s,
      %s
    ),(
      %s,
      %s
    )""")

        query.generate(indent=2, count=2)
        self.assertEqual(query.sql,"""INSERT
    INTO
      "people"
      (
        "stuff",
        "things"
      )
    VALUES
      (
        %s,
        %s
      ),(
        %s,
        %s
      )""")

        query = INSERT("people").OPTIONS("FAST")
        query.SELECT("stuff").FROM("things")

        query.generate()
        self.assertEqual(query.sql,"""INSERT FAST INTO "people" SELECT "stuff" FROM "things\"""")
        self.assertEqual(query.args, [])

        query.generate(indent=2)
        self.assertEqual(query.sql,"""INSERT
  FAST
INTO
  "people"
SELECT
  "stuff"
FROM
  "things\"""")

        query.generate(indent=2, count=1)
        self.assertEqual(query.sql,"""INSERT
    FAST
  INTO
    "people"
  SELECT
    "stuff"
  FROM
    "things\"""")

        query.generate(indent=2, count=2)
        self.assertEqual(query.sql,"""INSERT
      FAST
    INTO
      "people"
    SELECT
      "stuff"
    FROM
      "things\"""")

        query = INSERT("people").VALUES(stuff=1, things=2).VALUES(3, 4)
        query.SELECT("stuff").FROM("things")

        self.assertRaisesRegex(relations_sql.SQLError, "set VALUES or SELECT but not both", query.generate)


class TestUPDATE(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        query = UPDATE("people").SET(stuff="things").WHERE(things="stuff")
        query.OPTIONS("FAST").ORDER_BY("yin", yang=DESC).LIMIT(5)

        query.generate()
        self.assertEqual(query.sql, """UPDATE FAST "people" SET "stuff"=%s WHERE "things"=%s ORDER BY "yin","yang" DESC LIMIT %s""")
        self.assertEqual(query.args, ["things", "stuff", 5])

        query.generate(indent=2)
        self.assertEqual(query.sql,"""UPDATE
  FAST
  "people"
SET
  "stuff"=%s
WHERE
  "things"=%s
ORDER BY
  "yin",
  "yang" DESC
LIMIT %s""")

        query.generate(indent=2, count=1)
        self.assertEqual(query.sql,"""UPDATE
    FAST
    "people"
  SET
    "stuff"=%s
  WHERE
    "things"=%s
  ORDER BY
    "yin",
    "yang" DESC
  LIMIT %s""")

        query.generate(indent=2, count=2)
        self.assertEqual(query.sql,"""UPDATE
      FAST
      "people"
    SET
      "stuff"=%s
    WHERE
      "things"=%s
    ORDER BY
      "yin",
      "yang" DESC
    LIMIT %s""")

        query.LIMIT(10)

        self.assertRaisesRegex(relations_sql.SQLError, "LIMIT can only be total", query.generate)


class TestDELETE(unittest.TestCase):

    maxDiff = None

    def test_generate(self):

        query = DELETE("people").WHERE(things="stuff")
        query.OPTIONS("FAST").ORDER_BY("yin", yang=DESC).LIMIT(5)

        query.generate()
        self.assertEqual(query.sql, """DELETE FAST FROM "people" WHERE "things"=%s ORDER BY "yin","yang" DESC LIMIT %s""")
        self.assertEqual(query.args, ["stuff", 5])

        query.generate(indent=2)
        self.assertEqual(query.sql,"""DELETE
  FAST
FROM
  "people"
WHERE
  "things"=%s
ORDER BY
  "yin",
  "yang" DESC
LIMIT %s""")

        query.generate(indent=2, count=1)
        self.assertEqual(query.sql,"""DELETE
    FAST
  FROM
    "people"
  WHERE
    "things"=%s
  ORDER BY
    "yin",
    "yang" DESC
  LIMIT %s""")

        query.generate(indent=2, count=2)
        self.assertEqual(query.sql,"""DELETE
      FAST
    FROM
      "people"
    WHERE
      "things"=%s
    ORDER BY
      "yin",
      "yang" DESC
    LIMIT %s""")

        query.LIMIT(10)

        self.assertRaisesRegex(relations_sql.SQLError, "LIMIT can only be total", query.generate)
