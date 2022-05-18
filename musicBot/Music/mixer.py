import typing as t
from asyncio import sleep

import hikari
import lightbulb
from musicBot.Music.musicCommands import lavalink
from hikari.api import ActionRowBuilder

from musicBot.Libs import readWrite

mixerPL = lightbulb.Plugin('mixerPL')

# region Emojis
# ▶️- Play
# ⏸️- Pause
# ⏹️- Stop Single
# ⏭️- Skip
# 🔂 - Repeat Single
#
# 🔁 - Repeat Queue
# 🔀 - Shuffle Queue
# ⏹️ - Clear Queue
#
# 🔻 - Volume Down
# 🔺 - Volume Up
# endregion


async def gen_queue(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    buttons = [
        {'label': 'Repeat Queue', 'emoji': hikari.Emoji.parse('🔁')},
        {'label': 'Shuffle', 'emoji': hikari.Emoji.parse('🔀')},
        {'label': 'Stop Music', 'emoji': hikari.Emoji.parse('⏹️')},
    ]

    for btn in buttons:
        if buttons.index(btn) == 2:
            # start second row after second btn added
            rows.append(row)
            row = bot.rest.build_action_row()

        (
            # Adding the buttons into the action row.
            row.add_button(
                hikari.ButtonStyle.SECONDARY,
                # Set the buttons custom ID to the label.
                btn['label'],
            )
            # set emoji
            .set_emoji(btn['emoji'])
            # Set what user sees.
            .set_label(btn['label'])
            # Add the button to the container.
            .add_to_container()
        )

    # Append the second action row to rows after the for loop.
    rows.append(row)

    # Return the action rows from the function.
    return rows


async def gen_np(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    buttons = [
        {'label': 'Pause', 'emoji': hikari.Emoji.parse('⏸️')},
        {'label': 'Play', 'emoji': hikari.Emoji.parse('▶️')},
        {'label': 'Skip', 'emoji': hikari.Emoji.parse('⏭️')},
        {'label': 'Repeat Song', 'emoji': hikari.Emoji.parse('🔂')},
    ]

    for btn in buttons:
        if buttons.index(btn) == 2:
            # start second row after second btn added
            rows.append(row)
            row = bot.rest.build_action_row()

        (
            # Adding the buttons into the action row.
            row.add_button(
                hikari.ButtonStyle.SECONDARY,
                # Set the buttons custom ID to the label.
                btn['label'],
            )
            # set emoji
            .set_emoji(btn['emoji'])
            # Set what user sees
            .set_label(btn['label'])
            # Add the button to the container.
            .add_to_container()
        )

    # Append the second action row to rows after the for loop.
    rows.append(row)

    # Return the action rows from the function.
    return rows

# region Queue Embed
async def create_queueMixer(guildID, update=False, channelID=0):
    # Generate the action rows.
    rows = await gen_queue(mixerPL.bot)

    embedTitle = 'Next 5 Songs'

    guild = await mixerPL.bot.rest.fetch_guild(guildID)

    inVC = mixerPL.bot.cache.get_voice_state(guildID, mixerPL.bot.cache.get_me())

    if inVC is not None:
        node = await lavalink.get_guild_node(guildID)

        embedDescription = ''
        for n, i in enumerate(node.queue):
            if n > 0:
                if n < 6:
                    embedDescription += f"**{n}** - [{i.title}]({i.uri}) \n\u1CBC\u1CBC Requested by: {hikari.Guild.get_member(guild, int(i.requester)).mention}\n\u1CBC\u1CBC\n"
                else:
                    break

        if embedDescription == '':
            embedDescription = 'Queue Is Empty'

        if update:
            return hikari.Embed(title=embedTitle, description=embedDescription)

        return await mixerPL.bot.rest.create_message(channelID,
                                                     embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                                     components=rows)
    else:
        embedDescription = 'Not in VC'
        if update:
            return hikari.Embed(title=embedTitle, description=embedDescription)
        return await mixerPL.bot.rest.create_message(channelID,
                                                     embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                                     components=rows)


# endregion


# region Now Playing Embed
async def create_npMixer(guildID, update=False):
    rows = await gen_np(mixerPL.bot)
    embedTitle = 'Now Playing'
    embedDescription = ''

    guild = await mixerPL.bot.rest.fetch_guild(guildID)

    inVC = guild.get_voice_state(mixerPL.bot.get_me())
    if inVC is not None:
        node = await lavalink.get_guild_node(guildID)
        if not node.queue:
            embedDescription = "Nothing Currently Playing"
        else:

            embedDescription = f"[{node.queue[0].title}]({node.queue[0].uri}) requested by: {hikari.Guild.get_member(guild, int(node.queue[0].requester)).mention}\n"

    else:
        embedDescription = 'Not in a VC'

    guildItems = readWrite.readGuildFile(guildID)
    channelID = guildItems["channelID"]
    if update:
        return hikari.Embed(title=embedTitle, description=embedDescription)
    return await mixerPL.bot.rest.create_message(channelID,
                                                 embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                                 components=rows)


# endregion


async def msgUpdate(guildID):
    mixer = readWrite.readGuildFile(guildID)
    msgNpID = mixer["msgNpID"]
    msgQueueID = mixer["msgQueueID"]
    channelID = mixer["channelID"]
    try:

        node = await lavalink.get_guild_node(guildID)
        queue = node.queue

        if queue is not None:

            rows = await gen_np(mixerPL.bot)
            await mixerPL.bot.rest.edit_message(channelID, msgNpID,
                                                embed=await create_npMixer(guildID, True),
                                                components=rows,
                                                )

            rows = await gen_queue(mixerPL.bot)
            print('updating')
            await mixerPL.bot.rest.edit_message(channelID, msgQueueID,
                                                embed=await create_queueMixer(guildID, True),
                                                components=rows,
                                                )

    except Exception as e:
        print(e)
        print('Add no msg logic')
        await sleep(20)
        # await msgUpdate(guildID)

        # maybe "Respond with please run /createmixer"


@mixerPL.command()
@lightbulb.command('createmixer', 'Create messages in mixer channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def create_mixer(ctx: lightbulb.context.Context) -> None:
    msgNp = await create_npMixer(ctx.guild_id)
    msgNpID = msgNp.id
    msgQueue = await create_queueMixer(ctx.guild_id, channelID=ctx.channel_id)

    msgQueueID = msgQueue.id

    readWrite.setGuildFile(ctx.guild_id, msgNpID, msgQueueID, ctx.channel_id)

    await msgUpdate(ctx.guild_id)

    await ctx.respond(content='Created Mixer',
                      # flags=hikari.MessageFlag.EPHEMERAL,
                      delete_after=0
                      )


def load(bot: lightbulb.BotApp):
    bot.add_plugin(mixerPL)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mixerPL)
