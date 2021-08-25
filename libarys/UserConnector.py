import json
from .database import Connect as databaseConnect

class Connect:

    def __init__(self, database: databaseConnect):
        self.database = database

    def userGet(self, id: int, get: str) -> [int, str, dict]:
        """Fordere bestimmte Daten eines Users an"""
        return self.database.getSingle(id, "user", get)

    def userUpdate(self, id: int, update: str, value: str):
        """Update User Daten"""
        self.database.userVlaue(id, update, value)

    def userAdd(self, id: int, update: str, value: int):
        """Addiere etwas bestimmtes drauf, + oder - möglich durch die Integer Zahl. Verwendungsmöglichkeiten: Geldsystem, Levelsystem"""
        newValue = self.userGet(id, update) + value
        self.userUpdate(id, update, newValue)

    def userKeyUpdate(self, id: int, update: str, key: str, value: str):
        """Update in einem Dict einen bestimmten Key"""
        pass

    def userKeyGet(self, id: int, get: str, key: str) -> [int, str, dict, list]:
        """Fordere bestimmte Daten in einem Dict an"""
        try:
            userDict: dict = json.loads(self.userGet(id, get))
        except:
            return "error"
        try:
            return userDict[key]
        except KeyError:
            return "error"

    def userInsert(self, id: int):
        """Füge einen User in die Datenbank hinzu"""
        self.database.registerUser(id)
