import discord
from discord.ext import commands
import random

class ManageChannel(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    chan = discord.SlashCommandGroup("chan","channel management")
    keys = ["nico", "pablo", "juan", "sheen", "homura", "connor"]

    @chan.command(description="Nuke a channel of all messages")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx: discord.ApplicationContext):
        key = self.keys[random.randrange(0, len(self.keys))]
        responseEmbed = discord.Embed(
            description=f"Nuking in progress"
        )
        await ctx.send_response(embed=responseEmbed)
        await ctx.channel.purge()

    @chan.command(description="erase a specific number of messages from a channel")
    @commands.has_permissions(manage_channels=True)
    async def purge(self, ctx: discord.ApplicationContext, num: int):
        responseEmbed = discord.Embed(
            description=f"purging, {num} messages"
        )
        await ctx.send_response(embed=responseEmbed)
        await ctx.channel.purge(limit=num + 1)


def setup(bot: discord.Bot):
    bot.add_cog(ManageChannel(bot))
