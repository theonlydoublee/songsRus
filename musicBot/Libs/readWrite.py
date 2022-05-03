import json
from pathlib import Path


def readGuildFile(guildID):
    myfile = Path(f'musicBot/Files/{guildID}.json')
    myfile.touch(exist_ok=True)

    with open(f'musicBot/Files/{guildID}.json', 'r') as file:
        data = json.loads(file.read())
        return data


def writeGuildFile(data, guildID):
    with open(f'musicBot/Files/{guildID}.json', 'w') as file:
        json.dump(data, file, indent=2)


def setGuildFile(guildID, msgNpID, msgQueueID, channelID):
    data = readGuildFile(guildID)
    data['msgNP'] = msgNpID
    data['msgQueueID'] = msgQueueID
    data['channelID'] = channelID
