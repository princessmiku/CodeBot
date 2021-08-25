import asyncio

import discord

"""
Erstelle mit Hilfe dieser Klasse einfach Embeds die über mehrere seiten gehen
"""

class PageEmbed:

    def __init__(self, client: discord.Client, channel: discord.TextChannel, interact: discord.Member=False):
        self.client = client
        self.channel = channel
        self.interact = interact
        self.pages = {}

    def addPage(self, embed: discord.Embed):
        """Füge eine Seite hinzu mit einem Embed"""
        num = len(list(self.pages.keys()))
        self.pages[num] = embed

    def addPageStr(self, text: str):
        """Füge eine Seite hinzu mit einem String"""
        embed = discord.Embed(
            description=text
        )
        self.addPage(embed)

    async def run(self):
        """Lasse deine Seiten laufen"""
        if len(self.pages) < 1: await self.channel.send("*no results*"); return
        message = await self.channel.send(embed=discord.Embed(description="*loading...*"))
        maxPages = len(self.pages) - 1
        if maxPages < 2: await message.edit(embed=self.pages[0].set_footer(text="Data from https://www.coingecko.com/")); return
        if maxPages > 2: await message.add_reaction("↩")
        await message.add_reaction("⬅")
        await message.add_reaction("➡")
        if maxPages > 2: await message.add_reaction("↪")
        acceptEmojis = ["↩", "⬅", "➡", "↪"]
        runPages = True
        selectedPage = 0
        while runPages:
            await asyncio.sleep(0.2)
            await message.edit(embed=self.pages[selectedPage].set_footer(text=f"Page {str(selectedPage + 1)} / {maxPages + 1} | Data from https://www.coingecko.com/"))
            try:
                def check(playload):
                    if self.interact == False: return playload.message_id == message.id and playload.emoji.name in acceptEmojis
                    return playload.message_id == message.id and playload.emoji.name in acceptEmojis and playload.user_id == self.interact.id
                playload = await self.client.wait_for('raw_reaction_add', timeout=60, check=check)
            except asyncio.TimeoutError:
                runPages = False
                try:
                    await message.add_reaction("🚫")
                except:
                    pass
                break
            emoji = playload.emoji.name
            await message.remove_reaction(emoji, self.client.get_user(playload.user_id))
            if emoji == "↩":
                selectedPage = 0
            elif emoji == "⬅":
                if selectedPage <= 0: selectedPage = maxPages
                else: selectedPage -= 1
            elif emoji == "➡":
                if selectedPage >= maxPages: selectedPage = 0
                else: selectedPage += 1
            elif emoji == "↪":
                selectedPage = maxPages
