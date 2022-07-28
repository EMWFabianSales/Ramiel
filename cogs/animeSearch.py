from AnilistPython import Anilist
import discord
from discord.ext import commands

anilib = Anilist()

def remove_html(string):
    tag = False
    quote = False
    output = ""
    for ch in string:
            if ch == '<' and not quote:
                tag = True
            elif ch == '>' and not quote:
                tag = False
            elif (ch == '"' or ch == "'") and tag:
                quote = not quote
            elif not tag:
                output = output + ch
    return output

class animeSearch(commands.Cog):
    def __init__(self,bot:discord.Bot):
        self.bot = bot

    anime = discord.SlashCommandGroup("anime", "anime commands")
    manga = discord.SlashCommandGroup("manga", "manga commands")

    
    @anime.command(description="search for anime by name")
    async def search(self,ctx:discord.ApplicationContext, title:str):

        aniEmbed = discord.Embed(
            description=f"Searching for details on: **{title}**"
        )
        aniEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)

        res = await ctx.respond(embed=aniEmbed)

        aniItem = anilib.get_anime(title)
        aniairstat = aniItem.get("airing_status")
        aniepco = aniItem.get("airing_episodes")
        anigenres = aniItem.get("genres")
        anidesc = aniItem.get("desc")

        animegenres= ""
        for genre in anigenres:
            animegenres = animegenres + f"{genre}"
            if genre != anigenres[-1]:
                animegenres = animegenres + ", "
        
        aniEmbed = discord.Embed(
            title=f"{aniItem.get('name_romaji')}",
            description=f"**Airing Status:** {str(aniairstat).replace('_',' ')}\n\n**Episode Count:** {aniepco}\n\n**Genres:**\n{animegenres}\n\n**Description**:\n{remove_html(anidesc)}"
        )
        aniEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)

        aniEmbed.set_thumbnail(url=aniItem.get('cover_image'))
        await res.edit_original_message(embed=aniEmbed)
    
    @manga.command(description="search for manga by name")
    async def search(self,ctx:discord.ApplicationContext, title:str):
        
        mangaEmbed = discord.Embed(
            description=f"Searching for details on: **{title}**"
        )
        mangaEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)

        res = await ctx.respond(embed=mangaEmbed)

        mangaItem = anilib.get_manga(title)
        mangaName = mangaItem.get("name_romaji")
        mangaRelStatus = mangaItem.get("release_status")
        mangaDesc = mangaItem.get("desc")
        mangaGenreList = mangaItem.get("genres")

        mangaGenreString = ""
        for genre in mangaGenreList:
            mangaGenreString = mangaGenreString + f"{genre}"
            if genre != mangaGenreString[-1]:
                mangaGenreString = mangaGenreString + ", "

        mangaEmbed = discord.Embed(
            title = f"{mangaName}",
            description = f"**Status:** {mangaRelStatus}\n\n**Genres:**\n{mangaGenreString}\n\n**Description:**\n{remove_html(mangaDesc)}"
        )
        mangaEmbed.set_author(name="Ramie",icon_url=self.bot.user.avatar.url)

        mangaEmbed.set_thumbnail(url=mangaItem.get("cover_image"))
        await res.edit_original_message(embed=mangaEmbed)
        
def setup(bot:discord.Bot):
    bot.add_cog(animeSearch(bot))