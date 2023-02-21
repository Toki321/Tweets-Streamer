from helpers.tweepyClient import getTweepyClient

client = getTweepyClient()


# Get the ids and users from a table with the urls of twitter accounts and output to a txt file for further use

def extractUsername(url):
    url = url.split("/")
    return url[3]


def extractStuff():
    with open("idsToTrackNEW.txt", "r") as f:
        lines = f.readlines()
        toTrackIdList = []
        for line in lines:
            toTrackIdList.append(extractUsername(line).strip())

        return toTrackIdList


def writeStuff(toTrackUserList):
    with open("accountsForTracking.txt", "w") as f:
        for username in toTrackUserList:
            user = client.get_user(username=username)
            id = user[0]["id"]
            f.write(username + " " + str(id) + "\n")


toTrackUserList = extractStuff()

writeStuff(toTrackUserList)
