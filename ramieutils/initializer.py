import os
import discord
from ramieutils import jsonUtils


def startup(bot: discord.Bot):
    for guild in bot.guilds:
        print(f"{guild.name} | {guild.member_count} Members | {guild.id}")
        if f"{guild.id}.json" not in os.listdir("data/server/"):
            print(f"{guild.name} has no data, creating blank server Config")
            create_new_guild_config(bot, guild.id)


def create_new_guild_config(bot: discord.Bot, guild_id: int):
    init_server_data = jsonUtils.readInitData("server")

    guild = bot.get_guild(guild_id)

    init_server_data["serverOwner"] = guild.owner.name
    init_server_data["serverOwnerID"] = guild.owner_id
    init_server_data["guildName"] = guild.name
    init_server_data["guildID"] = guild.id

    for user in guild.members:
        if not user.bot:
            init_server_data["users"][str(user.id)] = {}
            init_server_data["users"][str(user.id)]["name"] = user.name
            init_server_data["users"][str(user.id)]["id"] = user.id
            init_server_data["users"][str(user.id)]["blacklisted"] = False
            init_server_data["users"][str(user.id)]["warnings"] = {}

    print(init_server_data)
    jsonUtils.writeData("server", guild.id, init_server_data)
