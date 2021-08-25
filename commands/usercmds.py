from settings import *


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
