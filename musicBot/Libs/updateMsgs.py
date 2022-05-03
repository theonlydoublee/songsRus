from musicBot.Libs import readWrite
import hikari, lightbulb

def msgUpdate(guildID, msgNpID, msgQueueID, channelID):
    print('Add logic to update messages')

    mixer = readWrite.readGuildFile(ctx.guild_id)
    msgNpID = mixer["msgNpID"]
    msgQueueID = mixer["msgQueueID"]
    channelID = mixer["channelID"]
    try:
        # await
        await musicPL.bot.rest.edit_message(channelID, msgNpID,
                                            embed=hikari.Embed(title="New Title NP",
                                                               description="New Description NP"))
        await musicPL.bot.rest.edit_message(channelID, msgQueueID,
                                            embed=hikari.Embed(title="New Title Q",
                                                               description="New Description Q"))
    except:
        print('Add no msg logic')