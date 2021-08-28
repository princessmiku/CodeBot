from settings import *

@commands.register(
    category="guildsettings"
)
async def registerRole(message: discord.Message):
    pass

@commands.register(
    category="guildsettings"
)
async def setserverlog(message: discord.Message):
    pass

@commands.register(
    category="information"
)
async def serverinfo(message: discord.Message):
    if message.mentions:
        return
    guild: discord.Guild = message.guild
    guild_description: str = guild.description
    if guild_description is None: guild_description = "*keine Vorhanden*"
    color = discord.Color.blue()
    if len(guild.roles) > 1: color = guild.roles[-1].color
    #guild_invite = database.getSingle(guild.id, "guild", "invite")
    guild_invite = "*coming soon*"
    if guild_invite is None: guild_invite = "*keine eingestellt*"
    embed = discord.Embed(
        title=f":compass: Server {guild.name}",
        description=guild_description,
        color=color
    ).set_thumbnail(url=guild.icon_url)
    embed.add_field(
        name=":detective:: Member",
        value=f"`{str(guild.member_count)}` User"
    )
    embed.add_field(
        name=":star2: Owner",
        value=guild.owner
    )
    embed.add_field(
        name=":medal: Roles",
        value=f"{str(len(guild.roles))} Roles"
    )
    embed.add_field(
        name=":keyboard: Afk Timeout",
        value=f"`{str(guild.afk_timeout / 60)}` minutes"
    )
    embed.add_field(
        name=":love_letter: Invite Link",
        value=guild_invite
    )

    embed.add_field(
        name=":pencil: Serverlog",
        value="*coming soon*" #database.getSingle(guild.id, "guild", "serverlog")

    )
    embed.add_field(
        name=":coin: Own coin",
        value="*coming soon*"
    )
    chats = {} # database.getSingle(guild.id, "guild", "global_chat")
    if len(chats) == 0:
        chats = "no / coming soon"
    else:
        chats = "yes / coming soon"
    embed.add_field(
        name=":globe_with_meridians: Use global Chats?",
        value=chats
    )
    embed.add_field(
        name=":hourglass_flowing_sand: Times",
        value=f"Server create: `{guild.created_at.strftime('%H:%M:%S on %B %d, %Y')}`\n"
              f"Bot join: `{guild.me.joined_at.strftime('%H:%M:%S on %B %d, %Y')}`",
        inline=False
    )
    await message.channel.send(
        embed=embed
    )
