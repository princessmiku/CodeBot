from settings import *

@client.event
async def on_ready():
    print("online")
    await client.change_presence(activity=discord.Game(name=f"{client_prefix}help | Eat errors"))


@client.event
async def on_message(message: discord.Message):
    if message.author.bot or message.author.id == client.user.id: return
    #api.userInsert(message.author.id)
    #await leveling.level_xp_add(message.author, message.channel)
    #await achiSys.Achievements(message.author.id, message).progressAchievement("chat", "active")
    await commands.call(message)

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
# Funktionen die er vor dem starten ausführen soll
createHelpEmbed() # wichtig zum funktionieren der Help List

client.run(tokens.bot_token)