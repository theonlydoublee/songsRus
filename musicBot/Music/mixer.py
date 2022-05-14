import typing as t
from asyncio import sleep

import hikari
import lightbulb
from musicBot.Music.musicCommands import lavalink
from hikari.api import ActionRowBuilder

from musicBot.Libs import readWrite  # , updateMsgs

mixerPL = lightbulb.Plugin('mixerPL')


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


async def gen_queue(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    # buttons = ['Loop Queue', 'Clear Queue']
    buttons = [
        {'label': 'Repeat Queue', 'emoji': hikari.Emoji.parse('🔁')},
        {'label': 'Shuffle', 'emoji': hikari.Emoji.parse('🔀')},
        {'label': 'Stop Music', 'emoji': hikari.Emoji.parse('⏹️')},
    ]

    for btn in buttons:

        if buttons.index(btn) == 2:  # and buttons.index(btn) != 0
            # If i is evenly divided by 4, and not 0 we want to
            # append the first row to rows and build the second
            # action row. (Gives a more even button layout)
            rows.append(row)
            row = bot.rest.build_action_row()

        (
            # Adding the buttons into the action row.
            row.add_button(
                # Gray button style, see also PRIMARY, and DANGER.
                hikari.ButtonStyle.SECONDARY,
                # Set the buttons custom ID to the label.
                btn['label'],
            )
                # set emoji
                .set_emoji(btn['emoji'])
                # Set the actual label.
                .set_label(btn['label'])
                # Finally add the button to the container.
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

    # Here we iterate len(COLORS) times.

    # buttons = ['Pause', 'Resume', 'Skip', 'Repeat']
    buttons = [
        {'label': 'Pause', 'emoji': hikari.Emoji.parse('⏸️')},
        {'label': 'Play', 'emoji': hikari.Emoji.parse('▶️')},
        {'label': 'Skip', 'emoji': hikari.Emoji.parse('⏭️')},
        {'label': 'Repeat Song', 'emoji': hikari.Emoji.parse('🔂')},
    ]

    for btn in buttons:

        if buttons.index(btn) == 2:  # and buttons.index(btn) != 0
            # If i is evenly divided by 4, and not 0 we want to
            # append the first row to rows and build the second
            # action row. (Gives a more even button layout)
            rows.append(row)
            row = bot.rest.build_action_row()

        (
            # Adding the buttons into the action row.
            row.add_button(
                # Gray button style, see also PRIMARY, and DANGER.
                hikari.ButtonStyle.SECONDARY,
                # Set the buttons custom ID to the label.
                btn['label'],
            )
                # set emoji
                .set_emoji(btn['emoji'])
                # Set the actual label.
                .set_label(btn['label'])
                # Finally add the button to the container.
                .add_to_container()
        )

    # Append the second action row to rows after the for loop.
    rows.append(row)

    # Return the action rows from the function.
    return rows


# region Vol Btns
# async def gen_vol(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
#     rows: t.List[ActionRowBuilder] = []
#
#     # Build the first action row
#     row = bot.rest.build_action_row()
#
#     # Here we iterate len(COLORS) times.
#
#     # buttons = ['Vol Down', 'Vol Up']
#     buttons = [{'label': 'Vol Down', 'emoji': hikari.Emoji.parse('🔻')}, {'label': 'Vol Up', 'emoji': hikari.Emoji.parse('🔺')}]
#
#     # emoiT = hikari.Emoji.parse(':small_red_triangle_down:')
#
#     for btn in buttons:
#         # print(btn)
#         (
#             # Adding the buttons into the action row.
#             row.add_button(
#                 # Gray button style, see also PRIMARY, and DANGER.
#                 hikari.ButtonStyle.SECONDARY,
#                 # Set the buttons custom ID to the label.
#                 btn['label'],
#             )
#             # set the emoji
#             .set_emoji(btn['emoji'])
#             # Set the actual label.
#             .set_label(btn['label'])
#             # Finally add the button to the container.
#             .add_to_container()
#         )
#
#     # Append the second action row to rows after the for loop.
#     rows.append(row)
#
#     # Return the action rows from the function.
#     return rows
# endregion


# region Base Create Queue
# @mixerPL.command()
# @lightbulb.command("mixerQueue", "Base queue for mixer")
# @lightbulb.implements(lightbulb.SlashCommand)
async def create_queueMixer(guildID, update=False, channelID=0):
    # Generate the action rows.
    # rows = await gen_queue(ctx.bot)
    rows = await gen_queue(mixerPL.bot)

    # Send the initial response with our action rows, and save the

    # await btnRoles.bot.rest.create_message(ctx.channel_id, embed=hikari.Embed(title="Pick a color"), components=rows)

    # queEmbed = hikari.Embed
    embedTitle = 'Next 5 Songs'
    # inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, mixerPL.bot.cache.get_me())
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

        # embedDescription = "\n".join(
        #     [f"{n + 1}- [{i.title}]({i.uri}) requested by: {hikari.Guild.get_member(ctx.get_guild(), int(i.requester)).mention}"
        #         for n, i in enumerate(node.queue)])

        if update:
            return hikari.Embed(title=embedTitle, description=embedDescription)

        return await mixerPL.bot.rest.create_message(channelID,
                                                     embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                                     components=rows)
        # return hikari.Embed(title=embedTitle, description=embedDescription)
    else:
        # queEmbed.title = 'Queue'
        embedDescription = 'Not in VC'
        if update:
            return hikari.Embed(title=embedTitle, description=embedDescription)
        return await mixerPL.bot.rest.create_message(channelID,
                                                     embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                                     components=rows)
        # return hikari.Embed(title=embedTitle, description=embedDescription)
    # await ctx.respond(content="Created Queue Message", delete_after=0)


# endregion


# region Base Now Playing
async def create_npMixer(guildID, update=False):
    rows = await gen_np(mixerPL.bot)
    embedTitle = 'Now Playing'
    embedDescription = ''

    # guild = await event.interaction.app.rest.fetch_guild(guildID)
    guild = await mixerPL.bot.rest.fetch_guild(guildID)

    # inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, mixerPL.bot.cache.get_me())
    inVC = guild.get_voice_state(mixerPL.bot.get_me())
    if inVC is not None:
        node = await lavalink.get_guild_node(guildID)
        if not node.queue:
            embedDescription = "Nothing Currently Playing"
        else:

            # embedDescription = f"{node.queue[0].title} by {node.queue[0].author}"
            embedDescription = f"[{node.queue[0].title}]({node.queue[0].uri}) requested by: {hikari.Guild.get_member(guild, int(node.queue[0].requester)).mention}\n"

            # await ctx.respond(f"{node.queue[0].title} by {node.queue[0].author}")
            # await mixerPL.bot.rest.create_message(ctx.channel_id,
            #                                       embed=hikari.Embed(title=embedTitle, description=embedDescription),
            #                                       components=rows)
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
    # print('Add logic to update messages')

    mixer = readWrite.readGuildFile(guildID)
    msgNpID = mixer["msgNpID"]
    msgQueueID = mixer["msgQueueID"]
    channelID = mixer["channelID"]
    try:

        node = await lavalink.get_guild_node(guildID)
        queue = node.queue

        if queue is not None:

            rows = await gen_np(mixerPL.bot)
            # print(await create_npMixer(guildID))
            await mixerPL.bot.rest.edit_message(channelID, msgNpID,
                                                embed=await create_npMixer(guildID, True),
                                                # embed=hikari.Embed(title="New Title Q", description="New Description Q"),
                                                components=rows,
                                                )

            # await musicPL.bot.rest.edit_message(channelID, msgNpID,
            #                                     embed=create_npMixer())

            rows = await gen_queue(mixerPL.bot)
            print('updating')
            await mixerPL.bot.rest.edit_message(channelID, msgQueueID,
                                                # embed=hikari.Embed(title="New Title Q", description="New Description Q"),
                                                embed=await create_queueMixer(guildID, True),
                                                components=rows,
                                                )

    except Exception as e:
        print(e)
        print('Add no msg logic')
        await sleep(20)
        # await msgUpdate(guildID)

        # maybe "Respond with please run /createmixer"


# region Base Volume

# async def create_volMixer(ctx: lightbulb.context.Context) -> None:
#     rows = await gen_vol(ctx.bot)
#     embedTitle = 'Overall Volume'
#     embedDescription = ''
#     inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, mixerPL.bot.cache.get_me())
#
#     level = await lavalink.get_guild_node(ctx.guild_id)
#     if level is not None:
#         print(level.volume)
#         level = 100
#
#     # print(level)
#
#     embedDescription = '0% <---------|> 100%'
#
#     await mixerPL.bot.rest.create_message(ctx.channel_id,
#                                           embed=hikari.Embed(title=embedTitle, description=embedDescription),
#                                           components=rows)

# endregion

@mixerPL.command()
@lightbulb.command('createmixer', 'Create messages in mixer channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def create_mixer(ctx: lightbulb.context.Context) -> None:
    msgNp = await create_npMixer(ctx.guild_id)
    msgNpID = msgNp.id
    # msgQueue = await create_queueMixer(ctx)
    msgQueue = await create_queueMixer(ctx.guild_id, channelID=ctx.channel_id)

    msgQueueID = msgQueue.id

    readWrite.setGuildFile(ctx.guild_id, msgNpID, msgQueueID, ctx.channel_id)

    await msgUpdate(ctx.guild_id)

    # await create_volMixer(ctx)

    await ctx.respond(content='Created Mixer',
                      # flags=hikari.MessageFlag.EPHEMERAL,
                      delete_after=0
                      )


def load(bot: lightbulb.BotApp):
    bot.add_plugin(mixerPL)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mixerPL)
