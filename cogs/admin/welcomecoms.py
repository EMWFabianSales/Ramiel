import json
import discord
from discord.ext import commands
import ramieutils

class WelcomeComs(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    welcome = discord.SlashCommandGroup("welcome", "Welcome Commands")

    @welcome.command(description="set Welcome Channel")
    @commands.has_permissions(manage_channels=True)
    @discord.option(
        "channel",
        required = False
    )
    async def setchan(self, ctx:discord.ApplicationContext, channel:discord.TextChannel):
        if channel is None:
            print("no channel provided setting channel to current channel")
            channel = ctx.channel
        
        print(f"Welcome channel is now {channel}")
        
        server_data:dict = ramieutils.readData("server", ctx.guild_id)
        server_data["welcome_channel"] = channel.id
        ramieutils.writeData("server", ctx.guild_id, server_data)

    @welcome.command(description="add a custom Welcome Message")
    @commands.has_permissions(manage_channels=True)
    async def addwm(self, ctx:discord.ApplicationContext, message:str):
        server_data:dict = ramieutils.readData("server", ctx.guild_id)
        server_data["welcome_messages"].append(message)
        ramieutils.writeData("server", ctx.guild_id,server_data)

    @welcome.command(description="add a custom Welcome Message")
    @commands.has_permissions(manage_channels=True)
    async def testwm(self, ctx:discord.ApplicationContext, index:int):
        server_data:dict = ramieutils.readData("server", ctx.guild_id)
        wm:str = server_data["welcome_messages"][index]
        wm = wm.replace("$USERMENTION", ctx.author.mention)
        await ctx.respond(wm)

    
    @welcome.command(description="add a custom Welcome Message")
    @commands.has_permissions(manage_channels=True)
    async def listwm(self, ctx:discord.ApplicationContext):
        server_data = ramieutils.readData("server", ctx.guild_id)
        wmlist = ""
        i = 0
        for m in server_data["welcome_messages"]:
            wmlist += f"{i}. {m}\n"
            i += 1
        
        await ctx.respond(wmlist)
    @welcome.command(description="add a custom Welcome Message")
    @commands.has_permissions(manage_channels=True)
    async def delwm(self, ctx:discord.ApplicationContext, index:int):
        server_data = ramieutils.readData("server", ctx.guild_id)
        server_data["welcome_messages"].pop(index)
        ramieutils.writeData("server", ctx.guild_id, server_data)
        
def setup(bot:discord.Bot):
    bot.add_cog(WelcomeComs(bot))