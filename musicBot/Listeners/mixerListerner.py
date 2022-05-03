import lightbulb, hikari

from musicBot.Music.musicCommands import lavalink


btnMixer = lightbulb.Plugin("btnMixer")


@btnMixer.listener(hikari.InteractionCreateEvent)
async def on_component_interaction(event: hikari.InteractionCreateEvent) -> None:
    # Filter out all unwanted interactions
    if not isinstance(event.interaction, hikari.ComponentInteraction):
        return

    # print(event.interaction.custom_id)
    # await event.interaction.create_initial_response(content=event.interaction.custom_id, flags=hikari.MessageFlag.EPHEMERAL, response_type=4)  # (1, 4, 5, 6, 7, 8, 9)
    # await event.interaction.message.respond(content=event.interaction.custom_id)

    guildID = event.interaction.guild_id
    guild = await event.interaction.app.rest.fetch_guild(guildID)
    # test.get_voice_state()

    # inVC = guild.get_voice_state(event.interaction.guild_id)  # , btnMixer.bot.get_me()
    inVC = guild.get_voice_state(btnMixer.bot.get_me())  # , btnMixer.bot.get_me()
    # testB = event.app.

    # print(inVC)

    if inVC is not None:
        node = await lavalink.get_guild_node(guildID)

        match event.interaction.custom_id:
            case 'Pause':
                print('Pause')
                await lavalink.pause(guildID, True)
                await event.interaction.create_initial_response(content='Paused The Music',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
                # await ctx.respond("The music is paused now")
                # lavalink.pause(event.interaction.guild_id)
            case 'Play':
                print('Resume')
                await lavalink.pause(guildID, False)
                await event.interaction.create_initial_response(content='Resumed The Music',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Skip':
                print('Skip')
                stats = False if node.repeat else True
                # print(stats)
                if stats:
                    await lavalink.repeat(guildID, False)
                await lavalink.skip(guildID)
                await event.interaction.create_initial_response(content='Skipped Song',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Repeat Song':
                node = await lavalink.get_guild_node(guildID)
                stats = False if node.repeat else True
                await lavalink.repeat(guildID, stats)
                if stats:
                    await event.interaction.create_initial_response(content='Repeating Song',
                                                                    flags=hikari.MessageFlag.EPHEMERAL,
                                                                    response_type=4
                                                                    )
                    return
                await event.interaction.create_initial_response(content='No Longer Repeating Song',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Loop Queue':
                print('Add logic to loop queue')
                await event.interaction.create_initial_response(content='Not Yet Implemented',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Shuffle':
                await lavalink.shuffle(guildID)
                await event.interaction.create_initial_response(content='Shuffled Queue\nDo /queue to see new queue',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
            case 'Stop':
                queue = await lavalink.queue(guildID)
                if len(queue) > 0:
                    await lavalink.stop(guildID)
                await btnMixer.bot.update_voice_state(guildID, None)
                await event.interaction.create_initial_response(content='Music Stopped\nAnd Cleared Queue',
                                                                flags=hikari.MessageFlag.EPHEMERAL,
                                                                response_type=4
                                                                )
                # await ctx.respond("Left the voice channel")
    else:
        await event.interaction.create_initial_response(content='Bot not in VC',
                                                        flags=hikari.MessageFlag.EPHEMERAL,
                                                        response_type=4
                                                        )
        # await ctx.respond(content='Bot not in a VC')


def load(bot: lightbulb.BotApp):
    bot.add_plugin(btnMixer)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(btnMixer)
