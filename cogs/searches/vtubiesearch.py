import discord
from discord.ext import commands

import ramieutils


class Vtubiesearch(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    # Create Command Group
    vtubie = discord.SlashCommandGroup("vtubie", "VTuber related commands")

    @vtubie.command(description="Search for VTuber")
    async def search(self, ctx: discord.ApplicationContext, vtuber_name: str):
        e = discord.Embed(
            description=f"searching VTubie for {vtuber_name}"
        )
        m = await ctx.respond(embed=e)
        e = ramieutils.vtubiesearch(vtuber_name)
        await m.edit_original_message(embed=e)


def setup(bot: discord.Bot):
    bot.add_cog(Vtubiesearch(bot))
