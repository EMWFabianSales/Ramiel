import discord
from discord.ext import commands
import datetime

import ramieutils


class ManageUser(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    user = discord.SlashCommandGroup("user", "manage users")

    # timeout command
    @user.command(description="place user in time out")
    @commands.has_permissions(moderate_members=True)
    @discord.option(
        "duration",
        min_value=0,
        max_value=99999,
        choices=[
            discord.OptionChoice(name="15 minutes", value=15),
            discord.OptionChoice(name="30 minutes", value=30),
            discord.OptionChoice(name="1 hour", value=60),
            discord.OptionChoice(name="2 hours", value=120),
            discord.OptionChoice(name="4 hours", value=240)
        ]
    )
    async def timeout(self, ctx: discord.ApplicationContext, user: discord.Member, duration: int, reason: str = ""):
        responseEmbed = discord.Embed(
            description=f"**TIME OUT**\n\n**User**:\n{user.mention}\n\n**Duration**: {duration} Minutes\n\n**Reason**:\n{reason}"
        )
        responseEmbed.set_author(name="Ramie", url="https://www.echomediaworks.com/ramie",
                                 icon_url=self.bot.user.avatar.url)
        responseEmbed.set_footer(icon_url=ctx.author.avatar.url, text=f"Timed out by {ctx.author.name}")

        await ctx.respond(embed=responseEmbed)
        await user.timeout_for(duration=datetime.timedelta(minutes=duration), reason=reason)

    @user.command(description="Ban User")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: discord.ApplicationContext, user: discord.Member, reason: str = ""):
        responseEmbed = discord.Embed(
            description=f"**BAN**\n\n**User**:\n{user.mention}\n\n**Reason**:\n{reason}"
        )
        responseEmbed.set_author(name="Ramie", url="https://www.echomediaworks.com/ramie",
                                 icon_url=self.bot.user.avatar.url)
        responseEmbed.set_footer(icon_url=ctx.author.avatar.url, text=f"Timed out by {ctx.author.name}")
        await ctx.respond(embed=responseEmbed)
        await user.ban(delete_message_days=2, reason=reason)

    @user.command(description="kick user from server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: discord.ApplicationContext, user: discord.Member, reason: str = ""):
        responseEmbed = discord.Embed(
            description=f"**KICK**\n\n**User**:\n{user.mention}\n\n**Reason**:\n{reason}"
        )
        responseEmbed.set_author(name="Ramie", url="https://www.echomediaworks.com/ramie",
                                 icon_url=self.bot.user.avatar.url)
        responseEmbed.set_footer(icon_url=ctx.author.avatar.url, text=f"Timed out by {ctx.author.name}")
        await ctx.respond(embed=responseEmbed)
        await user.kick(reason=reason)

    @user.command(description="change a users nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx:discord.ApplicationContext, target: discord.Member, new_name: str):
        responseEmbed = discord.Embed(
            description=f"**NAME CHANGE**\n\n{target.name} Changed to {new_name}."
        )
        await ctx.guild.get_member(target.id).edit(nick=f"{new_name}")
        await ctx.respond(embed=responseEmbed)

    @user.command(description="give user a warning")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx: discord.ApplicationContext, target:discord.Member, reason: str):
        responseEmbed = discord.Embed(
            description=f"**WARNING**\n\n**User**: {target.mention}\n\nReason: {reason}"
        )
        await ctx.respond(embed=responseEmbed)
        responseEmbed.description = f"**WARNING**\n\nServer: {ctx.guild.name}\n\nReason: {reason}"
        await target.send(embed=responseEmbed)

        server_data = ramieutils.readData("server", ctx.guild_id)
        server_data["users"][str(target.id)]["warnings"][len(server_data["users"][str(target.id)]["warnings"])] = f"{reason}"
        ramieutils.writeData("server", ctx.guild_id, server_data)

    @user.command(description="give user a warning")
    @commands.has_permissions(moderate_members=True)
    async def warnings(self, ctx:discord.ApplicationContext, target:discord.Member):
        server_data = ramieutils.readData("server", ctx.guild_id)
        responseEmbed = discord.Embed(
            description=f"**WARNINGS**\n\n**User**: {target.mention}\n\n"
        )
        warnint = 0
        for warning in server_data["users"][str(target.id)]["warnings"].values():
            responseEmbed.description += f"{warnint}. {warning}\n"
            warnint += 1
        await ctx.respond(embed=responseEmbed)

    @user.command(description="give user a warning")
    @commands.has_permissions(moderate_members=True)
    async def fakeout(self, ctx: discord.ApplicationContext, target: discord.Member, title: str, contents: str):
        responseEmbed = discord.Embed(
            description=f"**{title}**\n\n{contents}"
        )
        await ctx.respond(embed=responseEmbed)
        await target.send(embed=responseEmbed)

def setup(bot: discord.Bot):
    bot.add_cog(ManageUser(bot))
