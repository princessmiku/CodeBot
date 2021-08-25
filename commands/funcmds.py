from settings import *

@commands.register(
    category='fun'  # 'information'
)
async def hey(message: discord.Message):
    em: discord.Embed = discord.Embed(description="Hey")
    await message.channel.send(embed=em)
    return True


