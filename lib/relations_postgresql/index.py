"""–
Module for Column DDL
"""

# pylint: disable=unused-argument

import relations_sql
import relations_postgresql


class INDEX(relations_postgresql.DDL, relations_sql.INDEX):
    """
    INDEX DDL
    """

    TABLE = relations_postgresql.TABLE_NAME
    COLUMNS = relations_postgresql.COLUMN_NAMES

    CREATE = "INDEX"
    MODIFY = "ALTER INDEX RENAME %s TO %s"


class UNIQUE(INDEX):
    """
    UNIQUE INDEX DDL
    """

    CREATE = "UNIQUE INDEX"
