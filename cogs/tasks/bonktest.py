import discord
from discord.ext import commands,tasks
import requests

class BonkTest(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
        self.check_bonk_status.start()
    @tasks.loop(seconds=5.0)
    async def check_bonk_status(self):
        bonkval = requests.get("http://localhost:2593/api/bonkSand")
        bonkval = bonkval.json()
        if bonkval["should_bonk_val"] is True:
            requests.post("http://localhost:2593/api/bonkSand")
            await self.bot.get_user(422846591766888464).send("Your Mums a Dude")
        else:
            pass

def setup(bot:discord.Bot):
    bot.add_cog(BonkTest(bot))