import discord
from discord.ext import commands
import ramieutils


class Animesearch(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # Create Command Group
    anime = discord.SlashCommandGroup("anime", "Anime related commands")

    @anime.command(description="Search for an anime from My Anime List")
    @discord.option(
        "title",
        description="Anime Title"
    )
    async def search(self, ctx: discord.ApplicationContext, title: str):
        e = discord.Embed(
            description= f"Searching MyAnimeList for **{title}**"
        )
        m = await ctx.respond(embed=e)

        ani = ramieutils.anisearch(title)
        await m.edit_original_message(embed=ani)

    @anime.command(description="Have Ramie recommend you a random anime")
    async def random(self, ctx: discord.ApplicationContext):
        e = discord.Embed(
            description="Grabbing Random Anime"
        )

        m = await ctx.respond(embed=e)
        ani = ramieutils.randomAnime()
        await m.edit_original_message(embed=ani)


def setup(bot: discord.Bot):
    bot.add_cog(Animesearch(bot))
