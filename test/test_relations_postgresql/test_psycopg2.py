import unittest
import unittest.mock

import os
import psycopg2.extras

import relations
import relations_postgresql


class Meta(relations.Model):

    SCHEMA = "test_psycopg2"

    id = int,{"auto": True}
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict, {"extract": "for__0____1"}
    push = str


class TestPsycoPG2(unittest.TestCase):

    maxDiff = None

    def setUp(self):

        connection = psycopg2.connect(
            user="postgres", host=os.environ["POSTGRES_HOST"], port=int(os.environ["POSTGRES_PORT"]),
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('DROP DATABASE IF EXISTS "test_psycopg2"')
        cursor.execute('CREATE DATABASE "test_psycopg2"')

        self.connection = psycopg2.connect(
            dbname="test_psycopg2",
            user="postgres", host=os.environ["POSTGRES_HOST"], port=int(os.environ["POSTGRES_PORT"]),
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute('CREATE SCHEMA "test_psycopg2"')

    def tearDown(self):

        self.connection.close()

        connection = psycopg2.connect(
            user="postgres", host=os.environ["POSTGRES_HOST"], port=int(os.environ["POSTGRES_PORT"]),
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        connection.autocommit = True

        connection.cursor().execute('DROP DATABASE IF EXISTS "test_psycopg2"')

    def test_execute(self):

        cursor = self.connection.cursor()

        ddl = relations_postgresql.TABLE(Meta.thy().define())

        ddl.generate(indent=2)

        cursor.execute(ddl.sql)

        query = relations_postgresql.INSERT(
            "test_psycopg2.meta"
        ).VALUES(**{
            "name": "yep",
            "flag": True,
            "spend": 1.1,
            "people": {"tom"},
            "stuff": [1, None],
            "things": {"a": 1}
        }).VALUES(
            name="dive",
            flag=False,
            spend=3.5,
            people={"tom", "mary"},
            stuff=[1, 2, 3, None],
            things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]}
        )

        query.generate(indent=2)

        cursor.execute(query.sql, query.args)

        def check(value, **kwargs):

            query = relations_postgresql.SELECT(
                "name"
            ).FROM(
                "test_psycopg2.meta"
            ).WHERE(
                **kwargs
            )

            query.generate()

            cursor.execute(query.sql, query.args)

            if cursor.rowcount != 1:
                name = None
            else:
                name = cursor.fetchone()["name"]

            self.assertEqual(name, value, query.sql)

        check("yep", flag=True)

        check("dive", flag=False)

        check("dive", people={"tom", "mary"})

        check("dive", things={"a": {"b": [1, 2], "c": "sure"}, "4": 5, "for": [{"1": "yep"}]})

        check("dive", stuff__1=2)

        check("dive", things__a__b__0=1)

        check("dive", things__a__c__like="su")

        check("yep", things__a__b__null=True)

        check("dive", things____4=5)

        check(None, things__a__b__0__gt=1)

        check(None, things__a__c__not_like="su")

        check(None, things__a__d__null=False)

        check(None, things____4=6)

        check("dive", things__a__b__has=1)

        check(None, things__a__b__has=[1, 3])

        check("dive", name="dive", things__a__b__not_has=[1, 3])

        check("dive", things__a__b__not_has=[1, 3], things__a__b__null=False)

        check("dive", things__a__b__any=[1, 3])

        check(None, things__a__b__any=[4, 3])

        check("dive", things__a__b__all=[2, 1])

        check(None, things__a__b__all=[3, 2, 1])

        check("dive", people__has="mary")

        check(None, people__has="dick")

        check("dive", people__any=["mary", "dick"])

        check(None, people__any=["harry", "dick"])

        check("dive", people__all=["mary", "tom"])

        check(None, people__all=["tom", "dick", "mary"])
