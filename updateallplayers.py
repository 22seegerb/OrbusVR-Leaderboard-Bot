import pprint
import re
import time
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from update import updatePlayer, dataFromParse

def getSkillDPS(name, URL):
    request = requests.get(URL)
    request = str(request.content)

    links = [request[start: end + 16] for start, end in [(i.start(), i.end()) for i in re.finditer(r"\?id=", request)]]
    links = links[8:-40]

    options = Options()
    options.headless = True
    s = Service("geckodriver.exe")
    driver = webdriver.Firefox(options=options, service=s)

    for i, link in enumerate(links):
        print(name + " : (" + str(i + 1) + "/" + str(len(links)) + ")")
        updatePlayer(dataFromParse(driver, link))

    driver.quit()

players = open("players.txt", "r").read().split("\n")
players = [[x.split(" ")[0], x.split(" ")[-1]] for x in players]

for player in players:
    getSkillDPS(player[0], "https://leaderboard-orbus.xyz/" + player[1])



