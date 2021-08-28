from settings import *


@commands.register(
    category='team',
    botTeam=True
)
async def addlang(message: discord.Message):
    args = message.content.split(" ")[1:]
    author: discord.Member = message.author
    channel: discord.TextChannel = message.channel

    if not args: await channel.send(embed=discord.Embed(color=discord.Color.red(), description="bitte gebe der sprache einen namen")); return
    languageName = message.content.split(" ", 1)[1].lower()
    database.db.execute(f"INSERT OR IGNORE INTO programming_languages(name) VALUES ('{languageName}')")
    await channel.send(embed=discord.Embed(color=discord.Color.green(), description=f"Die Sprache `{languageName}` wurde hinzugefügt"))

@commands.register(
    category='team',  # 'information'
    botTeam=True
)
async def changemoney(message: discord.Message):
    args = message.content.split(" ")[1:]
    author: discord.Member = message.author
    channel: discord.TextChannel = message.channel
    if not args:
        await channel.send("*enter a num...*")
        return True
    if message.mentions:
        if len(args) > 1:
            if args[1].isnumeric():
                mention_user: discord.Member = message.mentions[0]
                try:
                    money = api.userGet(mention_user.id, "money") + int(args[1])
                except TypeError:
                    await channel.send(f"Oh... {mention_user.display_name} ist mir nicht bekannt")
                    return
                api.userUpdate(mention_user.id, "money", money)
                await channel.send(f"*yay **{mention_user.display_name}** hat nun **{str(money)}** geld*")
                return True

    await channel.send("*no no no...*")
    return True  # Wichtig