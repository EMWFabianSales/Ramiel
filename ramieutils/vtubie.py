import requests
from bs4 import BeautifulSoup as Bs
import discord

def generatelink(vtubername):
    vtubername = vtubername.split()

    searchlink = "https://vtubie.com/wp-admin/admin-ajax.php?s="

    if len(vtubername) > 1:
        for word in vtubername:
            searchlink = searchlink + f"{word}%20"
    else:
        searchlink = searchlink + vtubername[0]

    searchlink = searchlink + "&action=ma_s_ajax"

    return searchlink


def vtubiesearch(vtname:str):
    #vtname = input("Type VTuber Name: ")

    link = generatelink(vtname)
    #print(link + "\n\n\n")

    r = requests.get(link)
    rs = Bs(r.text, "html.parser")

    results = rs.find("div", class_="ma-s-ajax-result-item-container")
    vtuberlist = results.find_all("a", class_="ma-s-ajax-result-item-link")

    r = requests.get(vtuberlist[0]["href"])
    rs = Bs(r.text, "html.parser")

    vtuberinfo = grabVtuberInfo(vtuberlist[0]["href"])
    return vtuberinfo

def grabVtuberInfo(url:str):
    vtuberInfo = {
        "imgURL":"",
        "name":"",
        "group":"",
        "language":"",
        "description":"",
        "lore":"",
        "nicknames": "",
        "socials": ""
    }

    response = requests.get(url)
    doc = Bs(response.text, "html.parser")
    
    sections = doc.find("div", class_="ma-col-two-third").find_all("div", class_="ma-section-content")
    section2 = doc.find("div", class_="ma-col-one-third").find_all("div", class_="ma-section-content")


    #grab groups
    groups = ""

    for group in section2[3].find_all("li"):
        if group != section2[3].find_all("li")[-1]:
            groups = groups + f"{group.find('a').string}\n"
        else:
            groups = groups + f"{group.find('a').string}"

    #grab languages
    langs = ""

    for lang in section2[6].find_all("li"):
        if lang != section2[6].find_all("li")[-1]:
            langs = langs + f"{lang.find('a').string}\n"
        else:
            langs = langs + f"{lang.find('a').string}"

    #Create Description
    desc = ""
    for paragraph in sections[0].find_all("p"):
        if paragraph != sections[0].find_all("p")[-1]:
            desc = desc + f"{paragraph.string}\n\n"
        else:  
            desc = desc + f"{paragraph.string}"

    #create lore
    lore = ""
    for paragraph in sections[1].find_all("p"):
        if paragraph != sections[1].find_all("p")[-1]:
            lore = lore + f"{paragraph.string}\n\n"
        else:  
            lore = lore + f"{paragraph.string}"

    #nick names
    nicks = ""
    for name in sections[2].find_all("a"):
        if name.string == "+ Add":
            break
        else:
            if name != sections[2].find_all("a")[-1]:
                nicks = nicks + f"{name.string}, "
            else:  
                nicks = nicks + f"{name.string}."

    #socials
    socs = ""

    for link in sections[6].find_all("li"):


        socs = socs + f"{link.find('a')['href']}\n"

    #grab twitter


    socs = socs + section2[10].find("a")["href"]

    e = discord.Embed()
    e.add_field(name="Name", value=f"[{doc.find('h1', class_='ma-nov-page-title').text}]({url})", inline=True)
    e.add_field(name="Nicknames", value=nicks, inline=False)
    e.add_field(name="Groups", value=groups, inline=False)
    e.add_field(name="Languages", value=langs, inline=False)
    e.add_field(name="Socials", value=socs, inline=False)
    e.add_field(name="Description", value=desc, inline=False)
    e.add_field(name="Lore", value=lore, inline=False)
    e.set_thumbnail(url=doc.find("div", class_="ma-n-img-cont").find("img")["src"])

    '''vtuberInfo["imgURL"] = doc.find("div", class_="ma-n-img-cont").find("img")["src"]
    vtuberInfo["name"] = f"[{doc.find('h1', class_='ma-nov-page-title').text}]({url})"
    vtuberInfo["group"] = groups
    vtuberInfo["language"] = langs
    vtuberInfo["description"] = desc
    vtuberInfo["lore"] = lore
    vtuberInfo["nicknames"] = nicks
    vtuberInfo["socials"] = socs'''
    return e

