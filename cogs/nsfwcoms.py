import discord
from discord.ext import commands

class nsfwcoms(commands.Cog):
    def __init__(self,bot:discord.Bot):
        self.bot = bot

    nsfw = discord.SlashCommandGroup("nsfw", "nsfw commands")

    @nsfw.command(description="Look for hentai ;3")
    async def hentai(self, ctx:discord.ApplicationContext):
        await ctx.author.edit(nick=f"{ctx.author.name} is Horni")

        respondEmbed = discord.Embed(
            description=f"{ctx.author.mention} IS HORNI!!"
        )

        await ctx.respond(embed=respondEmbed)

def setup(bot:discord.Bot):
    bot.add_cog(nsfwcoms(bot))