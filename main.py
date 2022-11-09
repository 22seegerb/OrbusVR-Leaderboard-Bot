import discord
from discord.ext import tasks
from os import walk
import base64
import leaderboard
import update
import updatefromrecent
from update import dataFromParse
from PIL import Image

TOKEN = "MTAzOTIyNzQ3OTY3NzczOTA1OA.G4aq3l.oLFOOKvFUN_Q44aBIor5_jtx52jzJjIwIqPgKI"

bot = discord.Bot()

guilds = []
classes = ["Mage", "Scoundrel", "Ranger", "Shaman", "Warrior", "Paladin", "Musketeer", "Bard"]
colors = {
    "Mage": 32511,
    "Scoundrel": 16755200,
    "Ranger": 16645888,
    "Shaman": 4194559,
    "Warrior": 16711684,
    "Paladin": 11861846,
    "Musketeer": 971776,
    "Bard": 12779674,
}

weapon = {
    "Mage": "Wand",
    "Scoundrel": "Gun",
    "Ranger": "Bow",
    "Shaman": "Mask",
    "Warrior": "Sword",
    "Paladin": "Hammer",
    "Musketeer": "Musket",
    "Bard": "Mallets",
}


@bot.event
async def on_ready():
    print(f'Ready: {bot.user}')
    global guilds
    guilds = [g.id for g in bot.guilds]
    print(guilds)


def createBoardEmbed(title, board, playerclass, player=None):
    title += " - " + playerclass
    embed = discord.Embed(title=title)
    embed.color = colors[playerclass]
    for i, c in enumerate(board):
        line_data = c.split(" ")
        line_data = [x for x in line_data if x != ""]
        embed.add_field(name=line_data[0] + " " + line_data[1] + (" ⭐" if player == line_data[1] else ""),
                        value=line_data[3] + "\n" + line_data[5], inline=False)
    return embed


def createParseEmbed(data):
    embed = discord.Embed(title=data[0] + " - " + data[1])

    if data[5]:
        embed.title += data[5]

    embed.color = colors[data[1]]

    [ri, si], [rboard, sboard] = leaderboard.relParsePosition(data)

    embed.add_field(name="DPS", value="[" + data[2] + "](" + data[4] + ") \nPosition: " + str(ri))
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Skill DPS", value="[" + data[3] + "](" + data[4] + ") \nPosition: " + str(si))

    embed.add_field(name="Crit", value=data[7][0] + "\n\u200b")
    if data[7][1] != '':
        embed.add_field(name="Bleed", value=data[7][1].split("-")[0][:-1] + ")")
    else:
        embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    weapon_data = "Intellect: " + data[6][0] + "\n"
    weapon_data += "Strength: " + data[6][1] + "\n"
    embed.add_field(name=weapon[data[1]] + ": " + data[6][2] + " +" + data[6][3],
                    value=weapon_data)

    embed.add_field(name='\u200b', value="\u200b")

    weapon_data = ""
    def affix(a):
        a = " ".join([x.capitalize() for x in a.split("_")])
        a = a.replace("Charged Strike", "Charged Strikes")
        return a
    for a in data[6][4]:
        weapon_data += " - " + affix(a) + "\n"

    embed.add_field(name="Affixes", value=weapon_data)

    embed.add_field(name='\u200b', value=data[4], inline=False)

    def createRelativeBoardEmbed(title, board, playerclass, player=None):
        title += " - " + playerclass
        embed = discord.Embed(title=title)
        embed.color = colors[playerclass]
        for i, c in enumerate(board):
            embed.add_field(name=c[0] + " " + c[1],
                            value=c[2] + "\n" + c[3], inline=False)
        return embed

    regularBoard = createRelativeBoardEmbed("Regular", rboard, data[1])
    skillBoard = createRelativeBoardEmbed("Skill", sboard, data[1])

    return [embed, regularBoard, skillBoard]


def createEmbedPlayer(player, type, data):
    title = player + " (" + type.capitalize() + ")"
    embed = discord.Embed(title=title)
    embed.color = 34559
    for i, c in enumerate(data):
        line_data = c.split(" ")
        line_data = [x for x in line_data if x != ""]
        embed.add_field(name=line_data[0][:-1], value=line_data[1] + "\n" + line_data[3], inline=True)
        if (i - 1) % 2 == 0:
            embed.add_field(name='\u200b', value='\u200b')
    return embed

@bot.slash_command(guild_ids=[1034262640110878771])
async def top(ctx,
              type: discord.Option(str, choices=["skill", "regular"], required=False, default="regular"),
              playerclass: discord.Option(str, choices=classes, required=False, default=None),
              amount: discord.Option(int, choices=range(1, 16), required=False, default=5)):
    boards = []
    if type == "regular":
        boards = leaderboard.getRawLeaderboard(amount)
    if type == "skill":
        boards = leaderboard.getSkillLeaderboard(amount)

    if playerclass:
        await ctx.respond(
            embed=createBoardEmbed(type.capitalize() + " Leaderboard", boards[classes.index(playerclass)], playerclass))
    else:
        await ctx.respond(embeds=[createBoardEmbed(type.capitalize() + " Leaderboard", boards[classes.index(c)], c)
                                  for c in classes])


@bot.slash_command(guild_ids=[1034262640110878771])
async def player(ctx,
                 player: discord.Option(str),
                 type: discord.Option(str, choices=["skill", "regular"], required=False, default=None),
                 playerclass: discord.Option(str, choices=classes, required=False, default=None)):

    player = player.replace("_", "__")
    for playerFile in next(walk("parses"), (None, None, []))[2]:
        if player == playerFile[:-4]:
            f = open("parses/" + playerFile, "r")
            lines = f.readlines()
            skill = lines[1:9]
            raw = lines[9:17]
            if playerclass:
                skill = [skill[classes.index(playerclass)]]
                raw = [raw[classes.index(playerclass)]]
            if type == "skill":
                await ctx.respond(embed=createEmbedPlayer(player, type, skill))
            if type == "regular":
                await ctx.respond(embed=createEmbedPlayer(player, type, raw))
            if not type:
                await ctx.respond(embeds=[createEmbedPlayer(player, "regular", raw),
                                          createEmbedPlayer(player, "skill", skill)])
            return

    await ctx.respond("The specified player " + player + " could not be found.\n" +
                      "Please replace all non-alphabetical characters with \"_\".")


@bot.slash_command(guild_ids=[1034262640110878771])
async def rel_top(ctx,
                  player: discord.Option(str),
                  type: discord.Option(str, choices=["skill", "regular"], required=False, default="regular"),
                  playerclass: discord.Option(str, choices=classes, required=False, default=None),
                  amount: discord.Option(int, choices=range(1, 16), required=False, default=5)):
    boards = []
    if type == "regular":
        rawpositions = leaderboard.getPlaceOnLeaderboards(player, type)
        rawpositions = [(p - int(amount / 2) if p - int(amount / 2) > 0 else 0) if p >= 0 else -2 for p in rawpositions]
        boards = leaderboard.getRawLeaderboard(amount, rawpositions)
    elif type == "skill":
        skillpositions = leaderboard.getPlaceOnLeaderboards(player, type)
        skillpositions = [(p - int(amount / 2) if p - int(amount / 2) > 0 else 0) if p >= 0 else -2 for p in
                          skillpositions]
        boards = leaderboard.getSkillLeaderboard(amount, skillpositions)

    if playerclass:
        if not boards[classes.index(playerclass)]:
            await ctx.respond(player + " has not yet parsed for " + playerclass + ".")
        else:
            await ctx.respond(
                embed=createBoardEmbed(player + " - " + type.capitalize() + " Leaderboard",
                                       boards[classes.index(playerclass)], playerclass, player=player))
    else:
        if sum([bool(x) for x in boards]) != 0:
            await ctx.respond(embeds=[createBoardEmbed(player + " - " + type.capitalize() + " Leaderboard",
                                      boards[classes.index(c)], c, player=player) for c in classes if boards[classes.index(c)] != []])
        else:
            await ctx.respond(player + " has not yet parsed.")


@bot.slash_command(guild_ids=[1034262640110878771])
async def parse(ctx,
                url: discord.Option(str),
                show_relative_position: discord.Option(bool, required=False, default=False),
                show_graph: discord.Option(bool, required=False, default=True)):
    await ctx.respond("Getting information from Cindy, please wait...")
    try:
        url = url.split("https://leaderboard-orbus.xyz")[1]
    except:
        await ctx.respond("The link " + url + " is invalid.")

    data = dataFromParse(update.createDriver(), url)

    if data:
        def createImage(b64png, name):
            imgdata = base64.b64decode(b64png.split(",")[1])
            with open("tmp.png", 'wb') as f:
                f.write(imgdata)

            frontImage = Image.open('tmp.png')
            background = Image.open('back.png')

            frontImage = frontImage.convert("RGBA")
            background = background.convert("RGBA")

            width = (background.width - frontImage.width) // 2
            height = (background.height - frontImage.height) // 2

            background.paste(frontImage, (width, height), frontImage)
            background.save(name, format="png")

        createImage(data[8][0], "graph.png")
        graph = discord.File("graph.png", filename="graph.png")

        if show_relative_position:
            await ctx.channel.send(embeds=createParseEmbed(data))
        else:
            await ctx.channel.send(embed=createParseEmbed(data)[0])

        if show_graph:
            await ctx.channel.send(file=graph)
    else:
        await ctx.respond("The link " + url + " is invalid.")

@tasks.loop(hours=1.0)
async def update_from_recent(ctx):
    updatefromrecent.update()


bot.run(TOKEN)
