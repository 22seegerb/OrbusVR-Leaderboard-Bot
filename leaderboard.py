classNames = ["Mage", "Scoundrel", "Ranger", "Shaman", "Warrior", "Paladin", "Musketeer", "Bard"]

def getSkillLeaderboard(amount, offset=[0,0,0,0,0,0,0,0]):
    f = open("skillrankings.txt", "r")
    text = f.read().strip()
    f.close()

    classLeaderboards = text.split("\n\n\n")

    classLeaderboards = [x.split("\n")[offset[i] + 1:offset[i] + amount + 1] for i, x in enumerate(classLeaderboards)]

    return classLeaderboards

def getRawLeaderboard(amount, offset=[0,0,0,0,0,0,0,0]):
    f = open("rawrankings.txt", "r")
    text = f.read().strip()
    f.close()

    classLeaderboards = text.split("\n\n\n")

    classLeaderboards = [x.split("\n")[offset[i] + 1:offset[i] + amount + 1] for i, x in enumerate(classLeaderboards)]

    return classLeaderboards

def getPlaceOnLeaderboards(player, board):
    f = None
    if board == "regular":
        f = open("rawrankings.txt", "r")
    if board == "skill":
        f = open("skillrankings.txt", "r")

    text = f.read().strip()
    classLeaderboards = text.split("\n\n\n")
    classLeaderboards = [c.split("\n") for c in classLeaderboards]

    positions = []

    def getPosition(c, player):
        for i, line in enumerate(c):
            line_data = line.split(" ")
            line_data = [x for x in line_data if x != ""]
            if len(line_data) > 1 and player == line_data[1]:
                return i - 1
        return -1

    for c in classLeaderboards:
        positions.append(getPosition(c, player))

    return positions

def relParsePosition(data: object, amount: object = 3) -> object:
    def getPosition(type, c, damage):
        f = None
        if type == "regular":
            f = open("rawrankings.txt", "r")
        if type == "skill":
            f = open("skillrankings.txt", "r")

        compareIndex = 2 if type == "regular" else 3

        text = f.read().strip()
        board = text.split("\n\n\n")

        board = board[classNames.index(c)]

        board = board.split("\n")
        board = [line.split(" ") for line in board]
        board = [[d for d in line if d != ""] for line in board]
        board = [[line[0][:-1], line[1], line[3], line[5]] for line in board[1:]]

        f.close()

        for i, line in enumerate(board):
            if damage >= int(line[2]):
                return i, board
        return len(board), board

    ri, rboard = getPosition("regular", data[1], int(data[2]))
    si, sboard = getPosition("skill", data[1], int(data[3]))

    rboard.insert(ri, [0, data[0] + " ⭐", data[2], data[4]])
    sboard.insert(si, [0, data[0] + " ⭐", data[3], data[4]])

    if ri + 1 < len(rboard) and rboard[ri][3][-10:] == rboard[ri + 1][3][-10:]:
        rboard.pop(ri + 1)
    if si + 1 < len(sboard) and sboard[si][3][-10:] == sboard[si + 1][3][-10:]:
        sboard.pop(si + 1)

    def fixNumbers(board):
        start = int(board[0][0])
        if start == 0: start = 1
        for i, line in enumerate(board):
            line[0] = str(start + i) + ":"

    fixNumbers(rboard)
    fixNumbers(sboard)

    def getBounds(i, amount):
        left = i - (amount // 2)
        right = i + amount - (amount // 2)
        if left < 0:
            left = 0
            right = amount
        return [left, right]

    rbBound = getBounds(ri, amount)
    sbBound = getBounds(si, amount)

    return [ri+1, si+1], [rboard[rbBound[0]:rbBound[1]], sboard[sbBound[0]:sbBound[1]]]


