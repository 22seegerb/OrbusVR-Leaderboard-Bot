import pprint
import re
import time
import requests
import pprint

URL = "https://leaderboard-orbus.xyz/?class=0"

request = requests.get(URL)
request = str(request.content)

players = request.split("""\"3\"><a href=\"""")
players = [x.split(">")[:2] for x in players]
players = [[re.sub(r"(?i)\\...", '_', x[1][:-3]), x[0][:-1]] for x in players][1:]

with open("players.txt", "w") as f:
    for player in players:
        f.write(player[0])
        for i in range(20 - len(player[0])):
            f.write(" ")
        f.write(player[1])
        f.write("\n")
