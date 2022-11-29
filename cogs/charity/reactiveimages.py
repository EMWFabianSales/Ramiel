import discord
from discord.ext import commands


class ReactiveImages(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    ri = discord.SlashCommandGroup("ri", "reactive Images")

    @ri.command(description="Get Reactive image link for any user")
    async def grab(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.respond(f"{user.mention}'s Reactive Image Link is: https://reactive.fugi.tech/individual/{user.id}")

    @ri.command()
    @commands.has_permissions(manage_channels=True)
    async def payload(self, ctx: discord.ApplicationContext):
        for user in ctx.guild.members:
            if not user.bot:
                await ctx.respond(
                    f"{user.mention}'s Reactive Image Link is: https://reactive.fugi.tech/individual/{user.id}")


def setup(bot: discord.Bot):
    bot.add_cog(ReactiveImages(bot))