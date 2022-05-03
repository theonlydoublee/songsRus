import json
import os
from pathlib import Path


def readGuildFile(guildID):
    if not os.path.exists(f'musicBot/Files/{guildID}.json'):
        with open(f'musicBot/Files/{guildID}.json', 'w') as file:
            data = {
                      "msgNpID": 0,
                      "msgQueueID": 0,
                      "channelID": 0
                    }
            json.dump(data, file, indent=2)
        file.close()

    with open(f'musicBot/Files/{guildID}.json', 'r') as file:
        data = json.loads(file.read())
        print(f"reading: {data}")
        return data


def writeGuildFile(data, guildID):
    with open(f'musicBot/Files/{guildID}.json', 'w') as file:
        json.dump(data, file, indent=2)
        print(f"writing: {data}")
        file.close()


def setGuildFile(guildID, msgNpID, msgQueueID, channelID):
    data = readGuildFile(guildID)
    data['msgNpID'] = msgNpID
    data['msgQueueID'] = msgQueueID
    data['channelID'] = channelID
    print(f"set: {data}")
    writeGuildFile(data, guildID)
