import discord

from settings import *

@commands.register(
    category="moderation",
    permissions=["ban_members"]
)
async def ban(message: discord.Message):

    if not await etcLib.ifMod(message.author, message.channel): return
    if not message.mentions: await message.channel.send(embed=discord.Embed(description="no user mentioned", color=discord.Color.red())); return
    to_ban: discord.Member = message.mentions[0]
    if to_ban.id == client.user.id:
        await message.channel.send(embed=discord.Embed(description=f"i can't ban me", color=discord.Color.red()))
        return
    try:
        await to_ban.ban()
    except discord.Forbidden:
        await message.channel.send(embed=discord.Embed(description="This user is stronger then me", color=discord.Color.blurple()))
        return
    await etcLib.log(message.guild, f"User banned with a command", author=message.author, title="Ban")
    await message.channel.send(
        embed=discord.Embed(description=f"**{message.name}** successfully banned", color=discord.Color.green())
    )


@commands.register(
    category="moderation",
    permissions=["kick_members"]
)
async def kick(message: discord.Message):
    if not await etcLib.ifMod(message.author, message.channel): return
    if not message.mentions: await message.channel.send(embed=discord.Embed(description="no user mentioned", color=discord.Color.red())); return
    to_ban: discord.Member = message.mentions[0]
    if to_ban.id == client.user.id:
        await message.channel.send(embed=discord.Embed(description=f"i can't kick me", color=discord.Color.red()))
        return
    await etcLib.log(message.guild, f"User kicked with a command", author=message.author, title="Kick")
    try:
        await to_ban.kick()
    except discord.Forbidden:
        await message.channel.send(
            embed=discord.Embed(description="This user is stronger then me", color=discord.Color.blurple()))
        return
    await message.channel.send(
        embed=discord.Embed(description=f"**{message.name}** successfully kicked", color=discord.Color.green())
    )

@commands.register(
    category="guild"
)
async def rejoin(message: discord.Message):
    pass

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
            await etcLib.publicRoleRemove(message.author, invoke)
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
            await etcLib.publicRoleAdd(message.author, invoke)
        else:
            await message.author.add_roles(role)
        await message.channel.send(
            embed=discord.Embed(
                description=f"Role {role.mention} has been added",
                color=discord.Color.green()
            )
        )

@commands.register(
    category="guildsettings",
)
async def setleveling(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.guild): return
    pass

@commands.register(
    category="guildsettings",
)
async def rolemenu(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.guild): return
    args: str = message.content.split(" ")[1:]
    if not args:
        await message.channel.send(
            embed=discord.Embed(
                description=f"__Commands__\n\n"
                            f"Create a role menu `{client_prefix}rolemenu [role_mention] [role_mention]...`\n"
                            f"Create a role menu for all roles: `{client_prefix}rolemenu all`\n"
                            f"Disable all role menus: `{client_prefix}rolemenu off`",
                color=discord.Color.blue()
            ).set_footer(
                text="create a role menu for all roles will delete your old menus"
            )
        )
        return
    if not message.role_mentions:

        if args[0].lower() == "all":
            all_roles = json.loads(database.getSingle(message.guild.id, "guild", "roles"))
            if len(all_roles) == 0: await message.channel.send(embed=discord.Embed(
                description="no roles found",
                color=discord.Color.red()
            )); return
            role_dict = {str(message.channel.id): {}}
            nums = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
            sortRoles = {
                "autorole": [],
                "other": []
            }
            result = database.db.execute("SELECT * FROM programming_languages").fetchall()
            proLangs = []
            for x in result: proLangs.append(x[0])
            proLangs.sort()

            for x in all_roles:
                if proLangs.__contains__(x): sortRoles["autorole"].append([all_roles[x], x])
                else: sortRoles["other"].append([all_roles[x], x])
            if len(sortRoles["other"]) > 0:
                content = ""
                count = 0
                allcount = 0
                roles = []
                for r in sortRoles["other"]:
                    try:
                        role = message.guild.get_role(r[0])
                    except:
                        await message.channel.send(
                            embed=discord.Embed(
                                description="no exits role found, break role menu",
                                color=discord.Color.red()
                            )
                        )
                        return
                    roles.append(role.id)
                    content += f"{nums[count]} {role.mention}\n"
                    allcount += 1
                    count += 1
                    if count == 8 or allcount == len(sortRoles["other"]):
                        msg: discord.Message = await message.channel.send(
                            embed=discord.Embed(
                                title="Role menu",
                                description=content,
                                color=discord.Color.blurple()
                            )
                        )
                        for e in nums[:count]:
                            await msg.add_reaction(e)
                        content = ""
                        role_dict[str(message.channel.id)][msg.id] = roles
                        roles = []
                        count = 0
            if len(sortRoles["autorole"]) > 0:
                content = ""
                count = 0
                allcount = 0
                roles = []
                for r in sortRoles["autorole"]:
                    try:
                        role = message.guild.get_role(r[0])
                    except:
                        await message.channel.send(
                            embed=discord.Embed(
                                description="no exits role found, break role menu",
                                color=discord.Color.red()
                            )
                        )
                        return
                    roles.append(role.id)
                    content += f"{nums[count]} {role.mention}\n"
                    allcount += 1
                    count += 1
                    if count == 8 or allcount == len(sortRoles["autorole"]):
                        msg: discord.Message = await message.channel.send(
                            embed=discord.Embed(
                                title="Languages",
                                description=content,
                                color=discord.Color.blurple()
                            )
                        )
                        for e in nums[:count]:
                            await msg.add_reaction(e)
                        content = ""
                        role_dict[str(message.channel.id)][msg.id] = roles
                        roles = []
                        count = 0
            database.setSingle(message.guild.id, "guild", "rolemenu", json.dumps(role_dict))
            await message.channel.send(
                embed=discord.Embed(
                    description="creation finish",
                    color=discord.Color.green()
                ).set_footer(text="This message can be deleted")
            )
            return
        if args[0].lower() == "off":
            database.setSingle(message.guild.id, "guild", "rolemenu", "{}")
            await message.channel.send(
                embed=discord.Embed(
                    description="role menu is disabled",
                    color=discord.Color.green()
                )
            )
            return
        await message.channel.send(
            embed=discord.Embed(
                description="invalid args",
                color=discord.Color.red()
            )
        )
        return

    if len(message.role_mentions) > 8:
        await message.channel.send(
            embed=discord.Embed(
                description="only 8 roles each menu",
                color=discord.Color.red()
            )
        )
        return
    nums = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    role_dict = json.loads(database.getSingle(message.guild.id, "guild", "rolemenu"))
    if not role_dict.__contains__(str(message.channel.id)):
        role_dict[str(message.channel.id)] = {}
    content = ""
    count = 0
    roles = []
    sortRoles = {
        "other": []
    }
    for r in message.role_mentions:
        if r.position >= message.guild.me.top_role.position:
            pass
        else:
            sortRoles["other"].append(r)
    for role in sortRoles["other"]:
        roles.append(role.id)
        content += f"{nums[count]} {role.mention}\n"
        count += 1
    msg: discord.Message = await message.channel.send(
        embed=discord.Embed(
            title="Role menu",
            description=content,
            color=discord.Color.blurple()
        )
    )
    for e in nums[:count]:
        await msg.add_reaction(e)
    role_dict[str(message.channel.id)][msg.id] = roles
    database.setSingle(message.guild.id, "guild", "rolemenu", json.dumps(role_dict))
    await message.channel.send(
        embed=discord.Embed(
            description="creation finish",
            color=discord.Color.green()
        ).set_footer(text="This message can be deleted")
    )
    return

@commands.register(
    category="guildsettings",
)
async def removeRole(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.guild): return
    pass

@commands.register(
    category="guildsettings",
)
async def messagelog(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.guild): return
    await message.channel.send("*coming soon*")
    pass

@commands.register(
    category="guildsettings",
)
async def setwelcomerole(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.guild): return
    args: str = message.content.split(" ")[1:]
    if not message.role_mentions:
        if not args:
            await message.channel.send(
                embed=discord.Embed(
                    color=discord.Color.blue(),
                    description=f"__Command__\n\nSet Roles: `{client_prefix}setwelcomerole [role_mention]...`\nDisable: `{client_prefix}setwelcomerole off`\n\nPut so much role you want in the command, changes need all roles again with the changes"
                )
            )
            return
        if args[0].lower() == "off":
            database.setSingle(message.guild.id, "guild", "welcome_roles", "[]")
            await message.channel.send(
                embed=discord.Embed(
                    description="Welcome roles disabled",
                    color=discord.Color.green()
                )
            )
            return
        await message.channel.send(
            embed=discord.Embed(
                description="invalid args",
                color=discord.Color.red()
            )
        )
        return
    roles = []
    for r in message.role_mentions:
        roles.append(r.id)
    database.setSingle(message.guild.id, "guild", "welcome_roles", json.dumps(roles))
    await message.channel.send(
        embed=discord.Embed(
            description=f"Set `{len(roles)}` welcome roles",
            color=discord.Color.green()
        ).set_footer(text="Info: I can only set roles that are under my highest role")
    )

@commands.register(
    category="guildsettings",
)
async def setwelcome(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.guild): return
    args: str = message.content.split(" ")[1:]
    if not message.channel_mentions:
        if not args:
            await message.channel.send(
                embed=discord.Embed(
                    color=discord.Color.blue(),
                    description=f"__Command__\n\nSet Channel: `{client_prefix}setwelcome [channel_mention]`\nDisable: `{client_prefix}setwelcome off`"
                )
            )
            return
        if args[0].lower() == "off":
            database.setSingle(message.guild.id, "guild", "welcome_channel", None)
            await message.channel.send(
                embed=discord.Embed(
                    description="Welcome messages disabled",
                    color=discord.Color.green()
                )
            )
            return
        await message.channel.send(
            embed=discord.Embed(
                description="invalid args",
                color=discord.Color.red()
            )
        )
        return
    channel: discord.TextChannel = message.channel_mentions[0]
    if not channel.permissions_for(message.guild.me).send_messages:
        await message.channel.send(
            embed=discord.Embed(description="Invaild permissions in " + channel.mention, color=discord.Color.red())
        )
        return
    database.setSingle(message.guild.id, "guild", "welcome_channel", channel.id)
    await message.channel.send(
        embed=discord.Embed(
            description="Welcome channel set at " + channel.mention,
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
    if not await etcLib.ifMod(message.author, message.channel): return
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
async def setmodrole(message: discord.Message):
    if not message.role_mentions:
        await message.channel.send(
            embed=discord.Embed(
                description=f"Command: `{client_prefix}setmodrole [role_mention]`"
            )
        )
        return
    if not await etcLib.ifAdmin(message.author, message.channel): return
    role = message.role_mentions[0]
    database.setSingle(message.guild.id, "guild", "modRoleId", role.id)
    await message.channel.send(
        embed=discord.Embed(
            description=f"{role.mention} is now moderator, users with the role can now use mod commands in the bot"
        )
    )

@commands.register(
    category="guildsettings"
)
async def setguilddesc(message: discord.Message):
    if not await etcLib.ifAdmin(message.author, message.channel): return
    args: str = message.content.split(" ")[1:]
    if not args:
        database.setSingle(message.guild.id, "guild", "description", "unknown")
        await message.channel.send(
            embed=discord.Embed(
                description="Guild description removed",
                color=discord.Color.green()
            )
        )
        return

    database.setSingle(message.guild.id, "guild", "description", message.content.split(" ", 1)[1])
    await message.channel.send(
        embed=discord.Embed(
            description=f"Guild description set to\n\n{message.content.split(' ', 1)[1]}",
            color=discord.Color.green()
        )
    )

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
    if not await etcLib.ifAdmin(message.author, message.channel): return

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
    guild_description: str = database.getSingle(guild.id, "guild", "description")
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
        value=f"`{str(len(guild.roles))}` Roles"
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
        value=f"Level `{database.getSingle(guild.id, 'guild', 'serverlog')}`"

    )
    embed.add_field(
        name=":coin: Own coin",
        value="*coming soon*"
    )
    embed.add_field(
        name=":thunder_cloud_rain: Raid protection",
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
