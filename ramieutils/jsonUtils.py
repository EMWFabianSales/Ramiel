import json


def readInitData(type: str):
    if type == "user":
        with open(f"data/blankUserData.json", "r") as userFile:
            userinitdata = json.load(userFile)

            return userinitdata
    if type == "server":
        with open(f"data/blankServerData.json", "r") as serverFile:
            serverinitdata = json.load(serverFile)

            return serverinitdata


def readData(type: str, id):
    if type == "user":
        with open(f"data/user/{id}.json", "r") as userFile:
            userdata = json.load(userFile)

            return userdata
    if type == "server":
        with open(f"data/server/{id}.json", "r") as serverFile:
            serverdata = json.load(serverFile)

            return serverdata


def writeData(type:str, id, data:dict()):
    if type == "user":
        with open(f"data/user/{id}.json", "w") as userFile:
            json.dump(data, userFile, indent=4)

    if type == "server":
        with open(f"data/server/{id}.json", "w") as serverFile:
            json.dump(data, serverFile, indent=4)
