import asyncio

import lightbulb, hikari

from musicBot.Music.musicCommands import lavalink
from musicBot.Music.mixer import msgUpdate


btnMixer = lightbulb.Plugin("btnMixer")


@btnMixer.listener(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    # Filter out all unwanted interactions
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return

    guildID = event.interaction.guild_id
    guild = await event.interaction.app.rest.fetch_guild(guildID)

    inVC = guild.get_voice_state(btnMixer.bot.get_me())  # , btnMixer.bot.get_me()

    if inVC is not None:
        node = await lavalink.get_guild_node(guildID)

        # region Match Case
        match event.interaction.custom_id:
            case 'Pause':
                print('Pause')
                await lavalink.pause(guildID, True)
                await event.interaction.create_initial_response(content='> Paused',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )

            case 'Play':
                print('Resume')
                await lavalink.pause(guildID, False)
                await event.interaction.create_initial_response(content='> Resumed The Music',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Skip':
                print('Skip')
                stats = False if node.repeat else True
                if stats:
                    await lavalink.repeat(guildID, False)
                await lavalink.skip(guildID)
                await event.interaction.create_initial_response(content='> Skipped Song',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Repeat Song':
                node = await lavalink.get_guild_node(guildID)
                stats = False if node.repeat else True
                await lavalink.repeat(guildID, stats)
                if stats:
                    await event.interaction.create_initial_response(content='> Repeating Song',
                                                                    flags=hikari.MessageFlag.EPHEMERAL,
                                                                    response_type=4
                                                                    )
                    return
                await event.interaction.create_initial_response(content='> No Longer Repeating Song',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Repeat Queue':
                print('Add logic to loop queue')
                await event.interaction.create_initial_response(content='> Not Yet Implemented',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Shuffle':
                await lavalink.shuffle(guildID)
                await msgUpdate(guildID)

                await event.interaction.create_initial_response(content='> Shuffled Queue',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
                await asyncio.sleep(20)

            case 'Stop Music':
                queue = await lavalink.queue(guildID)
                if len(queue) > 0:
                    await lavalink.stop(guildID)

                await msgUpdate(guildID)

                await event.interaction.create_initial_response(content='Music Stopped\nAnd Cleared Queue',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
                await asyncio.sleep(20)

    else:
        await event.interaction.create_initial_response(content='Bot not in VC',
                                                        flags=hikari.MessageFlag.EPHEMERAL,
                                                        response_type=4
                                                        )


def load(bot: lightbulb.BotApp):
    bot.add_plugin(btnMixer)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(btnMixer)
