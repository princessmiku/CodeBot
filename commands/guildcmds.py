import discord

from settings import *


@commands.register(
    category="guild"
)
async def roles(message: discord.Message):
    roles = json.loads(database.getSingle(message.guild.id, "guild", "roles"))
    args: str = message.content.split(" ")[1:]
    if not args:
        pages = pageEmbed.PageEmbed(client, message.channel, message.author)
        pages.addPageList(list(roles.keys()), 15)
        await pages.run()
        return
    invoke = message.content.split(" ", 1)[1].lower()
    if not roles.__contains__(invoke):
        await message.channel.send(
            embed=discord.Embed(
                description=f"Self role `{invoke}` not exists",
                color=discord.Color.red()
            )
        )
        return
    role = message.guild.get_role(roles[invoke])
    if not role:
        await message.channel.send(
            embed=discord.Embed(
                description="Role not exist on this server",
                color=discord.Color.red()
            )
        )
        return
    roleIsLang = False
    result = database.db.execute(f"SELECT * FROM programming_languages WHERE name='{invoke}'").fetchone()
    if result is not None:
        roleIsLang = True
    if message.author.roles.__contains__(role):
        if roleIsLang:
            await publicRoles.remove(message.author, invoke, database)
        else:
            await message.author.remove_roles(role)
        await message.channel.send(
            embed=discord.Embed(
                description=f"Role {role.mention} has been removed",
                color=discord.Color.green()
            )
        )
    else:

        if roleIsLang:
            await publicRoles.add(message.author, invoke, database)
        else:
            await message.author.add_roles(role)
        await message.channel.send(
            embed=discord.Embed(
                description=f"Role {role.mention} has been added",
                color=discord.Color.green()
            )
        )

@commands.register(
    category="guildsettings"
)
async def registerRole(message: discord.Message):
    args: list = message.content.split(" ")[1:]
    if not args:
        await message.channel.send(
            embed=discord.Embed(
                color=discord.Color.blue(),
                description="register a role for yourself or assign it to the automatic one. Welcome role is not "
                            f"given here.\n\nProgramming language roles count as auto roles. if an auto role is set, "
                            f"all members automatically get this which meets the requirements.\nYou can find all "
                            f"under `{client_prefix}lang`\n\n"
                            f"All roles listet under `{client_prefix}roles`"
            ).add_field(
                name="Command",
                value=f"`{client_prefix}registerrole [role] [invoke]`\nRole: Role mention\nInvoke: Invoke / programming "
                      f"language name (for autorole)"
            )
        )
        return
    if not message.role_mentions or len(args) < 2:
        await message.channel.send(
            embed=discord.Embed(
                description="you forgot something",
                color=discord.Color.red()
            )
        )
        return
    role: discord.Role = message.role_mentions[0]
    if role.position >= message.guild.me.top_role.position:
        await message.channel.send(
            embed=discord.Embed(
                description="The role is higher than or equal to my highest role",
                color=discord.Color.red()
            )
        )
        return
    give_roles = json.loads(database.getSingle(message.guild.id, "guild", "roles"))
    registerName = message.content.split(' ', 2)[2].lower()
    result = database.db.execute(f"SELECT * FROM programming_languages WHERE name='{registerName}'").fetchone()
    autorole = False
    if result is not None:
        autorole = True
    give_roles[registerName] = role.id
    database.setSingle(message.guild.id, "guild", "roles", json.dumps(give_roles))
    await message.channel.send(
        embed=discord.Embed(
            description="Role set",
            color=discord.Color.blue()
        ).add_field(
            name="Invoke",
            value=registerName
        ).add_field(
            name="Role",
            value=role.mention
        ).add_field(
            name="Autorole",
            value=str(autorole)
        )
    )
    if autorole:
        members = message.guild.members
        for m in members:
            try:
                result = database.getSingle(m.id, "user", "langs")
            except TypeError:
                result = None
            if result:
                result = json.loads(result)
                if registerName in result:
                    await m.add_roles(role)


@commands.register(
    category="guildsettings"
)
async def serverlog(message: discord.Message):
    args: list = message.content.split(" ")[1:]
    if not args:
        await message.channel.send(
            embed=discord.Embed(
                title="Set your serverlog",
                color=discord.Color.blurple(),
                description=f"command: `{client_prefix}serverlog [level] [channel]`\n\n"
                            f"Level: available `0/1/2/3/4`\nChannel: Mention your channel\n\n"
                            f"**Current log level `{database.getSingle(message.guild.id, 'guild', 'serverlog')}`**"
            ).add_field(
                name=":new_moon: Level 0",
                value="**Bot log nothing**",
                inline=False
            ).add_field(
                name=":waning_crescent_moon: Level 1",
                value="**Minimal log**\n- Bot log guild specific things"
            ).add_field(
                name=":last_quarter_moon: Level 2",
                value="**Bot will log base Server changes**\n"
                      "- Member Join/Leave/Bans/Kicks\n"
                      "- Message edits/delete without content\n\n"
                      "- Bot log guild specific things"
            ).add_field(
                name=":waning_gibbous_moon: Level 3",
                value="**Bot will log very much Server changes**\n"
                      "- Member join/leave/bans/kicks/updates\n"
                      "- Message editing/deletion/pins/unpin without content\n"
                      "- Server Updates rename/settings/invites\n"
                      "- Channel creation/editing/deletion\n"
                      "- Voice State join/leave/mute/deaf/etc\n"
                      "- Roles creation/editing/deletion\n\n"
                      "- Bot log guild specific things"
            ).add_field(
                name=":full_moon: Level 4",
                value="**Log everything from 3 but with content**"
            )
        )
        return
    if not message.author.guild_permissions.administrator:
        await message.channel.send(embed=discord.Embed(
            description="missing permissions `administrator`",
            color=discord.Color.red()
        ))
        return

    logLevel: str = args[0]
    if logLevel not in ["0", "1", "2", "3", "4"]:
        await message.channel.send(
            embed=discord.Embed(
                description="invalid server log level",
                color=discord.Color.red()
            )
        )
        return
    if logLevel == "0":
        database.setSingle(message.guild.id, "guild", "serverlog", int(logLevel))
        database.setSingle(message.guild.id, "guild", "serverlogChannel", None)
        await message.channel.send(
            embed=discord.Embed(
                description="serverlog has been deactivated",
                color=discord.Color.green()
            )
        )
        return
    if not message.channel_mentions and logLevel != "0":
        await message.channel.send(
            embed=discord.Embed(
                description="You forgot the mention",
                color=discord.Color.red()
            )
        )
        return
    logChannel: discord.TextChannel = message.channel_mentions[0]
    if not logChannel.permissions_for(message.guild.me).read_messages:
        await message.channel.send(
            embed=discord.Embed(
                description="i can't read the channel",
                color=discord.Color.red()
            )
        )
        return
    if not logChannel.permissions_for(message.guild.me).send_messages:
        await message.channel.send(
            embed=discord.Embed(
                description="i can't send messages to the channel",
                color=discord.Color.red()
            )
        )
        return
    database.setSingle(message.guild.id, "guild", "serverlog", int(logLevel))
    database.setSingle(message.guild.id, "guild", "serverlogChannel", message.channel_mentions[0].id)
    embed = discord.Embed(
        description=f"log was activated on level `{logLevel}` in channel {message.channel_mentions[0].mention}",
        color=discord.Color.green()
    )

    gifs = {
        "1": "https://c.tenor.com/Rokyha7TPDUAAAAC/such-search.gif",
        "2": "https://c.tenor.com/TbgvutY7_5AAAAAC/patrick-pants.gif",
        "3": "https://c.tenor.com/5TRRWtGp9-kAAAAd/pirates-des-cara%C3%AFbes3-pirates-of-the-caribbean3.gif",
        "4": "https://c.tenor.com/DZr_z9eCVQoAAAAC/telescope-staring.gif"
    }
    embed.set_image(url=gifs[logLevel])
    await message.channel.send(embed=embed)

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
