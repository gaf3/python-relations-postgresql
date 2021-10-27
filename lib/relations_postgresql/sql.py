"""
Base SQL module for all of PostgreSQL SQL
"""


class SQL: # pylint: disable=too-few-public-methods
    """
    Base class for every PostgreSQL expression storing constants
    """

    QUOTE = '"'
    STR = "'"
    SEPARATOR = '.'
    PLACEHOLDER = "%s"
    JSONIFY = "(%s)::JSONB"
    PATH = "%s#>>%s"
