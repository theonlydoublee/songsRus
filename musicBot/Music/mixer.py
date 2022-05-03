import typing as t

import hikari
import lightbulb
from musicBot.Music.musicCommands import lavalink
from hikari.api import ActionRowBuilder

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
        {'label': 'Loop Queue', 'emoji': hikari.Emoji.parse('🔁')},
        {'label': 'Shuffle', 'emoji': hikari.Emoji.parse('🔀')},
        {'label': 'Clear', 'emoji': hikari.Emoji.parse('⏹️')},
    ]

    for btn in buttons:
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
               {'label': 'Skip Single', 'emoji': hikari.Emoji.parse('⏭️')},
               {'label': 'Repeat Song', 'emoji': hikari.Emoji.parse('🔂')},
               ]

    for btn in buttons:
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


async def gen_vol(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    # Here we iterate len(COLORS) times.

    # buttons = ['Vol Down', 'Vol Up']
    buttons = [{'label': 'Vol Down', 'emoji': hikari.Emoji.parse('🔻')}, {'label': 'Vol Up', 'emoji': hikari.Emoji.parse('🔺')}]

    # emoiT = hikari.Emoji.parse(':small_red_triangle_down:')

    for btn in buttons:
        # print(btn)
        (
            # Adding the buttons into the action row.
            row.add_button(
                # Gray button style, see also PRIMARY, and DANGER.
                hikari.ButtonStyle.SECONDARY,
                # Set the buttons custom ID to the label.
                btn['label'],
            )
            # set the emoji
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


# region Base Create Queue
# @mixerPL.command()
# @lightbulb.command("mixerQueue", "Base queue for mixer")
# @lightbulb.implements(lightbulb.SlashCommand)
async def create_queueMixer(ctx: lightbulb.Context) -> None:

    # Generate the action rows.
    rows = await gen_queue(ctx.bot)

    # Send the initial response with our action rows, and save the

    # await btnRoles.bot.rest.create_message(ctx.channel_id, embed=hikari.Embed(title="Pick a color"), components=rows)

    # queEmbed = hikari.Embed
    embedTitle = 'Queue - Next 5'
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, mixerPL.bot.cache.get_me())

    if inVC is not None:
        node = await lavalink.get_guild_node(ctx.guild_id)

        embedDescription = ''
        for n, i in enumerate(node.queue):
            if n < 5:
                embedDescription += f"{n + 1}- [{i.title}]({i.uri}) requested by: {hikari.Guild.get_member(ctx.get_guild(), int(i.requester)).mention}\n"
            else:
                break

        # embedDescription = "\n".join(
        #     [f"{n + 1}- [{i.title}]({i.uri}) requested by: {hikari.Guild.get_member(ctx.get_guild(), int(i.requester)).mention}"
        #         for n, i in enumerate(node.queue)])

        await mixerPL.bot.rest.create_message(ctx.channel_id,
                                              embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                              components=rows)

    else:
        # queEmbed.title = 'Queue'
        embedDescription = 'Not in VC'
        await mixerPL.bot.rest.create_message(ctx.channel_id,
                                              embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                              components=rows)

    # await ctx.respond(content="Created Queue Message", delete_after=0)

# endregion


# region Base Now Playing
async def create_npMixer(ctx: lightbulb.Context) -> None:
    rows = await gen_np(ctx.bot)
    embedTitle = 'Now Playing'
    embedDescription = ''
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, mixerPL.bot.cache.get_me())

    if inVC is not None:
        node = await lavalink.get_guild_node(ctx.guild_id)
        if not node.queue:
            embedDescription = "Nothing Currently Playing"
        else:

            embedDescription = f"{node.queue[0].title} by {node.queue[0].author}"

            # await ctx.respond(f"{node.queue[0].title} by {node.queue[0].author}")
            # await mixerPL.bot.rest.create_message(ctx.channel_id,
            #                                       embed=hikari.Embed(title=embedTitle, description=embedDescription),
            #                                       components=rows)
    else:
        embedDescription = 'Not in a VC'

    await mixerPL.bot.rest.create_message(ctx.channel_id,
                                          embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                          components=rows)
# endregion


# region Base Volume

async def create_volMixer(ctx: lightbulb.context.Context) -> None:
    rows = await gen_vol(ctx.bot)
    embedTitle = 'Overall Volume'
    embedDescription = ''
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, mixerPL.bot.cache.get_me())

    level = await lavalink.get_guild_node(ctx.guild_id)
    if level is not None:
        print(level.volume)
        level = 100

    # print(level)

    embedDescription = '0% <---------|> 100%'

    await mixerPL.bot.rest.create_message(ctx.channel_id,
                                          embed=hikari.Embed(title=embedTitle, description=embedDescription),
                                          components=rows)

# endregion


@mixerPL.command()
@lightbulb.command('createmixer', 'Create messages in mixer channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def create_mixer(ctx: lightbulb.context.Context) -> None:
    await create_npMixer(ctx)
    await create_queueMixer(ctx)
    await create_volMixer(ctx)

    await ctx.respond(content='Created Mixer', flags=hikari.MessageFlag.EPHEMERAL)




def load(bot: lightbulb.BotApp):
    bot.add_plugin(mixerPL)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mixerPL)
