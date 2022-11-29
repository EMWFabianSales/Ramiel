import random
import requests
import json
import os

def tenor_search(search_term):
    api_key = os.getenv("tenor")
    ckey = os.getenv("tenorckey")

    payload = {"q": search_term, "key": api_key, "client_key": ckey, "limit": 10}
    gifs = requests.get("https://tenor.googleapis.com/v2/search", params=payload)
    gifs = gifs.json()
    
    randgif = random.randrange(0, len(gifs["results"]))
    
    return gifs["results"][randgif]["media_formats"]["mediumgif"]["url"]

if(__name__ == "__main__"):
    i = 0
    while (i < 10):
        print(tenor_search("anime bonk"))
        i += 1