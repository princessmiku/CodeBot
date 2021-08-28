import discord, sqini, json, datetime
from dataSecret import tokens

from libarys import achievements as achiSys, commands as libCommandsF, database as libDatabaseF, getRole, leveling, pageEmbed, UserConnector

"""
Settings des Code Bots
hier werden alle festen Werte Konfiguriert

Außerdem gilt die datei der Verwaltung und verbindung aller Module
"""

# discord bot basic config
client = discord.Client(intents=discord.Intents.all())
client_prefix = "!"
client_version = "0.1"

client_owner_id = 293135882926555137
client_mainGuild_id = 879990188317749309
client_team_id = 879996983824228362

# basic config von der datenbank
database_path = "./save/data.db"
database_sync = True

database_sqini = sqini.Database(canDelete=True); database_sqini.read(database_path)
if database_sync: database_sqini.syncToDatabase()
database = libDatabaseF.Connect(database_sqini.db)
api = UserConnector.Connect(database)



# commands
commands = libCommandsF.Commands(client_prefix)
from commands import usercmds, funcmds, admincmds, botTeamCmds, programmingcmds, guildcmds



# set values
achiSys.Achievements.api = api
libCommandsF.api = api
leveling.api = api
libCommandsF.owner_id, libCommandsF.team_role, libCommandsF.main_guild = client_owner_id, client_team_id, client_mainGuild_id
