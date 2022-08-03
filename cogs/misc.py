import json
import discord
import random
from discord.ext import commands

class misc(commands.Cog):
    def __init__(self,bot:discord.Bot):
        self.bot = bot

    @commands.slash_command(description="Credits")
    async def credits(self, ctx:discord.ApplicationContext):
        respondEmbed=discord.Embed(
            title="CREDITS",
            description="**Programming:** SplitZer0\n**Twitter:** https://twitter.com/splitzer0\n\n**Project Planning:** NaoNyan\n**Twitter:** https://twitter.com/gamer_nyaa/\n**Twitch:** https://www.twitch.tv/naonyanvt\n\n**Contributors:**\n**Json & Python help:** MirageAegis\n**Twitter:** https://twitter.com/MirageAegiss\n**Twitch:** https://www.twitch.tv/mirageaegis\n\n**Command Suggestions:** Sandvich,\nOne Toasty Boi,\nMirageAegis"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=respondEmbed)

    @commands.slash_command(description="Invite Ramie to your own server")
    async def invite(self,ctx:discord.ApplicationContext):
        respondEmbed=discord.Embed(
            description="Add me to your server:\nhttps://www.echomediaworks.com/ramie"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        await ctx.respond(embed=respondEmbed)

    @commands.slash_command(description="Ramie Github Repo")
    async def repo(self, ctx:discord.ApplicationContext):
        respondEmbed=discord.Embed(
            description="Wanna contribute? Check out My Github Repo: https://github.com/EMWFabianSales/Ramiel"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        await ctx.respond(embed=respondEmbed)

    @commands.slash_command(description="Feed the prisoner")
    async def feedhorni(self, ctx:discord.ApplicationContext):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        respondEmbed = discord.Embed(
            description=f"Prisoner Has been Fed"
        )

        feedEmbed = discord.Embed(
            description= f"**OI** {self.bot.get_guild(929403679071682620).get_member(422846591766888464).mention}"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        
        feedEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        feedEmbed.set_image(url=gifs.get('feed')[random.randrange(0,len(gifs.get('feed')))])
        
        await self.bot.get_channel(996872461255725097).send(embed=feedEmbed)
        await ctx.send_response(embed=respondEmbed)

def setup(bot:discord.Bot):
    bot.add_cog(misc(bot))