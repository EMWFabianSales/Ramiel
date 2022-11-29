import discord
from discord.ext import commands
import os
import ramieutils
from dotenv import load_dotenv


class Reactions(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    react = discord.SlashCommandGroup('react','Reaction Commands')

    @react.command(description="hug your buds, hug your dog, hug your mums, just hug everyone")
    async def hug(self, ctx: discord.ApplicationContext, target: discord.Member):
        e = discord.Embed()
        e.description = f"**{ctx.author.mention} hugs {target.mention}. aww**"
        
        m = await ctx.respond(embed=e)
        
        gif = ramieutils.tenor_search("anime hug")
        e.set_image(url=gif)
        
        await m.edit_original_message(embed=e)

    @react.command(description="slap your friends for saying something dumb, or just for being down horrendous.")
    async def slap(self, ctx: discord.ApplicationContext, target: discord.Member):
        e = discord.Embed()
        e.description = f"**{ctx.author.mention} SLAPPED {target.mention}.**"
        
        m = await ctx.respond(embed=e)
        
        gif = ramieutils.tenor_search("anime slap")
        e.set_image(url=gif)
        
        await m.edit_original_message(embed=e)

    @react.command(description="bonk the horni")
    async def bonk(self, ctx: discord.ApplicationContext, target: discord.Member):
        e = discord.Embed()
        e.description = f"**{ctx.author.mention} Bonked {target.mention}.**"
        
        m = await ctx.respond(embed=e)
        
        gif = ramieutils.tenor_search("anime bonk")
        e.set_image(url=gif)
        
        await m.edit_original_message(embed=e)

    @react.command(description="punch, idk i'm running out of descriptions")
    async def punch(self, ctx: discord.ApplicationContext, target: discord.Member):
        e = discord.Embed()
        e.description = f"**{ctx.author.mention} Punched {target.mention}.**"
        
        m = await ctx.respond(embed=e)
        
        gif = ramieutils.tenor_search("anime punch")
        e.set_image(url=gif)
        
        await m.edit_original_message(embed=e)

    @react.command(description="headpat your friends, the wholesome nuggets, the innocent beans.")
    async def headpat(self, ctx: discord.ApplicationContext, target: discord.Member):
        e = discord.Embed()
        e.description = f"**{ctx.author.mention} pat {target.mention}'s head.**"
        
        m = await ctx.respond(embed=e)
        
        gif = ramieutils.tenor_search("anime head pat")
        e.set_image(url=gif)
        
        await m.edit_original_message(embed=e)

    @react.command(description="PEW PEW PEW THIS IS AMERICA, if it isn't... WELL IT IS NOW!!")
    async def shoot(self, ctx: discord.ApplicationContext, target: discord.Member):
        e = discord.Embed()
        
        e.description = f"**{ctx.author.mention} shot {target.mention}.**"
        m = await ctx.respond(embed=e)
        
        gif = ramieutils.tenor_search("anime shoot")
        
        e.set_image(url=gif)
        await m.edit_original_message(embed=e)

def setup(bot: discord.Bot):
    bot.add_cog(Reactions(bot))
