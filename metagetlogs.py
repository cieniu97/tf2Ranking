import requests
import urllib.request
import time
import json
import os.path
from bs4 import BeautifulSoup
import urllib


class GetLogs:

    def __init__(self, logs=False, gamemode=False, saveLocation=False):
        self.logs = logs
        self.gamemode = gamemode
        self.saveLocation = saveLocation

    def checkIfLogExists(self):
        for log in self.logs:
            pom = log
            log = str(log)
            print("Processing " + log)
            if os.path.isfile(self.saveLocation + log + '.json'):
                print("File exist - Skiping ", log)
                self.logs.remove(pom)

    def access(self):
        for log in self.logs:
            log = str(log)
            print("Proceeding to access file")
            urlJson = "http://logs.tf/json/" + log
            response = requests.get(urlJson)

            if response.status_code == 200:
                dataFromLog = requests.get(url=urlJson).json()
                self.checkGamemode(dataFromLog, log)
            else:
                print("Access deneid: ", response.status_code)
            time.sleep(0.25)

    def download(self, data, log, subbed=""):
        print("...........Downloading...........")
        with open(self.saveLocation + log + '.json', 'w') as outfile:
            json.dump(data, outfile)
        print("added log nr: " + log)
        time.sleep(0.5)

    def checkGamemode(self, data, log):
        if 'players' in data:
            ilegraczy = len(data["players"])
            if (self.gamemode == "hl" or self.gamemode == 9):
                if ilegraczy == (self.gamemode*2):
                    self.download(data, log)
                # elif ilegraczy >= (self.gamemode*2):
                # self.download(data, log, "Subbed-Lobby")
                else:
                    print("Game plaied with not enough players - Not eligible for statistics")
            elif (self.gamemode == "6s" or self.gamemode == 6):
                if ilegraczy == (self.gamemode*2):
                    self.download(data, log)
                # elif ilegraczy >= (self.gamemode*2):
                #     self.download(data, log, "Subbed-Lobby")
                else:
                    print("Game plaied with not enough players - Not eligible for statistics")
            else:
                print('Invalid log, not containing players')




def namesOfLogs(data):
    hrefs = []
    for z in data["logs"]:
        hrefs.append(z["id"])
    return hrefs


class InputListLogs:

    def __init__(self, title=False, map=False, uploader=False, players=False, limit=False, offset=False):
        self.title = title
        self.map = map
        self.uploader = uploader
        self.players = players
        self.limit = limit
        self.offset = offset

    def combineData(self):
        urlJson = "http://logs.tf/api/v1/log?"
        listOfplayers = ""
        if self.title is not False:
            urlJson += "&title=" + str(self.title)
        if self.map is not False:
            urlJson += "&map=" + str(self.map)
        if self.uploader is not False:
            urlJson += "&uploader=" + str(self.uploader)
        if self.players is not False:
            for player in self.players:
                listOfplayers = listOfplayers + player + ","
            listOfplayers = listOfplayers[:-1]
            urlJson += "&players=" + str(self.players)
        if self.limit is not False:
            urlJson += "&limit=" + str(self.limit)
        if self.offset is not False:
            urlJson += "&offset=" + str(self.offset)
        return urlJson

    def getData(self):
        urlJson = self.combineData()
        print("1.Attempting to access input data from", urlJson)
        print("2.It might take a while with limit set to big number")
        response = requests.get(urlJson)
        if response.status_code == 200:
            print('3.Data downloaded successfully')
            data = requests.get(url=urlJson).json()
            return data
        else:
            return response


inputData = InputListLogs()

inputData.limit = 10
# How many logs you wish to download

inputData.title = "Combined"
# Title of logs must containing

# inputData.map = map

# inputData.uploader = uploader

# inputData.players = players
# players should be displayed as array of steamID64 for example [steamID64, steamID64, steamID64, steamID64]

# inputData.limit = limit


# inputData.offset = offset
# from what log you wish to start your limit - default is 0 so logs are newest


listOfLogs = namesOfLogs(inputData.getData())

new = GetLogs()
new.logs = listOfLogs
new.gamemode = 6
new.saveLocation = 'logs/test/'
new.checkIfLogExists()
new.access()
