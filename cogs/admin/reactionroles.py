import discord
from discord.ext import commands
import ramieutils


class ReactionRoles(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    rr = discord.SlashCommandGroup("rr", "Reaction Role Commands")

    @rr.command(description="Reaction Roles")
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, message_id: str, emoji, role: discord.Role):
        print(emoji)

        serverdata = ramieutils.readData("server", ctx.guild_id)

        e = discord.Embed(
            description=""
        )

        if message_id not in serverdata["reactionRoles"]:
            serverdata['reactionRoles'][message_id] = {}
            serverdata['reactionRoles'][message_id]['max-roles'] = 0
            serverdata['reactionRoles'][message_id]["rr"] = {}

        if emoji in serverdata["reactionRoles"][message_id]["rr"]:
            e.description = f"{emoji} is already being used"
        else:
            serverdata['reactionRoles'][str(message_id)]["rr"][emoji] = role.id

            e.description = f"{emoji}|{role.mention} added to Message {message_id}"
            msg = await channel.fetch_message(message_id)
            await msg.add_reaction(emoji)

        ramieutils.writeData("server", ctx.guild_id, serverdata)
        await ctx.respond(embed=e)

    @rr.command(description="Remove a Reaction Role")
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, message_id: str, emoji):
        serverdata = ramieutils.readData("server", ctx.guild_id)

        e = discord.Embed()

        if message_id not in serverdata["reactionRoles"] or emoji not in serverdata["reactionRoles"][str(message_id)]['rr']:
            e.description = f"{emoji} not in Message Reaction Roles"
        else:
            msg = await ctx.guild.get_channel(channel.id).fetch_message(int(message_id))
            await msg.remove_reaction(emoji, ctx.guild.get_member(self.bot.user.id))
            e.description = f"{emoji} ({ctx.guild.get_role(serverdata['reactionRoles'][message_id]['rr'][emoji]).mention}) Removed from Reaction Roles"
            del serverdata["reactionRoles"][message_id]['rr'][emoji]

            ramieutils.writeData("server", ctx.guild_id, serverdata)

        await ctx.respond(embed=e)

    @rr.command(description="Configure Specific Reaction Role objects")
    @commands.has_permissions(manage_messages=True)
    @discord.option(
        "setting",
        choices=[
            discord.OptionChoice(name="Max Roles")
        ]
    )
    async def config(self, ctx: discord.ApplicationContext, message_id: str, setting: str = "", setting_value: str = ""):
        serverdata = ramieutils.readData("server", ctx.guild_id)

        if setting == "Max Roles":
            serverdata["reactionRoles"][message_id]["max-roles"] = int(setting_value)

        ramieutils.writeData("server", ctx.guild_id, serverdata)

def setup(bot: discord.Bot):
    bot.add_cog(ReactionRoles(bot))
