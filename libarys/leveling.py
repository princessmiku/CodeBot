import discord, random, time
from . import UserConnector, getRole

api: UserConnector.Connect = None

# Level System
# Voice
voice_time = 60
voice_save_interval = 360
voice_guilds_times = {}
user_voice_task = {}
# Text Chat
level_xp = [2, 5]
level_up_channel = 785560666626588672
# Hauptchat, Diskussion, Kummerkasten,
# Support, Vorstellungsrunde, NSFW Haupt Chat
# Anime Haupt Chat, Gaming Hauptchat, Zeichnen Haupt chats

level_allowed_channel = [743860301186990150, 744588473117179934, 744588515618062357,
                         746434143386075177, 745575249202118697, 746821322402693231,
                         746773204223131758, 746761029450727464, 746773868445958156]

level_user_cooldown = {}
level_default_list = {10: 1, 60: 2, 160: 3, 310: 4, 510: 5, 760: 6, 1060: 7, 1410: 8, 1810: 9, 2260: 10, 2760: 11, 3310: 12, 3910: 13, 4560: 14, 5260: 15, 6010: 16, 6810: 17, 7660: 18, 8560: 19, 9510: 20, 10510: 21, 11560: 22, 12660: 23, 13810: 24, 15010: 25, 16260: 26, 17560: 27, 18910: 28, 20310: 29, 21760: 30, 23260: 31, 24810: 32, 26410: 33, 28060: 34, 29760: 35, 31510: 36, 33310: 37, 35160: 38, 37060: 39, 39010: 40, 41010: 41, 43060: 42, 45160: 43, 47310: 44, 49510: 45, 51760: 46, 54060: 47, 56410: 48, 58810: 49, 61260: 50, 63760: 51, 66310: 52, 68910: 53, 71560: 54, 74260: 55, 77010: 56, 79810: 57, 82660: 58, 85560: 59, 88510: 60, 91510: 61, 94560: 62, 97660: 63, 100810: 64, 104010: 65, 107260: 66, 110560: 67, 113910: 68, 117310: 69, 120760: 70, 124260: 71, 127810: 72, 131410: 73, 135060: 74, 138760: 75, 142510: 76, 146310: 77, 150160: 78, 154060: 79, 158010: 80, 162010: 81, 166060: 82, 170160: 83, 174310: 84, 178510: 85, 182760: 86, 187060: 87, 191410: 88, 195810: 89, 200260: 90, 204760: 91, 209310: 92, 213910: 93, 218560: 94, 223260: 95, 228010: 96, 232810: 97, 237660: 98, 242560: 99, 247510: 100}
level_default_list_needXP = {1: 60, 2: 100, 3: 150, 4: 200, 5: 250, 6: 300, 7: 350, 8: 400, 9: 450, 10: 500, 11: 550, 12: 600, 13: 650, 14: 700, 15: 750, 16: 800, 17: 850, 18: 900, 19: 950, 20: 1000, 21: 1050, 22: 1100, 23: 1150, 24: 1200, 25: 1250, 26: 1300, 27: 1350, 28: 1400, 29: 1450, 30: 1500, 31: 1550, 32: 1600, 33: 1650, 34: 1700, 35: 1750, 36: 1800, 37: 1850, 38: 1900, 39: 1950, 40: 2000, 41: 2050, 42: 2100, 43: 2150, 44: 2200, 45: 2250, 46: 2300, 47: 2350, 48: 2400, 49: 2450, 50: 2500, 51: 2550, 52: 2600, 53: 2650, 54: 2700, 55: 2750, 56: 2800, 57: 2850, 58: 2900, 59: 2950, 60: 3000, 61: 3050, 62: 3100, 63: 3150, 64: 3200, 65: 3250, 66: 3300, 67: 3350, 68: 3400, 69: 3450, 70: 3500, 71: 3550, 72: 3600, 73: 3650, 74: 3700, 75: 3750, 76: 3800, 77: 3850, 78: 3900, 79: 3950, 80: 4000, 81: 4050, 82: 4100, 83: 4150, 84: 4200, 85: 4250, 86: 4300, 87: 4350, 88: 4400, 89: 4450, 90: 4500, 91: 4550, 92: 4600, 93: 4650, 94: 4700, 95: 4750, 96: 4800, 97: 4850, 98: 4900, 99: 4950}
level_reward_roles = {2: 743862893807796357, 5: 746424501490810962, 15: 746424514245820539, 40: 746424517500469328, 60: 746424519362871297}


async def level_xp_add(member: discord.Member, channel):
    if channel.id not in level_allowed_channel:
        return
    api.userInsert(member.id)
    if not level_user_cooldown.__contains__(member.id):
        level_user_cooldown[member.id] = 0

    if level_user_cooldown[member.id] + 5 > time.time():
        return
    level_user_cooldown[member.id] = time.time()

    api.userAdd(member.id, 'money', 5)

    user_xp = api.userGet(member.id, "xp")
    user_allxp = api.userGet(member.id, "allxp")
    user_level = api.userGet(member.id, "level")
    need_xp = level_default_list_needXP[user_level]

    randomXP = random.randint(level_xp[0], level_xp[1])
    user_xp += randomXP
    user_allxp += randomXP
    if user_xp > need_xp:
        user_level += 1
        user_xp = 0
        api.userUpdate(member.id, "level", user_level)
        role = False
        try:
            role_id = level_reward_roles[user_level]
            role = getRole.getRole(member.guild, roleID=role_id)
            await member.add_roles(role)
        except KeyError:
            None
        to_money_add = 25
        if 10 > user_level:
            to_money_add = 50
        elif 20 > user_level > 9:
            to_money_add = 100
        elif 40 > user_level > 19:
            to_money_add = 150
        elif user_level > 39:
            to_money_add = 200
        api.userAdd(member.id, 'money', to_money_add)

        ping = api.userGet(member.id, "levelupnotifi")
        addStr = f"Coins: `{str(to_money_add)}`"
        if role:
            addStr += f"Rolle: {role.mention}"
        embed = discord.Embed(
            title=":star: Level UP!",
            description=f"{member.mention} bist nun Level `{str(user_level)}`\n"
        )
        if ping == 1:
            await member.guild.get_channel(level_up_channel).send(member.mention, embed=embed)
        else:
            await member.guild.get_channel(level_up_channel).send(embed=embed)

    api.userUpdate(member.id, "allxp", user_allxp)
    api.userUpdate(member.id, "xp", user_xp)

