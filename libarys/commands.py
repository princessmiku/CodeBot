import discord

from libarys import etcLib

owner_id = 0
main_guild = 0
team_role = 0

class Commands:
    commands = {}
    helpPages = {}
    helpList = {'empty': []}
    helpEmbed = False
    blockIDs = []
    def __init__(self, prefix):
        self.prefix = prefix
    def register(self, category: str = 'empty', helpList = 'empty', permissions: list = [], userPermissions: list = [], block: bool=False, hidden: bool = False, botOwner: bool = False, botTeam: bool = False):
        """Füge eine funktion als Bot Befehl hinzu, vergesse die message nicht"""
        if botTeam or botOwner:
            hidden = True
        def wrapper(func):
            commandSettings = {
                "permissions": permissions,
                "userPermissions": userPermissions,
                "command": func,
                "block": block,
                "hidden": hidden,
                "botOwner": botOwner,
                "botTeam": botTeam
            }
            if not self.commands.__contains__(func.__name__.lower()):
                self.commands[func.__name__.lower()] = commandSettings
            else:
                print(func.__name__.lower(), "exist already")
            if not hidden:
                if not self.helpList.__contains__(category): self.helpList[category] = []
                self.helpList[category].append(func.__name__.lower())
                self.helpPages[func.__name__.lower()] = helpList
            print("register command:", func.__name__.lower())
            return func
        return wrapper

    async def call(self, message):
        """Command Caller, diese Funktion werte eine Nachricht aus und ruft den Befehl dazu auf mit berücksichtigung der einstellungen dafür"""
        content: str = message.content
        #discord.TextChannel.permissions_for()  print(perm.__getattribute__('send_messages'))
        #discord.Permissions().send_messages
        if not content.startswith(self.prefix): return False
        channel = message.channel
        invoke: str = message.content.split()[0][len(self.prefix):]
        if not self.commands.__contains__(invoke.lower()): return False
        if not channel.permissions_for(message.guild.me).send_messages: return False
        if not channel.permissions_for(message.guild.me).embed_links: await channel.send("Ich benötige hier das Recht `Links einbetten`, dieses ist eine Grund Vorraussetzung für die Nutzung");return False
        command = self.commands[invoke.lower()]

        if command["botOwner"]:
            if not message.author.id == owner_id: return

        if command["botTeam"]:
            if not message.guild.id == main_guild: return
            role = etcLib.getRole(message.guild, roleID=team_role)
            if not message.author.roles.__contains__(role): return

        if command["block"]:
            if message.author.id in self.blockIDs: await channel.send(embed=discord.Embed(description="active season", color=discord.Color.red())); return False

        if len(command["permissions"]) != 0:
            selfPerm = message.channel.permissions_for(message.guild.me)
            for p in command["permissions"]:
                if not selfPerm.__getattribute__(p): await channel.send(embed=discord.Embed(description="bot require permission `" + p + "`", color=discord.Color.red())); return False

        if len(command["userPermissions"]) != 0:
            selfPerm = message.channel.permissions_for(message.author)
            for x in selfPerm:
                print(x)
            for p in command["userPermissions"]:
                if not selfPerm.__getattribute__(p): await channel.send(embed=discord.Embed(description="user require permission `" + p + "`", color=discord.Color.red())); return False
        await command["command"](message)
        return True
