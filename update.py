import os
from os import walk
import re
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
import time


def updateLeaderboards():
    players = next(walk("parses"), (None, None, []))[2]  # [] if no file

    classNames = ["Mage", "Scoundrel", "Ranger", "Shaman", "Warrior", "Paladin", "Musketeer", "Bard"]

    best = [[] for _ in range(8)]

    for player in players:
        f = open("parses/" + player)
        lines = f.readlines()
        name = lines[0].strip()
        for c in range(1, 9):
            values = lines[c].split(" ")
            parse = int(values[1])
            link = values[-1].strip()
            if parse:
                best[c - 1].append((name, parse, link))
        f.close()

    for c in best: c.sort(key=lambda x: -x[1])

    f = open("skillrankings.txt", "w")
    for i, c in enumerate(best):
        f.write(classNames[i] + "\n")
        for rank, player in enumerate(c):
            spaces = 16 - len(player[0]) - len(str(rank + 1))
            f.write("      " + str(rank + 1) + ": " + player[0])
            for _ in range(spaces):
                f.write(" ")
            f.write("( " + str(player[1]) + " | " + player[2] + " )\n")
        f.write("\n\n")
    f.close()

    best = [[] for _ in range(8)]
    for player in players:
        f = open("parses/" + player)
        lines = f.readlines()
        name = lines[0].strip()
        for c in range(9, 17):
            values = lines[c].split(" ")
            parse = int(values[1])
            link = values[-1].strip()
            if parse:
                best[c - 9].append((name, parse, link))
        f.close()

    for c in best: c.sort(key=lambda x: -x[1])

    f = open("rawrankings.txt", "w")
    for i, c in enumerate(best):
        f.write(classNames[i] + "\n")
        for rank, player in enumerate(c):
            spaces = 16 - len(player[0]) - len(str(rank + 1))
            f.write("      " + str(rank + 1) + ": " + player[0])
            for _ in range(spaces):
                f.write(" ")
            f.write("( " + str(player[1]) + " | " + player[2] + " )\n")
        f.write("\n\n")
    f.close()


def dataFromParse(driver, link):
    URL = "https://leaderboard-orbus.xyz" + link

    request = requests.get(URL)
    request = str(request.content)

    try:
        playerName = request.split("data-player=")
        playerName = playerName[1].split("\"")[1]
        playerName = re.sub(r"(?i)\\...", '_', playerName)

        dps = request.split("<td class=\"td1\">Total dps:</td>")
        dps = dps[1].split(">")[1].split("<")[0]
    except IndexError:
        return [playerName, "Mage", 0, 0, "_"]

    try:
        driver.get(URL)
        playerClass = driver.execute_script("""return document.getElementById("target_class").innerHTML""")
        while playerClass == '':
            time.sleep(0.1)
            playerClass = driver.execute_script("""return document.getElementById("target_class").innerHTML""")

        driver.find_element('xpath', '/html/body/div[2]/div[1]/button[2]').click()

        skill_dps = driver.execute_script("""return document.getElementById("inject_skill_dps").innerHTML""")
        while skill_dps == '':
            time.sleep(0.1)
            skill_dps = driver.execute_script("""return document.getElementById("inject_skill_dps").innerHTML""")

        subclass = driver.execute_script("""return document.getElementById("inject_sub_class_name").innerHTML""")

        bleed = driver.execute_script("""return document.getElementById("inject_bleed_dps").innerHTML""")

        crit = driver.execute_script("""return document.getElementById("inject_crit_dps").innerHTML""")

        time.sleep(1)

        graph = driver.execute_script("""return document.getElementById("line_chart").toDataURL()""")

        hit = driver.execute_script("""return document.getElementById("dot_chart").toDataURL()""")

        driver.close()


        # Get Weapon Stats
        weapon_int = request.split("data-intellect=")[1][:7].split("\"")[1]
        weapon_str = request.split("data-strength=")[1][:7].split("\"")[1]
        weapon_plus_before = request.split("before_plus=")[1][:7].split("\"")[1]
        weapon_plus_after = request.split("after_plus=")[1][:7].split("\"")[1]
        weapon_affixes = request.split("\"weapon_affixes\">")[1][:20].split("<")[0].split(",")

        return [playerName, playerClass, dps, skill_dps, URL, subclass,
                [weapon_int, weapon_str, weapon_plus_before, weapon_plus_after, weapon_affixes], [crit, bleed], [graph, hit]]
    except selenium.common.exceptions.JavascriptException:
        print("Failed to get data:", URL)
        return [playerName, "Mage", 0, 0, "_"]


def createDriver(headless=True):
    options = Options()
    options.headless = headless
    s = Service("geckodriver.exe")
    return webdriver.Firefox(options=options, service=s)


def updatePlayer(data):
    if not os.path.isfile("parses/" + data[0] + ".txt"):
        f = open("parses/" + data[0] + ".txt", "w")
        f.write(data[0] + "\n")
        classes = ["Mage", "Scoundrel", "Ranger", "Shaman", "Warrior", "Paladin", "Musketeer", "Bard"]
        maxLen = 20
        for c in classes:
            spaces = maxLen - len(c + ": 0") + 5
            f.write(c + ": 0")
            for i in range(spaces):
                f.write(" ")
            f.write("link: _ \n")
        for c in classes:
            spaces = maxLen - len(c + ": 0") + 5
            f.write(c + ": 0")
            for i in range(spaces):
                f.write(" ")
            f.write("link: _ \n")
        f.close()

    f = open("parses/" + data[0] + ".txt", "r")
    classes = f.read().split("\n")[1:]
    classes = [x for playerClass in classes for x in playerClass.split(" ") if x != '']
    parseClasses = classes[::4]
    parseDamage = classes[1::4]
    parseLinks = classes[3::4]
    highestSkill = {parseClasses[i][:-1]: [parseDamage[i], parseLinks[i]] for i in range(0, 8)}
    highestDPS = {parseClasses[i][:-1]: [parseDamage[i], parseLinks[i]] for i in range(8, 16)}

    if int(highestSkill[data[1]][0]) < int(data[3]):
        highestSkill[data[1]][0] = int(data[3])
        highestSkill[data[1]][1] = data[4]

    if int(highestDPS[data[1]][0]) < int(data[2]):
        highestDPS[data[1]][0] = int(data[2])
        highestDPS[data[1]][1] = data[4]

    f = open("parses/" + data[0] + ".txt", "w")
    f.write(data[0] + "\n")
    maxLen = 20

    for player_class in highestSkill:
        maxLen = max(maxLen, len(player_class + ": " + str(highestSkill[player_class][0])))

    for player_class in highestSkill:
        spaces = maxLen - len(player_class + ": " + str(highestSkill[player_class][0])) + 5
        f.write(player_class + ": " + str(highestSkill[player_class][0]))
        for i in range(spaces):
            f.write(" ")
        f.write("link: " + str(highestSkill[player_class][1]) + "\n")

    for player_class in highestDPS:
        spaces = maxLen - len(player_class + ": " + str(highestDPS[player_class][0])) + 5
        f.write(player_class + ": " + str(highestDPS[player_class][0]))
        for i in range(spaces):
            f.write(" ")
        f.write("link: " + str(highestDPS[player_class][1]) + "\n")
    f.close()
