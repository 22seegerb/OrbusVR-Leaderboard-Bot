import os
import pprint
import re
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
import pprint
import time

from update import updatePlayer, dataFromParse

def update():
    recentURL = "https://leaderboard-orbus.xyz/?recent=1"
    lastURL = open("lastupdated.txt", "r").read()

    request = requests.get(recentURL)
    request = str(request.content)

    newParses = request.split(lastURL.split("https://leaderboard-orbus.xyz")[1])[0]

    newParses = [x.split("\" class")[0] for x in newParses.split("position:relative;\" href=\"")][1:-1]

    print(newParses)

    if newParses:
        options = Options()
        options.headless = True
        s = Service("geckodriver.exe")
        driver = webdriver.Firefox(options=options, service=s)

        for parse in newParses:
            updatePlayer(dataFromParse(driver, parse))

        f = open("lastupdated.txt", "w")
        f.write("https://leaderboard-orbus.xyz" + newParses[0])

        driver.quit()