import os
import discord
from dotenv import load_dotenv
import discord.ext

load_dotenv()
testToken = os.getenv('testtoken')
buildToken = os.getenv('buildtoken')

botintents = discord.Intents.all()
bot = discord.Bot(intents=botintents, guild_ids=[929403679071682620])


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} with ID {bot.user.id}\nSERVERS:")
    for guild in bot.guilds:
        print(f"{guild.name} | {guild.id} | {guild.member_count} | Owner: {guild.owner} | Owner ID: {guild.owner_id}")

initial_extentions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extentions.append(f"cogs.{filename[:-3]}")

if __name__ == '__main__':
    for extention in initial_extentions:
        bot.load_extension(extention)

bot.run(buildToken)