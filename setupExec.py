from imaplib import Commands
import sys
import os
import json
import discord
from discord.ext import commands

def initializiation(bot:discord.Bot):
    for guild in bot.guilds:
        if f"{guild.id}.json" not in os.listdir("data/serverData"):
            serverInitData = {
                "serverOwner": f"{guild.owner}",
                "servereOwnerID": f"{guild.owner_id}",
                "guildName":f"{guild.name}",
                "adminRoles":[

                ],
                "reactionRoles":{

                }
            }



            with open(f"data/serverData/{guild.id}.json", "w") as guildDataFile:
                json.dump(serverInitData, guildDataFile, indent=4)

def initNewGuild(bot:discord.Bot, guild:discord.Guild):
    serverInitData = {
        "serverOwner": f"{guild.owner}",
        "servereOwnerID": f"{guild.owner_id}",
        "guildName":f"{guild.name}",
        "adminRoles":[

        ],
        "reactionRoles":{

        }
    }
    
    with open(f"data/serverData/{guild.id}.json", "w") as guildDataFile:
        json.dump(serverInitData, guildDataFile)