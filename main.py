import os
import discord
from dotenv import load_dotenv
import discord.ext
import setupExec

load_dotenv()
testToken = os.getenv('testtoken')
buildToken = os.getenv('buildtoken')

botintents = discord.Intents.all()
bot = discord.Bot(intents=botintents, auto_sync_commands=True)

@bot.event
async def on_ready():
    setupExec.initializiation(bot)
    print(f"Logged in as {bot.user.name} with ID {bot.user.id}\nSERVERS:")
    for guild in bot.guilds:
        print(f"{guild.name} | {guild.id} | {guild.member_count} | Owner: {guild.owner} | Owner ID: {guild.owner_id}")

initial_extentions = []

@bot.event
async def on_guild_join(guild):
    setupExec.initNewGuild(bot, guild)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extentions.append(f"cogs.{filename[:-3]}")

if __name__ == '__main__':
    for extention in initial_extentions:
        bot.load_extension(extention)

bot.run(buildToken)