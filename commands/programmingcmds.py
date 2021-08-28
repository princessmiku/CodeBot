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
                embed=discord.Embed(description="Der user hat keine daten", color=discord.Color.red()))
            return
        langStr = "• `" + "`\n• `".join(langList) + "`"
        await message.channel.send(embed=discord.Embed(
            description=langStr,
            color=discord.Color.teal(),
            title=f"Programmiersprachen von {user.name}"
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
            description= "Hier kannst du aussuchen welche Sprachen du alles kannst, diese werden dann im Profil angezeigt",
            color=discord.Color.teal(),
            title="Programmiersprachen"
        )
        if len(possible) != 0:
            embed.add_field(
                name="Verfügbar",
                value= "• `" + "`\n• `".join(possible) + "`"
            )
        if len(langList) != 0:
            embed.add_field(
                name="Ausgewählt",
                value="• `" + "`\n• `".join(langList) + "`"
            )
        embed.add_field(
            name="Commands",
            value=f"Hinzufügen\n`{client_prefix}lang [sprache]`\n\nEntfernen\n`{client_prefix}lang [sprache]`",
            inline=False
        )
        await message.channel.send(embed=embed)
        return
    result = database.db.execute(f"SELECT * FROM programming_languages WHERE name = '{message.content.split(' ', 1)[1].lower()}'").fetchone()
    if result is None: await message.channel.send(embed=discord.Embed(description="Sprache nicht gefunden", color=discord.Color.red())); return
    userdata: list = json.loads(api.userGet(message.author.id, "langs"))
    if userdata.__contains__(result[0]):
        userdata.remove(result[0])
        userdata = sorted(userdata)
        api.userUpdate(message.author.id, "langs", json.dumps(userdata))
        await message.channel.send(
            embed=discord.Embed(
                description=f"Die Sprache `{result[0].capitalize()}` wurde aus deinem Profil entfernt"
            )
        )
        return
    userdata.append(result[0])
    userdata = sorted(userdata)
    api.userUpdate(message.author.id, "langs", json.dumps(userdata))
    await message.channel.send(
        embed=discord.Embed(
            description=f"Die Sprache `{result[0].capitalize()}` wurde deinem Profil hinzugefügt"
        )
    )


@commands.register(
    category="programming",
)
async def info(message: discord.Message):
    args: list = message.content.split(" ")[1:]
    if not args: await lang(message); return
    result = database.db.execute(f"SELECT * FROM programming_languages WHERE name = '{message.content.split(' ', 1)[1].lower()}'").fetchone()
    if result is None: await message.channel.send(embed=discord.Embed(description="Sprache nicht gefunden", color=discord.Color.red())); return
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
