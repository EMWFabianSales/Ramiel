import discord
from discord.ext import commands, tasks

import ramieutils


class ReactionRoleEvents(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    async def giveRole(self, ctx: discord.RawReactionActionEvent):
        serverData = ramieutils.readData("server", ctx.guild_id)

        # is Custom Server Emoji
        if f"<:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]['rr']:
            await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).add_roles(
                self.bot.get_guild(ctx.guild_id).get_role(
                    serverData["reactionRoles"][str(ctx.message_id)]['rr'][f"<:{ctx.emoji.name}:{ctx.emoji.id}>"]))
        # is Animated Custom Server Emoji
        elif f"<a:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]['rr']:
            await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).add_roles(self.bot.get_guild(
                ctx.guild_id).get_role(
                serverData["reactionRoles"][str(ctx.message_id)]['rr'][f"<a:{ctx.emoji.name}:{ctx.emoji.id}>"]))
        else:
            await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).add_roles(
                self.bot.get_guild(ctx.guild_id).get_role(
                    serverData["reactionRoles"][str(ctx.message_id)]['rr'][ctx.emoji.name]))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx: discord.RawReactionActionEvent):
        serverData: dict() = ramieutils.readData("server", ctx.guild_id)

        # print(ctx)
        countedRoles = 0

        if ctx.member is not self.bot.user:
            if str(ctx.message_id) in serverData["reactionRoles"]:
                if serverData['reactionRoles'][str(ctx.message_id)]['max-roles'] != 0:
                    for role in ctx.member.roles:
                        if role.id in serverData["reactionRoles"][str(ctx.message_id)]["rr"].values():
                            countedRoles += 1
                    if countedRoles >= serverData['reactionRoles'][str(ctx.message_id)]['max-roles']:
                        await ctx.member.send(
                            "you have already claimed the max roles for that message, please remove some roles and try again")
                    else:
                        await self.giveRole(ctx)
                else:
                    await self.giveRole(ctx)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, ctx: discord.RawReactionActionEvent):
        serverData = ramieutils.readData("server", ctx.guild_id)

        if ctx.member is not self.bot.user:
            if str(ctx.message_id) in serverData["reactionRoles"]:
                # is Custom Server Emoji
                if f"<:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]['rr']:
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(
                        self.bot.get_guild(ctx.guild_id).get_role(
                            serverData["reactionRoles"][str(ctx.message_id)]['rr'][f"<:{ctx.emoji.name}:{ctx.emoji.id}>"]))
                # is Animated Custom Server Emoji
                elif f"<a:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]['rr']:
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(
                        self.bot.get_guild(ctx.guild_id).get_role(
                            serverData["reactionRoles"][str(ctx.message_id)]['rr'][f"<a:{ctx.emoji.name}:{ctx.emoji.id}>"]))
                else:
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(
                        self.bot.get_guild(ctx.guild_id).get_role(
                            serverData["reactionRoles"][str(ctx.message_id)]['rr'][ctx.emoji.name]))


def setup(bot: discord.Bot):
    bot.add_cog(ReactionRoleEvents(bot))
