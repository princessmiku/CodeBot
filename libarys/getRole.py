import discord


def getRole(guild: discord.Guild, message: discord.Message = None, roleID=None, rolestr=None):
    try:
        if roleID != None:
            role: discord.Role = guild.get_role(roleID)
            return role
        if message != None:
            if message.role_mentions:
                return message.role_mentions[0]
            else:
                r: str = message.content.split(" ", 1)[1]
                if r.isnumeric():
                    role = guild.get_role(r)
                    return role

                for x in guild.roles:
                    if x.name.lower() == r.lower():
                        return x
        if rolestr != None:
            if rolestr.isnumeric():
                role = guild.get_role(rolestr)
                return role

            for x in guild.roles:
                if x.name.lower() == rolestr.lower():
                    return x

        return None
    except:
        return None