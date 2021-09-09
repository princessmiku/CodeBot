import discord.shard

from settings import *


def startup():
    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot or message.author.id == client.user.id: return
        api.userInsert(message.author.id)
        # await leveling.level_xp_add(message.author, message.channel)
        # await achiSys.Achievements(message.author.id, message).progressAchievement("chat", "active")
        await commands.call(message)

    @client.event
    async def on_message_delete(message: discord.Message):
        guild: discord.Guild = message.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if loglevel >= 4:
                content = message.content
                if len(content) > 600:
                    content = message.content[0:600] + "..."
                await etcLib.log(guild, f"__Channel:__ {message.channel.mention}\n\n```diff\n- {content}```",
                                 title=f"Message from {message.author.name} was deleted", author="Delete event")
            else:
                await etcLib.log(guild, f"__Channel:__ {message.channel.mention}\n\n*content hidden*",
                                 title=f"Message from {message.author.name} was deleted in", author="Delete event")

    @client.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        guild: discord.Guild = before.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if before.content == "" and after.content == "":
                return
            if loglevel >= 4:
                old_content = before.content
                if len(old_content) > 600:
                    old_content = before.content[0:600] + "..."
                after_content = after.content
                if len(after_content) > 600:
                    after_content = after.content[0:600] + "..."

                await etcLib.log(guild,
                                 f"__Channel:__ {before.channel.mention}\n\n__Old message__\n```diff\n- {old_content}```\n\n__New message__\n```diff\n+ {after_content}```",
                                 title=f"Message from {before.author.name} was edited", author="Edit event")
            else:
                await etcLib.log(guild, f"__Channel:__ {before.channel.mention}\n\n*content hidden*",
                                 title=f"Message from {before.author.name} was edited", author="Edit event")

    @client.event
    async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
        emojis = payload.emoji.name
        if emojis in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]:
            nums = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2, "4️⃣": 3, "5️⃣": 4, "6️⃣": 5, "7️⃣": 6, "8️⃣": 7}
            count = nums[emojis]
            message_id = payload.message_id
            user_id = payload.user_id
            channel_id = payload.channel_id
            guild_id = payload.guild_id
            guild: discord.Guild = client.get_guild(guild_id)
            channel: discord.TextChannel = guild.get_channel(channel_id)
            message: discord.Message = await channel.fetch_message(message_id)
            user: discord.Member = await guild.fetch_member(user_id)
            if user.bot: return
            rolemenu = json.loads(database.getSingle(guild_id, "guild", "rolemenu"))
            if not rolemenu.__contains__(str(channel_id)): return
            if not rolemenu[str(channel_id)].__contains__(str(message_id)): return
            await message.remove_reaction(payload.emoji, user)
            roleID = rolemenu[str(channel_id)][str(message_id)][count]
            try:
                role = guild.get_role(roleID)
            except:
                loglevel = database.getSingle(guild_id, "guild", "serverlog")
                if loglevel > 0:
                    await etcLib.log(guild, f"error in rolemenu, role id `{roleID}`", title="Error in role menu", author="rolemenu")
                return
            result = database.db.execute("SELECT * FROM programming_languages").fetchall()
            liste = []
            for x in result: liste.append(x[0])
            roles = json.loads(database.getSingle(guild.id, "guild", "roles"))
            for x in roles:
                if roles[x] == roleID:
                    if liste.__contains__(x):
                        if user.roles.__contains__(role):
                            await etcLib.publicRoleRemove(user, x)
                        else:
                            await etcLib.publicRoleAdd(user, x)
                        return

            if user.roles.__contains__(role):
                await user.remove_roles(role)
            else:
                await user.add_roles(role)

    @client.event
    async def on_raw_reaction_remove(payload):
        pass

    @client.event
    async def on_raw_reaction_clear(payload):
        pass

    @client.event
    async def on_guild_channel_create(channel: discord.TextChannel):
        guild: discord.Guild = channel.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            await etcLib.log(guild, f"__Channel:__ {channel.mention}", title=f"Channel {channel.name} created",
                             author="Channel create event")

    @client.event
    async def on_guild_channel_delete(channel: discord.TextChannel):
        guild: discord.Guild = channel.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            await etcLib.log(guild, title=f"Channel {channel.name} was deleted", author="Channel delete event")

    @client.event
    async def on_guild_channel_update(before: discord.TextChannel, after: discord.TextChannel):
        guild: discord.Guild = before.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            updates = ""
            only_positon = False
            if before.name != after.name:
                updates += f"- Name changed from `{before.name}` to `{after.name}`\n"
            if before.position != after.position:
                updates += f"- Position changed from `{before.position}` to `{after.position}`\n"
                if before.position + 1 == after.position:
                    only_positon = True
                elif before.position - 1 == after.position:
                    only_positon = True
            if before.type == discord.ChannelType.text:
                if before.category != after.category:
                    updates += f"- Category changed from `{before.category.name}` to `{after.category.name}`\n"
                if before.is_nsfw() != after.is_nsfw():
                    updates += f"- NSFW settings changed from `{before.is_nsfw()}` to `{after.is_nsfw()}`\n"
                if before.is_news() != after.is_news():
                    updates += f"- News settings changed from `{before.is_news()}` to `{after.is_news()}`\n"
                if before.members != after.members:
                    updates += f"- Probably permissions changed\n"
                if before.slowmode_delay != after.slowmode_delay:
                    updates += f"- Slowmode changed from `{before.slowmode_delay}` to `{after.slowmode_delay}`\n"
                if before.topic != after.topic:
                    updates += f"- Topic/Description was changed\n"
            if before.type != after.type:
                updates += f"- Channel typ changed from `{before.type}` to `{after.type}`\n"
            if updates == "":
                updates += "something not logged was changed"
            if only_positon:
                return

            await etcLib.log(guild, f"__Channel:__ {after.mention}\n\n{updates}", title="Channel was edited",
                             author="Channel update event")

    @client.event
    async def on_guild_channel_pins_update(channel, last_pin):
        guild: discord.Guild = channel.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            await etcLib.log(guild, f"in channel {channel.mention}", title="Pin update",
                             author="Channel pins update event")

    @client.event
    async def on_guild_integrations_update(guild):
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            await etcLib.log(guild, "update guild integrations", title="Guild updated",
                             author="integrations update event")

    @client.event
    async def on_member_join(member: discord.Member):
        guild: discord.Guild = member.guild

        async def logging():
            loglevel = database.getSingle(guild.id, "guild", "serverlog")
            if loglevel >= 2:
                await etcLib.log(guild, f"{member.mention} joined", title="New user", author="Member join event")

        await logging()

        if member.bot: return
        api.userInsert(member.id)
        welcome_channel = database.getSingle(guild.id, "guild", "welcome_channel")
        if welcome_channel is not None:
            await guild.get_channel(welcome_channel).send(
                f":inbox_tray: Welcome {member.name}, you'r the `{guild.member_count}` Member"
            )
        roleIds = json.loads(database.getSingle(guild.id, "guild", "welcome_roles"))
        if len(roleIds) > 0:
            roles = []
            for rID in roleIds: roles.append(guild.get_role(rID))
            if len(roles) > 0: await member.add_roles(*roles, reason="Welcome roles")
        userLangs = json.loads(database.getSingle(member.id, "user", "langs"))
        if len(userLangs) > 0:
            roles = []
            server_roles = json.loads(database.getSingle(guild.id, "guild", "roles"))
            for x in userLangs:
                if server_roles.__contains__(x):
                    for rID in roleIds: roles.append(guild.get_role(rID))
            if len(roles) > 0: await member.add_roles(*roles, reason="Languages roles")

    @client.event
    async def on_member_remove(member: discord.Member):
        guild: discord.Guild = member.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            await etcLib.log(guild, f"{member.mention} leave the guild, reason: kick, ban or by her self",
                             title="Lost user", author="Member remove event")
        if member.bot: return
        welcome_channel = database.getSingle(guild.id, "guild", "welcome_channel")
        if welcome_channel is not None:
            await guild.get_channel(welcome_channel).send(
                f":outbox_tray: Good bye {member.name}"
            )

    @client.event
    async def on_member_update(before: discord.Member, after: discord.Member):
        guild: discord.Guild = after.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            updates = ""
            if before.color != after.color:
                updates += f"- Color changed from `{before.color}` to `{after.color}`\n"
            if before.display_name != after.display_name:
                updates += f"- Display name changed from `{before.display_name}` to `{after.display_name}`\n"
            if before.top_role != after.top_role:
                updates += f"- top role changed from `{before.top_role.name}` to `{after.top_role.name}`\n"
            if len(before.roles) != len(after.roles):
                updates += f"- Role count changed from `{len(before.roles)}` to `{len(after.roles)}`\n"
            if before.guild_permissions != after.guild_permissions:
                updates += f"- New guild permissions"
            if updates != "":
                await etcLib.log(guild, f"__Member:__ {after.mention}\n\n{updates}", title="Member was updated",
                                 author="Member update event")

    @client.event
    async def on_user_update(before: discord.User, after: discord.User):
        pass

    @client.event
    async def on_guild_join(guild: discord.Guild):
        database.db.execute(
            f"INSERT OR IGNORE INTO  guild(id, name, create_at) VALUES ({str(guild.id)}, '{guild.name}', '{datetime.datetime.today().strftime('%H:%M:%S on %B %d, %Y')}')")

    @client.event
    async def on_guild_remove(guild: discord.Guild):
        pass

    @client.event
    async def on_guild_update(before: discord.Guild, after: discord.Guild):
        guild: discord.Guild = after
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            updates = ""
            if before.name != after.name:
                updates += f"- Name changed from `{before.name}` to `{after.name}`\n"
            if before.description != after.description:
                updates += f"- Description changed from `{before.description}` to `{after.description}`\n"
            if before.icon != after.icon:
                updates += f"- Guild icon was updated\n"
            if before.afk_timeout != after.afk_timeout:
                updates += f"- Afk timeout changed from `{before.afk_timeout}`s to `{after.afk_timeout}`s\n"
            if before.afk_channel != after.afk_channel:
                updates += f"- Afk channel changed from `{before.afk_channel.mention}` to `{after.afk_channel.mention}`\n"
            if before.banner_url != after.banner_url:
                updates += f"- Banner was updated"
            if before.rules_channel != after.rules_channel:
                updates += f"- Rules channel changed from `{before.rules_channel.mention}` to `{after.rules_channel.mention}`\n"
            # if before != after:
            #    updates += f"- x changed from `{before}` to `{after}`\n"
            # if before != after:
            #    updates += f"- x changed from `{before}` to `{after}`\n"

    @client.event
    async def on_guild_role_create(role: discord.Role):
        guild: discord.Guild = role.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            await etcLib.log(guild, f"Role: {role.mention}", title="Role created", author="Role create event")

    @client.event
    async def on_guild_role_delete(role: discord.Role):
        guild: discord.Guild = role.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            await etcLib.log(guild, f"Role: {role.name}", title="Role created", author="Role delete event")

    @client.event
    async def on_guild_role_update(before: discord.Role, after: discord.Role):
        guild: discord.Guild = after.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 3:
            updates = ""
            if before.name != after.name:
                updates += f"- Name changed from `{before.name}` to `{after.name}`\n"
            if before.color != after.color:
                updates += f"- Color changed from `{before.color}` to `{after.color}`\n"
            if before.position != after.position:
                updates += f"- Role position changed from `{before.position}` to `{after.position}`\n"
                return
            if before.permissions != after.permissions:
                updates += f"- Permissions updated\n"
            if updates == "":
                updates += "something not logged was changed"
            await etcLib.log(guild, f"__Role:__ {after.mention}\n\n{updates}", title="Role was updated", author="Role update event")

    @client.event
    async def on_guild_emojis_update(guild: discord.Guild, before: discord.Emoji, after: discord.Emoji):
        return
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if loglevel >= 4:
                await etcLib.log()
            else:
                await etcLib.log()

    @client.event
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        return
        guild: discord.Guild = member.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if loglevel >= 4:
                await etcLib.log()
            else:
                await etcLib.log()

    @client.event
    async def on_member_ban(guild: discord.Guild, user: discord.User):
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            await etcLib.log(guild, f"__User:__ {user.mention}", title="User banned", author="Member ban event")

    @client.event
    async def on_member_unban(guild: discord.Guild, user: discord.User):
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if loglevel >= 2:
                await etcLib.log(guild, f"__User:__ {user.mention}", title="User unbanned", author="Member unban event")

    @client.event
    async def on_invite_create(invite: discord.Invite):
        return
        guild: discord.Guild = invite.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if loglevel >= 4:
                await etcLib.log()
            else:
                await etcLib.log()

    @client.event
    async def on_invite_delete(invite: discord.Invite):
        return
        guild: discord.Guild = invite.guild
        loglevel = database.getSingle(guild.id, "guild", "serverlog")
        if loglevel >= 2:
            if loglevel >= 4:
                await etcLib.log()
            else:
                await etcLib.log()

    # @client.event
    # async def on_():
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
    await client.change_presence(activity=discord.Game(name=f"{client_prefix}help | Eat errors"))
    guilds = client.guilds
    for g in guilds:
        database.db.execute(
            f"INSERT OR IGNORE INTO  guild(id, name, create_at) VALUES ({str(g.id)}, '{g.name}', '{datetime.datetime.today().strftime('%H:%M:%S on %B %d, %Y')}')")

        async for member in g.fetch_members(limit=None):
            api.userInsert(member.id)
    startup()
    print("initialize finish, bot now active")


client.loop.create_task(initialize())
client.run(tokens.bot_token)
