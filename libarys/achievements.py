import configparser
import json

import discord

from . import UserConnector

achiDict = {}


def loadAchi():
    achiIni = configparser.ConfigParser()
    achiIni.read('save/achievement.ini')
    for x in achiIni.sections():
        achiType, achiAction = achiIni[x]["type"].split("-")
        if not achiDict.__contains__(achiType): achiDict[achiType] = {}
        if not achiDict[achiType].__contains__(achiAction): achiDict[achiType][achiAction] = {}
        achiDict[achiType][achiAction][x] = {"name": achiIni[x]['name'], "progress":  int(achiIni[x]['progress']), "type": achiIni[x]["type"]}
        achiDict[x] = {"name": achiIni[x]['name'], "progress": int(achiIni[x]['progress']), "action": achiAction}
    print(achiDict)

loadAchi()


class Achievements:
    api: UserConnector.Connect = None
    loadedUser = {}

    def __init__(self, user_id: int, message: discord.Message):
        self.user_id = user_id
        self.message = message
        self.achievement = {}
        if self.loadedUser.__contains__(user_id):
            self.achievement = self.loadedUser[user_id]
        else:
            self.loadAchievement()

    def loadAchievement(self):
        """Lade die Erfolge eines Users, wird automatisch beim klassen aufruf ausgeführt"""
        self.achievement.clear()
        result = json.loads(self.api.userGet(self.user_id, 'achievements'))
        for x in result.copy():
            result[x]['name'] = achiDict[x]['name']
            result[x]['progress'] = [result[x]['progress'], achiDict[x]['progress']]
        self.achievement = result

    def getAchievements(self) -> list:
        """Frage alle gemachten Erfolge an (keinen fortschritt)"""
        result = json.loads(self.api.userGet(self.user_id, 'achievements'))
        finished = []
        for x in result:
            if result[x]['progress'] >= achiDict[x]['progress']:
                finished.append(achiDict[x]['name'])
        return finished

    def getAllAchievements(self) -> dict:
        """Frage alle Erfolge an + Fortschritt"""
        result = json.loads(self.api.userGet(self.user_id, 'achievements'))
        for x in result.copy():
            result[x]['name'] = achiDict[x]['name']
            result[x]['progress'] = [result[x]['progress'], achiDict[x]['progress']]
        return result

    def getAchievement(self, achievement: str) -> dict:
        """Frage Information zu einem bestimmten Erfolg an"""
        if self.achievement.__contains__(achievement):
            return self.achievement[achievement]
        return {}

    def saveAchievements(self):
        """Speichere die Achievements"""
        self.loadedUser[self.user_id] = self.achievement.copy()
        saveDict = {}
        for a in self.achievement.copy():
            saveDict[a] = {
                "name": self.achievement[a]["name"],
                "progress": self.achievement[a]["progress"][0]
            }
        self.api.userUpdate(self.user_id, 'achievements', json.dumps(saveDict))

    def unlockAchievement(self, achievement: str):
        """Schalte ein Erfolg Frei"""
        achi = self.getAchievement(achievement)
        achi["progress"] = [achiDict[achievement]['progress'], 0]
        self.achievement[achievement] = achi

    async def progressAchievement(self, achiType: str, achiAction: str, progress: int = 1):
        """Füge fortschritt zum Erfolg hinzu"""
        if not achiDict.__contains__(achiType): return
        if not achiDict[achiType].__contains__(achiAction): return
        achivs = achiDict[achiType][achiAction].copy()
        for a in achivs:
            if not self.achievement.__contains__(a):
                self.achievement[a] = {}
                self.achievement[a]['name'] = achiDict[a]['name']
                self.achievement[a]['progress'] = [0, achiDict[a]['progress']]
            if self.achievement[a]['progress'][0] < self.achievement[a]['progress'][1]:
                self.achievement[a]['progress'][0] += progress
                if self.achievement[a]['progress'][0] >= self.achievement[a]['progress'][1]:
                    self.unlockAchievement(a); await self.sendAchievementMessage(a)
        #print(self.achievement)
        self.saveAchievements()
        #print(self.achievement)

    def lockAchievment(self, achievement: str):
        """Entferne einen Bestimmten Erfolg"""
        pass

    async def sendAchievementMessage(self, achievement: str):
        await self.message.channel.send(embed=discord.Embed(
            title=":star: Achievement unlocked",
            description=achiDict[achievement]['name']
        ))