from settings import *


@commands.register(
    category="programming",
)
async def lang(message: discord.Message):
    args: list = message.content.split(" ")[1:]
    if message.mentions:
        user = message.mentions[0]
        try:
            langList: list = json.loads(api.userGet(user.id, "langs"))
        except TypeError:
            await message.channel.send(
                embed=discord.Embed(description="User have no data", color=discord.Color.red()))
            return
        langStr = "• `" + "`\n• `".join(langList) + "`"
        await message.channel.send(embed=discord.Embed(
            description=langStr,
            color=discord.Color.teal(),
            title=f"Languages from {user.name}"
        ))
        return
    if not args:
        result = database.db.execute("SELECT * FROM programming_languages").fetchall()
        liste = []
        for x in result: liste.append(x[0])
        liste = sorted(liste)
        possible = []
        listStr = ""
        langList: list = json.loads(api.userGet(message.author.id, "langs"))
        for x in liste:
            if not langList.__contains__(x): possible.append(x)
        embed = discord.Embed(
            description="Here you can choose which languages you can, these will then be displayed in your profile",
            color=discord.Color.teal(),
            title="Programming languages"
        )
        if len(possible) != 0:
            embed.add_field(
                name="Available",
                value="• `" + "`\n• `".join(possible) + "`"
            )
        if len(langList) != 0:
            embed.add_field(
                name="Selected",
                value="• `" + "`\n• `".join(langList) + "`"
            )
        embed.add_field(
            name="Commands",
            value=f"Add: `{client_prefix}lang [lang]`\nDelete: `{client_prefix}lang [lang]`\nInfo: `{client_prefix}info [lang]`",
            inline=False
        )
        await message.channel.send(embed=embed)
        return
    result = database.db.execute(f"SELECT * FROM programming_languages WHERE name = '{message.content.split(' ', 1)[1].lower()}'").fetchone()
    if result is None: await message.channel.send(embed=discord.Embed(description="Language not found", color=discord.Color.red())); return
    userdata: list = json.loads(api.userGet(message.author.id, "langs"))
    if userdata.__contains__(result[0]):
        await publicRoles.remove(message.author, result[0], database)
        await message.channel.send(
            embed=discord.Embed(
                description=f"The language `{result[0].capitalize()}` has been removed from your profile"
            )
        )
        return
    await publicRoles.add(message.author, result[0], database)
    await message.channel.send(
        embed=discord.Embed(
            description=f"The language `{result[0].capitalize()}` has been added to your profile"
        )
    )


@commands.register(
    category="programming",
)
async def info(message: discord.Message):
    args: list = message.content.split(" ")[1:]
    if not args: await lang(message); return
    result = database.db.execute(f"SELECT * FROM programming_languages WHERE name = '{message.content.split(' ', 1)[1].lower()}'").fetchone()
    if result is None: await message.channel.send(embed=discord.Embed(description="Language not found", color=discord.Color.red())); return
    embed = discord.Embed(
            title=result[0].capitalize(),
            color=discord.Color.teal()
        ).add_field(
            name=":link: Link",
            value=result[2],
            inline=False
        ).add_field(
            name=":clapper: Tutorial",
            value=result[3],
            inline=False
        )

    if result[1] != None:
        embed.set_thumbnail(url=result[1])
    await message.channel.send(
        embed=embed
    )

@commands.register(
    category="programming",
)
async def question(message: discord.Message):
    pass
