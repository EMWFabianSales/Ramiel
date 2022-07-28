from email import message
import os
import json
import discord
from discord.ext import commands
admingroupdatapath = "data/adminRoles"
reactionRolesPath = "data/reactionRoles"

def checkIfAdmin(ctx:discord.ApplicationContext):
    if f"{str(ctx.guild_id)}.json" not in os.listdir(admingroupdatapath):
        with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "w") as adminGroupFile:
            blackdict = dict()

            blackdict["0"] = []
            
            json.dump(blackdict, adminGroupFile)
    
    with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "r") as adminGroupFile:
        adminGroupData = json.load(adminGroupFile)



    if ctx.user.id == ctx.guild.owner_id:
        return True
    else:
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            for role in ctx.user.roles:
                if role.id in adminGroupData:
                    return True
                    break
                else:
                    return False

def checkIfRoleInAdminFile(ctx:discord.ApplicationContext, role:discord.Role):
    with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "r") as adminGroupFile:
        adminGroupData = json.load(adminGroupFile)

    if role.id in adminGroupData["0"]:
        return True
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
        with open(f"{reactionRolesPath}/{ctx.guild_id}.json","r") as reactionPath:
            reactionData = json.load(reactionPath)

        if(str(ctx.emoji.id) != 'None'):
            if str(ctx.message_id) in reactionData:
                if f"<:{ctx.emoji.name}:{ctx.emoji.id}>" in reactionData[str(ctx.message_id)].keys():
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(self.bot.get_guild(ctx.guild_id).get_role(int(reactionData[str(ctx.message_id)][f"<:{ctx.emoji.name}:{ctx.emoji.id}>"])))
                elif f"<a:{ctx.emoji.name}:{ctx.emoji.id}>" in reactionData[str(ctx.message_id)].keys():
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(self.bot.get_guild(ctx.guild_id).get_role(int(reactionData[str(ctx.message_id)][f"<a:{ctx.emoji.name}:{ctx.emoji.id}>"])))
        #is Default Emoji
        else:
            #check if message has rection roles
            if str(ctx.message_id) in reactionData:
                if ctx.emoji.name in reactionData[str(ctx.message_id)].keys():
                    await self.bot.get_guild(ctx.guild_id).get_member(ctx.user_id).remove_roles(self.bot.get_guild(ctx.guild_id).get_role(int(reactionData[str(ctx.message_id)][ctx.emoji.name])))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, ctx:discord.ApplicationContext):
        with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "r") as reactionPath:
            reactiondata = json.load(reactionPath)
        
        #is Custom Emoji
        if(str(ctx.emoji.id) != 'None'):
            if str(ctx.message_id) in reactiondata:
                if f"<:{ctx.emoji.name}:{ctx.emoji.id}>" in reactiondata[str(ctx.message_id)].keys():
                    await ctx.member.add_roles(self.bot.get_guild(ctx.guild_id).get_role(int(reactiondata[str(ctx.message_id)][f"<:{ctx.emoji.name}:{ctx.emoji.id}>"])))
                elif f"<a:{ctx.emoji.name}:{ctx.emoji.id}>" in reactiondata[str(ctx.message_id)].keys():
                    await ctx.member.add_roles(self.bot.get_guild(ctx.guild_id).get_role(int(reactiondata[str(ctx.message_id)][f"<a:{ctx.emoji.name}:{ctx.emoji.id}>"])))
        #is Default Emoji
        else:
            #check if message has rection roles
            if str(ctx.message_id) in reactiondata:
                if ctx.emoji.name in reactiondata[str(ctx.message_id)].keys():
                    await ctx.member.add_roles(self.bot.get_guild(ctx.guild_id).get_role(int(reactiondata[str(ctx.message_id)][ctx.emoji.name])))
        
    #commands

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
    async def purge(self,ctx:discord.ApplicationContext):
        
        with open(f"{reactionRolesPath}/{str(ctx.guild.id)}.json", "r") as reactionPath:
            reactionRolesData = json.load(reactionPath)

        isadmin = False
        
        if (ctx.author.id != self.bot.get_guild(ctx.guild.id).owner_id):
            if ctx.author.guild_permissions.administrator:
                isadmin = True
            elif str(ctx.guild.id) in reactionRolesData:
                for r in ctx.author.roles:
                    if str(r.id) in reactionRolesData[str(ctx.guild.id)]:
                        isadmin = True
        else:
            isadmin = True

        if isadmin == True:
            await ctx.channel.purge()
            await ctx.send_response("channel purged", delete_after=5)
        else:
            await ctx.respond("You do not have the correct permissions to access this command")
        
    
    @adminroles.command(description="add role to admin roles")
    async def add(self, ctx:discord.ApplicationContext, role:discord.Role):
        respondEmbed = discord.Embed(
            description=f"adding **{role}** to Admin Group"
        )
        respondEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)


        m = await ctx.respond(embed=respondEmbed)

        if checkIfAdmin(ctx):
            with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "r") as adminRoleFile:
                adminGroupData:dict = json.load(adminRoleFile)
            
            if checkIfRoleInAdminFile(ctx, role):
                respondEmbed = discord.Embed(
                    description=f"**{role}** already exists in Admin Group"
                )
                respondEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)

                await m.edit_original_message(embed=respondEmbed)
            else:
                respondEmbed = discord.Embed(
                description=f"**{role}** added to Admin Group"
                )
                respondEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)
                adminGroupData["0"].append(role.id)
                await m.edit_original_message(embed=respondEmbed)
                
            with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "w") as adminRoleFile:
                json.dump(adminGroupData, adminRoleFile)
        else:
            respondEmbed = discord.Embed(
                    description=f"You do not have the correct permissions to access this command"
                )
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
            await m.edit_original_message(embed=respondEmbed)

    @adminroles.command(description="remove role from admin roles")
    async def remove(self, ctx:discord.ApplicationContext, role:discord.Role):
        respondEmbed = discord.Embed(
            description=f"removing {role} from Admin Group"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
        m = await ctx.respond(embed=respondEmbed)

        if(checkIfAdmin(ctx)):
            with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "r") as adminRoleFile:
                adminGroupData:dict = json.load(adminRoleFile)

            if(checkIfRoleInAdminFile(ctx,role)):
                del adminGroupData["0"][adminGroupData["0"].index(role.id)]
                respondEmbed = discord.Embed(
                    description=f"**{role}** removed from Admin Group"
                )
                respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
                await m.edit_original_message(embed=respondEmbed)
            else:
                respondEmbed = discord.Embed(
                    description=f"**{role}** does not exist in Admin Group"
                )
                respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
                await m.edit_original_message(embed=respondEmbed)

            with open(f"{admingroupdatapath}/{ctx.guild_id}.json", "w") as adminRoleFile:
                    json.dump(adminGroupData, adminRoleFile)
        else:
            respondEmbed = discord.Embed(
                    description=f"You do not have the correct permissions to access this command"
                )
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
            await m.edit_original_message(embed=respondEmbed)
    
    @reactionroles.command(description="Add reaction role to Message")
    async def add(self,ctx:discord.ApplicationContext, messageid, emoji, roletoadd:discord.Role):
        
        respondEmbed = discord.Embed(
            description=f"Adding reaction roles: {emoji}({roletoadd.mention}) to {messageid}"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    

        if checkIfAdmin(ctx):
            

            if f"{ctx.guild_id}.json" not in os.listdir(reactionRolesPath):
                with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "w") as reactionRolesFile:
                    json.dump(dict(), reactionRolesFile)
            
            with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "r") as reactionRolesFile:
                reactionRolesData:dict = json.load(reactionRolesFile)

            if messageid not in reactionRolesData:
                reactionRolesData[messageid] = {}

            if emoji not in reactionRolesData[messageid]:
                respondEmbed = discord.Embed(
                
                description=f"Reaction Role {emoji}({roletoadd.mention}) added to {messageid}"
                ) 
                reactionRolesData[messageid][emoji] = roletoadd.id
            else:
                respondEmbed = discord.Embed(
                
                description=f"Reaction Role {emoji}({ctx.guild.get_role(reactionRolesData[messageid].get(emoji)).mention}) Already Exists in {messageid}"
                ) 

            with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "w") as reactionRolesFile:
                json.dump(reactionRolesData, reactionRolesFile)
            
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

            await m.edit_original_message(embed=respondEmbed)
        else:
            respondEmbed = discord.Embed(
                    description=f"You do not have the correct permissions to access this command"
                )
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
            await m.edit_original_message(embed=respondEmbed)

    @reactionroles.command(description="Remove reaction role from message")
    async def remove(self,ctx:discord.ApplicationContext, messageid, emoji):
        with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "r") as reactionRolesFile:
                reactionRolesData:dict = json.load(reactionRolesFile)

        respondEmbed = discord.Embed(
            description=f"Removing reaction roles: {emoji} from {messageid}"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    

        if checkIfAdmin(ctx):
            
            if messageid not in reactionRolesData:
                reactionRolesData[messageid] = {}

            if emoji in reactionRolesData[messageid]:
                respondEmbed = discord.Embed( 
                    description=f"Reaction Role {emoji}({ctx.guild.get_role(reactionRolesData[messageid][emoji]).mention}) Removed from {messageid}"
                ) 
                del reactionRolesData[messageid][emoji]
            else:
                respondEmbed = discord.Embed(
                    description=f"Reaction Role {emoji} does not exist in {messageid}"
                ) 

            with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "w") as reactionRolesFile:
                json.dump(reactionRolesData, reactionRolesFile)
            
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

            await m.edit_original_message(embed=respondEmbed)
        else:
            respondEmbed = discord.Embed(
                    description=f"You do not have the correct permissions to access this command"
                )
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
            await m.edit_original_message(embed=respondEmbed)
    
    @reactionroles.command(description="List all reaction roles in a message")
    async def list(self, ctx:discord.ApplicationContext, messageid):
        with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "r") as reactionRolesFile:
                reactionRolesData:dict = json.load(reactionRolesFile)

        respondEmbed = discord.Embed(
            description=f"Grabbing reaction role list"
        )
        respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)

        m = await ctx.respond(embed=respondEmbed)    
        
        if checkIfAdmin(ctx):
            with open(f"{reactionRolesPath}/{ctx.guild_id}.json", "r") as reactionRolesFile:
                reactionRolesData:dict = json.load(reactionRolesFile)

            
            responseString = f"Reaction roles in {messageid}:\n"
            listItemNumber = 0
            for emoji in reactionRolesData[str(messageid)].keys():
                responseString = responseString + f"**{listItemNumber}.** {emoji}({ctx.guild.get_role(reactionRolesData[str(messageid)].get(emoji)).mention})\n"
                listItemNumber += 1
            respondEmbed =  discord.Embed(
                description=responseString
            )
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
            await m.edit_original_message(embed=respondEmbed)
        else:
            respondEmbed = discord.Embed(
                    description=f"You do not have the correct permissions to access this command"
                )
            respondEmbed.set_author(name="Ramie", icon_url=self.bot.user.avatar.url)
            await m.edit_original_message(embed=respondEmbed)

def setup(bot:discord.Bot):
    bot.add_cog(admin(bot))
