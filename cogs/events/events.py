import discord
from discord.ext import commands
from discord import Webhook
import aiohttp
import ramieutils
import random


class Events(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.hlv = 99

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready Master Zer0!")
        ramieutils.startup(self.bot)
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discord.com/api/webhooks/1024711374342983700/gSFJYa8gLAY6SPxlAw5iuyHNXZyD3I0Wd9WalPWhD8Xwdb_DPZJY3yWw-FlJ2jJeMcTr', session=session)
            await webhook.send('Ramie Now Online', username='Ramie Status')
            await self.bot.get_guild(929403679071682620).get_member(422846591766888464).edit(nick="bebe")

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url('https://discord.com/api/webhooks/1045884232305745930/GenkueLMPbpuXq0GpChKcB6bWMKoSlsJF9JL8cTicKXnUV0jgKiLPXp9hgqaHDnacQEY', session=session)
            await webhook.send(f'{exception}', username='Ramie Error')

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        ramieutils.create_new_guild_config(self.bot, guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild.id
        server_data = ramieutils.readData("server", guild)
        wm_index = random.randrange(0, len(server_data["welcome_messages"]))

        await self.bot.get_guild(guild).get_channel(server_data["welcome_channel"]).send(str(server_data["welcome_messages"][wm_index]).replace("$USERMENTION", member.mention))

    '''@commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        #print(after.id)
        self.hlv -= 1
        if self.hlv < 2:
            self.hlv = 99
        if after.id == 422846591766888464:
            if after.nick == f"BEBE":
                return
            else:
                await after.edit(nick="BEBE")
       '''


def setup(bot: discord.Bot):
    bot.add_cog(Events(bot))
