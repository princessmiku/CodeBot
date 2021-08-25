import datetime
import sqlite3, os

class Connect:

    def __init__(self, connection: sqlite3.Connection):
        self.db = connection

    def setSingle(self, id: int, table: str, column: str, value):
        """Setze eine einzelne Variable"""
        if isinstance(value, int): self.db.execute(f"UPDATE {table} SET {column}={str(value)} WHERE id={str(id)}")
        else: self.db.execute(f"UPDATE {table} SET {column}='{str(value)}' WHERE id={str(id)}")
        self.db.commit()

    def getSingle(self, id: int, table: str, column: str):
        """Fordere eine einzige Variable an"""
        return self.db.execute(f"SELECT {column} FROM {table} WHERE id={str(id)}").fetchone()[0]

    def userVlaue(self, id: int, column: str, value = False):
        """Setze oder fordere eine User Variable an"""
        if value is False: return self.getSingle(id, "user", column)
        self.setSingle(id, "user", column, value)

    def registerUser(self, id: int):
        """Registriere einen neuen User"""
        self.db.execute(f"INSERT OR IGNORE INTO user(id, createat) VALUES ({str(id)}, '{datetime.datetime.today().strftime('%H:%M:%S on %B %d, %Y')}')")
        self.db.commit()
