from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
import sqlite3

from eel.values import Number, Null, String, BaseType, List


class SqliteModule(EelModule):
    @staticmethod
    @eel_function
    def connect(database: String):  # TODO: Add other optional args
        return RTResult().success(DatabaseConnection(sqlite3.connect(database.value)))

    @staticmethod
    @eel_function
    def cursor(connection: "DatabaseConnection"):
        return RTResult().success(DatabaseCursor(connection.cursor()))

    @staticmethod
    @eel_function
    def execute(cursor: "DatabaseCursor", query: String):
        cursor.cursor.execute(query.value)
        return RTResult().success(Null())

    @staticmethod
    @eel_function
    def fetchall(cursor: "DatabaseCursor"):
        result = cursor.cursor.fetchall()

        # TODO: I would like to convert result to a list of dictionaries

        return RTResult().success(List(result))


class DatabaseConnection(BaseType):
    def __init__(self, connection):
        super().__init__()
        self.conn: sqlite3.Connection = connection
        self.type = "DatabaseConnection"

    def copy(self):
        return DatabaseConnection(self.conn)

    def __repr__(self):
        return f"DatabaseConnection {str(self.conn)}"

    def __getattr__(self, item):
        return getattr(self.conn, item)


class DatabaseCursor(BaseType):
    def __init__(self, cursor):
        super().__init__()
        self.cursor: sqlite3.Cursor = cursor
        self.type = "DatabaseConnection"

    def copy(self):
        return DatabaseCursor(self.cursor)

    def __repr__(self):
        return f"DatabaseCursor {str(self.cursor)}"

    def __getattr__(self, item):
        return getattr(self.cursor, item)


SqliteModule.initialize()
