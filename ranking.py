import os
import json
import statistics
import datetime


players = []


class Player:
    def __init__(self, name=0, won=0, lost=0, wonClass={}, lostClass={}, kills=0, deaths=0, assists=0, damage=0, airs=0, hs=0, bs=0):
        self.name = name
        self.won = won
        self.lost = lost
        self.wonClass = {
                "scout": 0,
                "soldier": 0,
                "pyro": 0,
                "heavyweapons": 0,
                "engineer": 0,
                "demoman": 0,
                "sniper": 0,
                "medic": 0,
                "spy": 0
        }
        self.lostClass = {
                "scout": 0,
                "soldier": 0,
                "pyro": 0,
                "heavyweapons": 0,
                "engineer": 0,
                "demoman": 0,
                "sniper": 0,
                "medic": 0,
                "spy": 0
        }
        self.percent = 1
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.damage = damage
        self.airs = airs
        self.headshots = hs
        self.backstabs = bs

    def win(self):
        self.won += 1
        self.percent = self.won / (self.won + self.lost)

    def loose(self):
        self.lost += 1
        self.percent = self.won / (self.won + self.lost)


def checkScore(data):
    if data["teams"]["Red"]["score"] > data["teams"]["Blue"]["score"]:
        score = "Red"
    elif data["teams"]["Red"]["score"] < data["teams"]["Blue"]["score"]:
        score = "Blue"
    else:
        score = "Tie"
    return score


def getFiles():
    path_to_json = 'logs/tf2c/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    # print(json_files)  # for me this prints ['foo.json']
    # smallList = []
    # for z in range(0, 50):
    #     smallList.append(json_files[z])
    return json_files


def getPlayer(name):
    n = 0
    for player in players:
        if name == player.name:
            return n
        n += 1
    player = Player(name)
    players.append(player)
    return n


def processData():
    json_files = getFiles()
    time = []
    for file in json_files:
        with open('logs/tf2c/' + file) as json_file:
            data = json.load(json_file)

        if len(data["chat"]) >= 5:
            if data["chat"][4]["msg"] == "Location: Europe":
                score = checkScore(data)
                time.append(int(data["info"]["date"]))
                if score != "Tie":
                    for player in data["players"]:
                        n = getPlayer(player)
                        klasa = data["players"][player]["class_stats"][0]
                        klasa = klasa["type"]
                        classStats = data["players"][player]
                        if data["players"][player]["team"] == score:
                            players[n].win()
                            x = players[n].wonClass.setdefault(klasa)
                            players[n].wonClass[klasa] = x + 1
                            players[n].kills += classStats["kills"]
                            players[n].deaths += classStats["deaths"]
                            players[n].assists += classStats["assists"]
                            players[n].damage += classStats["dmg"]
                            players[n].airs += classStats["as"]
                            players[n].headshots += classStats["headshots"]
                            players[n].backstabs += classStats["backstabs"]
                        else:
                            players[n].loose()
                            x = players[n].lostClass.setdefault(klasa)
                            players[n].lostClass[klasa] = x + 1
    # time = statistics.mean(time)
    timemin = min(time)
    timemax = max(time)
    timemin = datetime.datetime.fromtimestamp(timemin)
    timemax = datetime.datetime.fromtimestamp(timemax)

    print('_________________\nTIME PERIOD')
    print(timemin.strftime('%Y-%m-%d %H:%M:%S'), timemax.strftime('%Y-%m-%d %H:%M:%S'))
    print('_________________\n')


def ranking(order=True, amount=10):
    min = averageGames()
    tab = []
    print('_________________\n FILTORWANIE')
    print(f'Ilość graczy przed filtrowaniem: {len(players)} ')
    for player in players:
        if (player.won + player.lost) > min:
            tab.append(player)
    tab.sort(key=lambda x: x.percent, reverse=order)
    if amount >= len(tab):
        amount = len(tab)
    toplist = tab[:amount]
    print(f'Ilość graczy po filtrowaniu: {len(tab)} ')
    print('_________________\nRANKING GRACZY\n\n')
    for player in toplist:
        print( f'ID:{player.name}\n Won:{player.won}\n Lost:{player.lost}\n Percent: {player.percent}\n' )
        print(f'kills: {player.kills} deaths: {player.deaths} damage: {player.damage} assists: {player.assists} \n')
        print(f'Headshots: {player.headshots}, Backstabs: {player.backstabs}, Airshots: {player.airs}')
        print(f'Wygrane: {player.wonClass}')
        print(f'Przegrane: {player.lostClass}')
        print('-----------------')


def yourStats(id):
    players.sort(key=lambda x: x.percent, reverse=True)
    for n in range(0, len(players)-1):
        if players[n].name == id:
            player = players[n]
            print(f'\n\n_____________You are {n} in {len(players)}  ___________')
            print( f'ID:{player.name}\n Won:{player.won}\n Lost:{player.lost}\n Percent: {player.percent}\n' )
            print(f'kills: {player.kills} deaths: {player.deaths} damage: {player.damage} assists: {player.assists} \n')
            print(f'Headshots: {player.headshots}, Backstabs: {player.backstabs}, Airshots: {player.airs}')
            print(f'Wygrane: {player.wonClass}')
            print(f'Przegrane: {player.lostClass}')


def stats():
    wonStats = {
            "scout": 0,
            "soldier": 0,
            "pyro": 0,
            "heavyweapons": 0,
            "engineer": 0,
            "demoman": 0,
            "sniper": 0,
            "medic": 0,
            "spy": 0
    }
    lostStats = {
            "scout": 0,
            "soldier": 0,
            "pyro": 0,
            "heavyweapons": 0,
            "engineer": 0,
            "demoman": 0,
            "sniper": 0,
            "medic": 0,
            "spy": 0
    }
    for player in players:
        wonStats["scout"] += player.wonClass["scout"]
        wonStats["soldier"] += player.wonClass["soldier"]
        wonStats["pyro"] += player.wonClass["pyro"]
        wonStats["heavyweapons"] += player.wonClass["heavyweapons"]
        wonStats["engineer"] += player.wonClass["engineer"]
        wonStats["demoman"] += player.wonClass["demoman"]
        wonStats["sniper"] += player.wonClass["sniper"]
        wonStats["medic"] += player.wonClass["medic"]
        wonStats["spy"] += player.wonClass["spy"]

        lostStats["scout"] += player.lostClass["scout"]
        lostStats["soldier"] += player.lostClass["soldier"]
        lostStats["pyro"] += player.lostClass["pyro"]
        lostStats["heavyweapons"] += player.lostClass["heavyweapons"]
        lostStats["engineer"] += player.lostClass["engineer"]
        lostStats["demoman"] += player.lostClass["demoman"]
        lostStats["sniper"] += player.lostClass["sniper"]
        lostStats["medic"] += player.lostClass["medic"]
        lostStats["spy"] += player.lostClass["spy"]
    print(wonStats)
    print(lostStats)


def averageGames():
    tab = []

    for player in players:
        val = player.won + player.lost
        tab.append(val)
    average = statistics.mean(tab)
    median = statistics.median(tab)
    bottom = 0
    normal = 0
    top = 0
    for player in players:
        val = player.won + player.lost
        if average > median:
            if val < median:
                bottom += 1
            elif val > average:
                top += 1
            else:
                normal += 1
        elif average < median:
            if val > median:
                top += 1
            elif val < average:
                bottom += 1
            else:
                normal += 1

    pom = []
    for player in players:
        val = player.won + player.lost
        if val > average:
            pom.append(val)
    clearedAverage = statistics.mean(pom)
    print('Czysta średnia:', clearedAverage)
    print('Średnia:', average)
    print('Mediana:', median)
    print(bottom, normal, top)

    ceiling = max(tab)
    array = [0] * (ceiling+1)
    for player in players:
        val = player.won + player.lost
        array[val] += 1
    sum = 0
    for n in range(1, len(array)):
        sum += (n * array[n])
        # print(n, ' występuje ', array[n], ' razy')
    print("Suma zagranych gier: ", sum)
    goal = sum * 0.2
    temp = 0
    twenty = 0
    for n in range(len(array)-1, 1, -1):
        temp += (n * array[n])
        if temp >= goal:
            twenty = n
            # print('Szukana: ', n)
            # print('20 % gier:', goal, ' Osiągnięto: ', temp)
            break
    return twenty


processData()
ranking()
# print(averageGames())
yourStats('[U:1:73989841]')
