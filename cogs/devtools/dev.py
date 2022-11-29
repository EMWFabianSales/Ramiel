import discord
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    devtools = discord.SlashCommandGroup("devtools", "tools only for developer", guild_ids=[985278997963374652])

    @devtools.command(description="Invite Dev Bot")
    async def invite(self, ctx: discord.ApplicationContext):
        await ctx.respond("https://discord.com/api/oauth2/authorize?client_id=981213332491108362&permissions=4398046511095&scope=bot%20applications.commands")

    @devtools.command(description="Grab User Avatar")
    async def avatar(self, ctx: discord.ApplicationContext, user):
        e = discord.Embed()
        e.set_image(url=self.bot.get_user(int(user)).avatar.url)
        await ctx.respond(embed=e)

    @devtools.command(description="get delay from bot to client")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"{round(self.bot.latency*1000)}ms")


def setup(bot: discord.Bot):
    bot.add_cog(Dev(bot))
