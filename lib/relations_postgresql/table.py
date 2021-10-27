"""–
Module for Column DDL
"""

# pylint: disable=unused-argument

import relations_sql
import relations_postgresql


class TABLE(relations_postgresql.DDL, relations_sql.TABLE):
    """
    TABLE DDL
    """

    NAME = relations_postgresql.TABLE_NAME
    COLUMN = relations_postgresql.COLUMN
    INDEX = relations_postgresql.INDEX
    UNIQUE = relations_postgresql.UNIQUE

    INDEXES = False

    SCHEMA = """ALTER TABLE %s SET SCHEMA %s"""
    STORE = """ALTER TABLE %s RENAME TO %s"""
    PRIMARY = """PRIMARY KEY (%s)"""
