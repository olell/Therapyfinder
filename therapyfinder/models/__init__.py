"""
Therapistfinder - therapistfinder/models/__init__.py

Author/s: olel
Therapistfinder (thus this code) is public domain.
"""

# Global imports
from peewee import SqliteDatabase # Todo: support other database types

# Local imports

class Database(object):
    # Singleton database container
    instance = None

    @staticmethod
    def get():
        if Database.instance is not None:
            return Database.instance._db
        else:
            Database()
            return Database.instance._db

    @staticmethod
    def register_models(*models):
        db = Database.get()
        db.create_tables(models)

    def __init__(self):
        # Don't override existing instance
        if Database.instance is not None:
            return
        Database.instance = self

        self._db = SqliteDatabase("db_dev.sqlite3") # Todo: db configuration