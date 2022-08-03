import os
import json
import discord
import random
from discord.ext import commands

class reacts(commands.Cog):
    def __init__(self,bot:discord.Bot):
        self.bot = bot

    react = discord.SlashCommandGroup("react","reaction commands")

    @react.command(description="bonk your enenmies, or just your  horni friends :3")
    async def bonk(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if  target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} bonked **Themselves**?!?!"
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} bonked {target.mention}"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**COUNTER**\n{self.bot.user.mention} bonked {ctx.author.mention}"
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('bonk')[random.randrange(0,len(gifs.get('bonk')))])
    
        await ctx.send_response(embed=respondEmbed)

    @react.command(description="Crush your enemies under the weight of you hammer")
    async def hammer(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} bashed **THEIR OWN** skull in with a hammer?!?!"
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} bashed {target.mention}'s skull in with a hammer"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**COUNTER**\n{self.bot.user.mention} bashed {ctx.author.mention}'s skull in with a hammer"
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('hammer')[random.randrange(0,len(gifs.get('hammer')))])
    
        await ctx.respond(embed=respondEmbed)

    @react.command(description="Bash in someones face with a pan")
    async def pan(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if  target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} smacked **THEMSELVES** with a frying pan?!?!"
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} smacked {target.mention} with a frying pan"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**COUNTER**\n{self.bot.user.mention} smacked {ctx.author.mention} with a frying pan"
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('pan')[random.randrange(0,len(gifs.get('pan')))])
    
        await ctx.send_response(embed=respondEmbed)

    @react.command(description="its in the name, hug your friends, your enemies, everyone deserves a hug now and then")
    async def hug(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if  target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} hugs **themselves**, how creepy"
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} hugs {target.mention}"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**FAILED COUNTER**\n{ctx.author.mention} hugs {target.mention}, th-thank you (Ŏ艸Ŏ)"
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('hug')[random.randrange(0,len(gifs.get('hug')))])
    
        await ctx.send_response(embed=respondEmbed)
    
    @react.command(description="Headpat your friends, spread the love!!")
    async def headpat(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if  target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} gave **themselves** a headpat, a self pat? idk..."
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} gave {target.mention} a headpat"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**COUNTER**\n{ctx.author.mention} gave {target.mention} a headpat, sorry but i don't like getting my hair messy :3 "
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('headpat')[random.randrange(0,len(gifs.get('headpat')))])
    
        await ctx.send_response(embed=respondEmbed)

    @react.command(description="guns, guns, guns this is America, if it isn't... well it is now!!")
    async def gun(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if  target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} shot **themselves**... ummm... somebody get the doctor"
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} shot {target.mention}, **calls emergency number**"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**COUNTER**\n{ctx.author.mention} shot {target.mention}, nice try"
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('gun')[random.randrange(0,len(gifs.get('gun')))])
    
        await ctx.send_response(embed=respondEmbed)
    
    @react.command(description="go on, slap a bitch")
    async def slap(self, ctx:discord.ApplicationContext, target:discord.Member):
        with open("data/memegifs.json","r") as memegif:
            gifs = json.load(memegif)
        
        if  target == ctx.author:
            respondEmbed = discord.Embed(
                description=f"{ctx.author.mention} slapped **themselves**... you good?"
            )
        elif target != self.bot.user:
            respondEmbed = discord.Embed(
                description=f"**ghasp**{ctx.author.mention} slapped {target.mention}"
            )
        else:
            respondEmbed = discord.Embed(
                description=f"**COUNTER**\n{ctx.author.mention} slapped {target.mention}, Ramie is untouchable"
            )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        respondEmbed.set_image(url=gifs.get('slap')[random.randrange(0,len(gifs.get('slap')))])
    
        await ctx.send_response(embed=respondEmbed)
def setup(bot:discord.Bot):
    bot.add_cog(reacts(bot))