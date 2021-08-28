from settings import *

@commands.register(
    category="information"
)
async def profile(message: discord.Message):
    if message.mentions:
        user: discord.Member = message.mentions[0]
    else:
        user: discord.Member = message.author
    # embed start
    embed = discord.Embed(
        title=f"Profil von {user.name}",
        description=api.userGet(user.id, "description"),
        color=user.top_role.color
    ).set_thumbnail(url=user.avatar_url)
    #req = await client.http.request(discord.http.Route("GET", "/users/{uid}/", uid=user.id))
    #print(req)
    #banner_id = req["banner"]
    ## If statement because the user may not have a banner
    #if banner_id:
    #    banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.gif?size=512"
    #    embed.set_image(url=banner_url)
    embed.add_field(
        name=":pencil: Names",
        value=f"Name: {user.name}\nNickname: {user.display_name}"
    )
    embed.add_field(
        name=":moneybag: Money",
        value=f"`{api.userGet(user.id, 'money')}€`"
    )
    embed.add_field(
        name="Roles",
        value=str(len(user.roles))
    )
    # setup languages
    langList: list = json.loads(api.userGet(user.id, "langs"))
    if len(langList) > 5:
        langStr = str(len(langList)) + " Sprachen"
        embed.set_footer(text="Alle sprachen kannst du mit !lang oder eines anderen Users mit !lang [mention] anschauen")
    elif len(langList) == 8:
        langStr = "*Keine ausgweählt*"
        if not message.mentions or user == message.author:
            embed.set_footer(text="mit !lang kann man sich Sprachen zuweisen")
    else:
        langStr = "`" + "`, `".join(langList) + "`"
    embed.add_field(
        name=":globe_with_meridians: Languages",
        value=langStr
    )

    embed.add_field(
        name=":hourglass_flowing_sand: Times",
        value=f"Server join: `{user.joined_at.strftime('%H:%M:%S on %B %d, %Y')}`\n"
              f"Account create: `{user.created_at.strftime('%H:%M:%S on %B %d, %Y')}`\n"
              f"Bot join: `{api.userGet(user.id, 'create_at')}`",
        inline=False
    )
    await message.channel.send(embed=embed)


@commands.register(
    category='information',
    hidden=True
)
async def help(message: discord.Message):
    args: list = message.content.split(" ")[1:]
    if not args:
        await message.channel.send(
            embed=commands.helpEmbed
        )
        return
    if not commands.helpPages.__contains__(args[0].lower()):
        await message.channel.send(
            embed=discord.Embed(
                description="keine seite vorhanden",
                color=discord.Color.red()
            )
        )
        return
    toSend = commands.helpPages[args[0].lower()]
    if isinstance(toSend, discord.Embed):
        await message.channel.send(
            embed=toSend.set_author(name=args[0].lower())
        )
    else:
        await message.channel.send(
            embed=discord.Embed(
                description=toSend,
                color=discord.Color.greyple()
            ).set_author(name=args[0].lower())
        )
