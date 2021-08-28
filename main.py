import discord.shard

from settings import *


def startup():

    @client.event
    async def on_ready():
        print("online")
        await client.change_presence(activity=discord.Game(name=f"{client_prefix}help | Eat errors"))

    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot or message.author.id == client.user.id: return
        api.userInsert(message.author.id)
        #await leveling.level_xp_add(message.author, message.channel)
        #await achiSys.Achievements(message.author.id, message).progressAchievement("chat", "active")
        await commands.call(message)

    @client.event
    async def on_message_delete(message: discord.Message):
        pass

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        pass

    @client.event
    async def on_raw_reaction_add(payload):
        pass

    @client.event
    async def on_raw_reaction_remove(payload):
        pass

    @client.event
    async def on_raw_reaction_clear(payload):
        pass

    @client.event
    async def on_guild_channel_create(channel):
        pass

    @client.event
    async def on_guild_channel_delete(channel):
        pass

    @client.event
    async def on_guild_channel_update(before, after):
        pass

    @client.event
    async def on_guild_channel_pins_update(channel, last_pin):
        pass

    @client.event
    async def on_guild_integrations_update(guild):
        pass

    @client.event
    async def on_member_join(member: discord.Member):
        pass

    @client.event
    async def on_member_remove(member: discord.Member):
        pass

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        pass

    @client.event
    async def on_user_update(before: discord.User, after: discord.User):
        pass

    @client.event
    async def on_guild_join(guild: discord.Guild):
        pass

    @client.event
    async def on_guild_remove(guild: discord.Guild):
        pass

    @client.event
    async def on_guild_update(before: discord.Guild, after: discord.Guild):
        pass

    @client.event
    async def on_guild_role_create(role: discord.Role):
        pass

    @client.event
    async def on_guild_role_delete(role: discord.Role):
        pass

    @client.event
    async def on_guild_role_update(before: discord.Role, after: discord.Role):
        pass

    @client.event
    async def on_guild_emojis_update(guild: discord.Guild, before: discord.Emoji, after: discord.Emoji):
        pass

    @client.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        pass

    @client.event
    async def on_member_ban(guild: discord.Guild, user: discord.User):
        pass

    @client.event
    async def on_member_unban(guild: discord.Guild, user: discord.User):
        pass

    @client.event
    async def on_invite_create(invite: discord.Invite):
        pass

    @client.event
    async def on_invite_delete(invite: discord.Invite):
        pass

    #@client.event
    #async def on_():
    #    pass


def createHelpEmbed():  # hier erstellt der Bot die Help anhand der eingetragenden Befhele
    embed = discord.Embed(
        color=discord.Color.teal(),
        title=":pencil: Help"
    )
    for cat in commands.helpList:
        if cat != "empty":
            embed.add_field(
                name=cat,
                value="`" + "`, `".join(commands.helpList[cat]) + "`",
                inline=False
            )
        else:
            if len(commands.helpList[cat]): embed.description = "`" + "`, `".join(commands.helpList[cat]) + "`"
    commands.helpEmbed = embed



createHelpEmbed()  # wichtig zum funktionieren der Help List


async def initialize():
    print("start initialize")
    await client.wait_until_ready()

    guilds = client.guilds
    for g in guilds:
        database.db.execute(
            f"INSERT OR IGNORE INTO  guild(id, name, create_at) VALUES ({str(g.id)}, '{g.name}', '{datetime.datetime.today().strftime('%H:%M:%S on %B %d, %Y')}')")

    startup()
    print("initialize finish, bot now active")

client.loop.create_task(initialize())
client.run(tokens.bot_token)