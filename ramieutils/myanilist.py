import requests
from bs4 import BeautifulSoup
import discord
import random

def grabAniInfo(url: str):
    anime_info = {
        "title": "Unknown",
        "genres": "Unknown",
        "score": "Unknown",
        "synopsis": "Unknown",
        "episodes": "Unknown",
        "airing_status": "Unknown",
        "airing_season": "Unknown",
        "broadcast": "Unknown",
        "studio": "Unknown",
        "url": f"{url}",
        "thumbnail_url": "Unknown"
    }

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    anime_info["title"] = soup.find("h1", class_="title-name h1_bold_none").text
    anime_info["score"] = soup.find("div", class_="fl-l score").find("div").text
    anime_info["synopsis"] = soup.find("p", itemprop="description").text[0:512]
    anime_info["synopsis"] = anime_info["synopsis"].replace("\n\r\n", "\n\n")


    anime_info["thumbnail_url"] = soup.find("div", class_="leftside").find("a").find("img")["data-src"]

    info = soup.find("td", class_="borderClass").find_all("div", class_="spaceit_pad")

    for tab in info:
        if "Episodes" in tab.text:
            anime_info["episodes"] = tab.text.replace("\nEpisodes:\n", "").replace("\n", "").replace(" ", "")
        elif "Status" in tab.text:
            anime_info["airing_status"] = tab.text.replace("\nStatus:\n", "").replace("\n", "")
        elif "Premiered" in tab.text:
            anime_info["airing_season"] = tab.text.replace("\nPremiered:\n", "").replace("\n", "")
        elif "Broadcast" in tab.text and "Broadcasting" not in tab.text:
            anime_info["broadcast"] = tab.text.replace("\nBroadcast:\n", "").replace("\n", "")
        elif "Studios" in tab.text:
            anime_info["studio"] = tab.text.replace("\nStudios:\n", "").replace("\n", "")
        elif "Genres" in tab.text:
            genres = []
            for genre in tab.find_all("a"):
                genres.append(genre.text)
            anime_info["genres"] = ", ".join(genres)

    e = discord.Embed()
    e.add_field(name="Title", value=f"[{anime_info['title']}]({anime_info['url']})", inline=False)
    e.add_field(name="Score", value=f"{anime_info['score']}", inline=False)
    e.add_field(name="Genres", value=f"{anime_info['genres']}", inline=False)
    e.add_field(name="Episodes", value=f"{anime_info['episodes']}", inline=True)
    e.add_field(name="Status", value=f"{anime_info['airing_status']}", inline=True)
    e.add_field(name="Season", value=f"{anime_info['airing_season']}", inline=True)
    e.add_field(name="Broadcast", value=f"{anime_info['broadcast']}", inline=True)
    e.add_field(name="Studios", value=f"{anime_info['studio']}", inline=True)
    e.add_field(name="Synopsis", value=f"{anime_info['synopsis']}", inline=False)
    e.set_thumbnail(url=anime_info["thumbnail_url"])
    e.set_footer(text="Source: MyAnimeList.net")
    return e

def randomAnime():

    r = requests.get("https://myanimelist.net/anime.php")
    soup = BeautifulSoup(r.text, "html.parser")

    genre_container = soup.find("div", class_="genre-link")
    genre_columns = genre_container.find_all("div", class_="genre-list-col")

    genre_list_container = genre_columns[random.randrange(0, 3)].find_all("div", class_="genre-list al")

    genre = genre_list_container[random.randrange(0, len(genre_list_container))].find("a", class_="genre-name-link")

    if "Boys Love" in genre.text or "Girls Love" in genre.text:
        genre = genre_columns[0].find("div", class_="genre-list al").find("a", class_="genre-name-link")

    print(genre.text)

    r2 = requests.get(f"https://myanimelist.net{genre['href']}")
    soup2 = BeautifulSoup(r2.text, "html.parser")

    body = soup2.find("div", id="myanimelist")
    wrapper = body.find("div", id="contentWrapper")
    titles = soup2.find_all("a", class_="link-title")

    return grabAniInfo(titles[random.randrange(0, len(titles))]["href"])

def anisearch(anime_name: str):
    # check for spaces, create search URL
    if " " in anime_name:
        anime_name = anime_name.replace(" ", "%20")

    # scrape site
    r = requests.get(f"https://myanimelist.net/search/all?q={anime_name}&cat=all")
    # parse data to BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")

    # Grab first anime in search
    searchresults = soup.find_all("article")[0].find("div", class_="list di-t w100").find("div", class_="title").find("a")

    # scrape anime's page and return Embed to Ramie
    return grabAniInfo(searchresults["href"])
