import os
from dotenv import load_dotenv
import discord
import ramieutils


def main():
    load_dotenv()
    token = os.getenv("testtoken")
    bot = discord.Bot(intents=discord.Intents.all())
    for directory in os.listdir("cogs"):
        for file in os.listdir(f"./cogs/{directory}"):
            if file.endswith(".py"):
                bot.load_extension(f"cogs.{directory}.{file[:-3]}")
    print(bot.cogs.keys())
    bot.run(token)


if __name__ == '__main__':
    main()
