import os
import json
import datetime
import humanfriendly
import discord
from discord.ext import commands
import discord.utils
reactionRolesPath = "data/reactionRoles"

def checkIfAdmin(ctx:discord.ApplicationContext):
    with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
        serverData = json.load(serverFile)

    if ctx.user.id == ctx.guild.owner_id:
        return True
    else:
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            for role in ctx.user.roles:
                if role.id in serverFile["adminRoles"]:
                    return True
                    break
                else:
                    return False

class admin(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot

    admin = discord.SlashCommandGroup("admin", "Admin Commands")
    adminroles = discord.SlashCommandGroup("adminroles","Manage Admin Roles")
    reactionroles = discord.SlashCommandGroup("reactionroles","Reaction Role Commands")

    #listeners
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,ctx):
        with open(f"data/serverData/{ctx.guild_id}.json","r") as serverFile:
            serverData = json.load(serverFile)

        if(str(ctx.emoji.id) != 'None'):
            if str(ctx.message_id) in serverData["reactionRoles"]:
                if f"<:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]:
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(self.bot.get_guild(ctx.guild_id).get_role(int(serverData["reactionRoles"][str(ctx.message_id)][f"<:{ctx.emoji.name}:{ctx.emoji.id}>"])))
                elif f"<a:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]:
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(self.bot.get_guild(ctx.guild_id).get_role(int(serverData["reactionRoles"][str(ctx.message_id)][f"<a:{ctx.emoji.name}:{ctx.emoji.id}>"])))
        #is Default Emoji
        else:
            #check if message has rection roles
            if str(ctx.message_id) in serverData["reactionRoles"]:
                if ctx.emoji.name in serverData["reactionRoles"][str(ctx.message_id)].keys():
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(self.bot.get_guild(ctx.guild_id).get_role(int(serverData["reactionRoles"][str(ctx.message_id)][ctx.emoji.name])))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx:discord.ApplicationContext):
        with open(f"data/serverdata/{ctx.guild_id}.json", "r") as serverFile:
            serverData = json.load(serverFile)
        
        #is Custom Emoji
        if(str(ctx.emoji.id) != 'None'):
            if str(ctx.message_id) in serverData["reactionRoles"]:
                if f"<:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]:
                    await ctx.member.add_roles(self.bot.get_guild(ctx.guild_id).get_role(int(serverData["reactionRoles"][str(ctx.message_id)][f"<:{ctx.emoji.name}:{ctx.emoji.id}>"])))
                elif f"<a:{ctx.emoji.name}:{ctx.emoji.id}>" in serverData["reactionRoles"][str(ctx.message_id)]:
                    await ctx.member.add_roles(self.bot.get_guild(ctx.guild_id).get_role(int(serverData["reactionRoles"][str(ctx.message_id)][f"<a:{ctx.emoji.name}:{ctx.emoji.id}>"])))
        #is Default Emoji
        else:
            #check if message has rection roles
            if str(ctx.message_id) in serverData["reactionRoles"]:
                if ctx.emoji.name in serverData["reactionRoles"][str(ctx.message_id)]:
                    await ctx.member.add_roles(self.bot.get_guild(ctx.guild_id).get_role(int(serverData["reactionRoles"][str(ctx.message_id)][ctx.emoji.name])))
        
    #commands
    @admin.command(description="Put User in Time Out")
    async def timeout(self, ctx:discord.ApplicationContext, user:discord.Member, duration:discord.Option(description="timeout duration"), reason:discord.Option(str, description="reason for time out", required=False)):
        if checkIfAdmin(ctx):
            time = humanfriendly.parse_timespan(duration)
            m = await ctx.respond(f"placing {user} in time out")

            await user.timeout(until= discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)

            await m.edit_original_message(f"{user} has been placed in timeout for \"{reason}\"")

    @admin.command(description="Ban User")
    async def ban(self, ctx:discord.ApplicationContext, user:discord.Member, reason:discord.Option(str, description="reason for ban", required=False)):
        if checkIfAdmin(ctx):

            m = await ctx.respond(f"banning {user}")
            await user.ban(reason=reason)
            await m.edit_original_message(f"{user} has been banned for \"{reason}\"")

    @admin.command(description="Kick User")
    async def kick(self, ctx:discord.ApplicationContext, user:discord.Member, reason:discord.Option(str, description="reason for kick", required=False)):
        if checkIfAdmin(ctx):

            m = await ctx.respond(f"banning {user}")
            await user.kick(reason=reason)
            await m.edit_original_message(f"{user} has been kicked for \"{reason}\"")

    @admin.command(description="announce message in channel")
    async def announce(self,ctx:discord.ApplicationContext, channelid, announcement:str):
        if checkIfAdmin(ctx):
            responseEmbed = discord.Embed(
                description=f"Announcement Sent to <#{channelid}>"
            )
            await ctx.respond(embed=responseEmbed)
            await self.bot.get_channel(int(channelid)).send(announcement)
        else:
            await ctx.respond("You do not have the correct permissions to access this command")


    @admin.command(description="Purge channel of all messages")
    async def purge(self,ctx:discord.ApplicationContext, purgetype:discord.Option(str, description="'c' for Channel Purge, 'i' for integer delete"), deletesize:discord.Option(int, required=False)):
        if checkIfAdmin(ctx):
            if(purgetype == 'c'):
                await ctx.channel.purge()
                await ctx.send_response("channel purged", delete_after=2)
            if(purgetype == 'i'):
                await ctx.channel.purge(limit=deletesize)
                await ctx.send_response(f"{deletesize} messages purged", delete_after=2)
        else:
            await ctx.respond("You do not have the correct permissions to access this command")

    @adminroles.command(description="add role to admin roles")
    async def add(self, ctx:discord.ApplicationContext, role:discord.Role):
        respondEmbed = discord.Embed(
            description=f"adding {role.mention} to Admin Group"
        )
        respondEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)
        
        m = await ctx.respond(embed=respondEmbed)

        #Admin Check
        if checkIfAdmin(ctx):
            with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)

            if role.id in serverData["adminRoles"]:
                respondEmbed.description = f"{role.mention} already in Admin Group"
            else:
                serverData["adminRoles"].append(role.id)

                respondEmbed.description = f"{role.mention} added to Admin Group"
    
            #write data:
            with open(f"data/serverData/{ctx.guild_id}.json", "w") as serverFile:
                json.dump(serverData, serverFile, indent=4)
        else:
            respondEmbed.description = f"You do not have the correct permissions to use **/adminroles** command"
        
        await m.edit_original_message(embed=respondEmbed)
               
            
    @adminroles.command(description="remove role from admin roles")
    async def remove(self, ctx:discord.ApplicationContext, role:discord.Role):
        respondEmbed = discord.Embed(
            description=f"removing {role.mention} from Admin Group"
        )
        
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        
        m = await ctx.respond(embed=respondEmbed)

        if(checkIfAdmin(ctx)):
            with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)

            if role.id not in serverData["adminRoles"]:
                respondEmbed.description = f"{role.mention} not in Admin Group"
            else:
                del serverData["adminRoles"][serverData["adminRoles"].index(role.id)]
                respondEmbed.description = f"{role.mention} removed from Admin Group"
            
            with open(f"data/serverData/{ctx.guild_id}.json", "w") as serverFile:
                json.dump(serverData, serverFile, indent=4)
        else:
            respondEmbed.description = f"You do not have the correct permissions to use **/adminroles** command"

        await m.edit_original_message(embed=respondEmbed)
            
    @adminroles.command(description="List all Admin Roles")
    async def list(self, ctx:discord.ApplicationContext):
        with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)

        respondEmbed = discord.Embed(
            description=f"Grabbing reaction role list"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    
        
        if checkIfAdmin(ctx):
            with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)
            
            responseString = f"roles in Admin Group:\n"
            listItemNumber = 0
            for role in serverData["adminRoles"]:
                responseString = responseString + f"**{listItemNumber}.** {ctx.guild.get_role(role).mention}\n"
                listItemNumber += 1
            respondEmbed.description = responseString
        else:
            respondEmbed.description=f"You do not have the correct permissions to access this command"
        await m.edit_original_message(embed=respondEmbed)

    @reactionroles.command(description="Add reaction role to Message")
    async def add(self,ctx:discord.ApplicationContext, messageid, emoji, roletoadd:discord.Role):
        
        respondEmbed = discord.Embed(
            description=f"Adding reaction roles: {emoji}({roletoadd.mention}) to {messageid}"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    

        if checkIfAdmin(ctx):
            with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)

            if str(messageid) not in serverData["reactionRoles"]:
                serverData["reactionRoles"][str(messageid)] = {}

            if emoji in serverData["reactionRoles"][str(messageid)].keys():
                respondEmbed.description = f"{emoji} already in message's Reaction Roles"
            else:
                serverData["reactionRoles"][str(messageid)][emoji] = roletoadd.id
                respondEmbed.description = f"{emoji} ({roletoadd.mention}) added to message's Reaction Roles"

            with open(f"data/serverData/{ctx.guild_id}.json", "w") as serverFile:
                json.dump(serverData, serverFile, indent=4)
        await m.edit_original_message(embed=respondEmbed)

    @reactionroles.command(description="Remove reaction role from message")
    async def remove(self,ctx:discord.ApplicationContext, messageid, emoji):
        respondEmbed = discord.Embed(
            description=f"Removing reaction roles: {emoji} from {messageid}"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    

        if checkIfAdmin(ctx):
            with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)
            if (messageid not in serverData["reactionRoles"].keys()) or (emoji not in serverData["reactionRoles"][str(messageid)]):
                respondEmbed.description = f"{emoji} not in messages's Reaction Roles"
            else:
                del serverData["reactionRoles"][str(messageid)][emoji]
                respondEmbed.description = f"{emoji} removed from message's Reaction Roles"
            with open(f"data/serverData/{ctx.guild_id}.json", "w") as serverFile:
                json.dump(serverData, serverFile, indent=4)
        await m.edit_original_message(embed=respondEmbed)
    
    @reactionroles.command(description="List all reaction roles in a message")
    async def list(self, ctx:discord.ApplicationContext, messageid):
        with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)

        respondEmbed = discord.Embed(
            description=f"Grabbing reaction role list"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    
        
        if checkIfAdmin(ctx):
            with open(f"data/serverData/{ctx.guild_id}.json", "r") as serverFile:
                serverData:dict = json.load(serverFile)

            
            responseString = f"Reaction roles in {messageid}:\n"
            listItemNumber = 0
            for emoji in serverData["reactionRoles"][str(messageid)].keys():
                responseString = responseString + f"**{listItemNumber}.** {emoji}({ctx.guild.get_role(serverData['reactionRoles'][str(messageid)].get(emoji)).mention})\n"
                listItemNumber += 1
            respondEmbed.description = responseString
        else:
            respondEmbed.description=f"You do not have the correct permissions to access this command"
        await m.edit_original_message(embed=respondEmbed)

def setup(bot:discord.Bot):
    bot.add_cog(admin(bot))
