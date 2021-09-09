import discord, json, datetime
from . import database as libDB

database: libDB.Connect = None


async def ifMod(member: discord.Member, channel: discord.TextChannel = False):
    if member.guild_permissions.administrator:
        return True
    modrole = database.getSingle(member.guild.id, "guild", "modRoleId")
    if modrole == 0:
        if channel:
            await channel.send(
                embed=discord.Embed(description="server have no mod role, run with administrator permissions",
                                    color=discord.Color.red()))
        return False
    role_ids = list(map(int, [r.id for r in member.roles]))
    if role_ids.__contains__(modrole):
        return True
    if channel:
        await channel.send(
            embed=discord.Embed(description="you need the mod role or admin to run this command part", color=discord.Color.red()))
    return False


async def ifAdmin(member: discord.Member, channel: discord.TextChannel = False):
    if member.guild_permissions.administrator:
        return True
    if channel:
        await channel.send(
            embed=discord.Embed(description="you need admin to run this command part", color=discord.Color.red()))
    return False


async def log(guild: discord.Guild, text: str = "*no content*", title: str = "Serverlog", color = discord.Color.blue(), author: str = "unknown"):
    channel: int = database.getSingle(guild.id, "guild", "serverlogChannel")
    if channel is None:
        return
    try:
        channel: discord.TextChannel = guild.get_channel(channel)
        await channel.send(
            embed=discord.Embed(
                title=title,
                description=text,
                color=color
            ).set_author(
                name="Author: " + author
            ).set_footer(
                text=datetime.datetime.today().strftime('%H:%M:%S on %B %d, %Y')
            )
        )
    except:
        pass

async def publicRoleAdd(member: discord.Member, name: str):
    guilds = member.mutual_guilds
    userdata: list = json.loads(database.getSingle(member.id, "user", "langs"))
    if not userdata.__contains__(name):
        userdata.append(name)
        userdata.sort()
        database.setSingle(member.id, "user", "langs", json.dumps(userdata))
    for g in guilds:
        try:
            give_roles = json.loads(database.getSingle(g.id, "guild", "roles"))
            if name in give_roles:
                member = await g.fetch_member(member.id)
                role = g.get_role(give_roles[name])
                await member.add_roles(role)
        except:
            pass


async def publicRoleRemove(member: discord.Member, name: str):
    guilds = member.mutual_guilds
    userdata: list = json.loads(database.getSingle(member.id, "user", "langs"))
    if userdata.__contains__(name):
        userdata.remove(name)
        userdata.sort()
        database.setSingle(member.id, "user", "langs", json.dumps(userdata))
    for g in guilds:
        try:
            give_roles = json.loads(database.getSingle(g.id, "guild", "roles"))
            if name in give_roles:
                member = await g.fetch_member(member.id)
                role = g.get_role(give_roles[name])
                await member.remove_roles(role)
        except:
            pass


def getRole(guild: discord.Guild, message: discord.Message = None, roleID=None, rolestr=None):
    try:
        if roleID != None:
            role: discord.Role = guild.get_role(roleID)
            return role
        if message != None:
            if message.role_mentions:
                return message.role_mentions[0]
            else:
                r: str = message.content.split(" ", 1)[1]
                if r.isnumeric():
                    role = guild.get_role(r)
                    return role

                for x in guild.roles:
                    if x.name.lower() == r.lower():
                        return x
        if rolestr != None:
            if rolestr.isnumeric():
                role = guild.get_role(rolestr)
                return role

            for x in guild.roles:
                if x.name.lower() == rolestr.lower():
                    return x

        return None
    except:
        return None