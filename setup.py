#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="relations-postgresql",
    version="0.2.0",
    package_dir = {'': 'lib'},
    py_modules = [
        'relations_postgresql',
        'relations_postgresql.sql',
        'relations_postgresql.expression',
        'relations_postgresql.criterion',
        'relations_postgresql.criteria',
        'relations_postgresql.clause',
        'relations_postgresql.query',
        'relations_postgresql.ddl',
        'relations_postgresql.column',
        'relations_postgresql.index',
        'relations_postgresql.table'
    ],
    install_requires=[]
)
