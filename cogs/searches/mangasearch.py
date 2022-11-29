import discord
from discord.ext import commands


class Mangasearch(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # Create Command Group
    manga = discord.SlashCommandGroup("manga", "Manga related commands")


def setup(bot: discord.Bot):
    bot.add_cog(Mangasearch(bot))