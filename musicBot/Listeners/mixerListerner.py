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

    inVC = guild.get_voice_state(event.interaction.guild_id)  # , btnMixer.bot.get_me()
    inVC = guild.get_voice_state(btnMixer.bot.get_me())  # , btnMixer.bot.get_me()
    # testB = event.app.

    print(inVC)

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


# ROLES = [{"rolename": "Test 1", "roleid": 966826632448999464},
    #          {"rolename": "Test 2", "roleid": 966826674257797260},
    #          {"rolename": "Test 3", "roleid": 966826707724173323},
    #          ]
    # guildID = event.interaction.guild_id
    #
    # member = event.interaction.member
    #
    # memRoles = member.get_roles()
    # btnID = event.interaction.custom_id
    #
    # memRoleIDS = []
    #
    # for role in memRoles:
    #     memRoleIDS.append(role.id)
    #
    # print('\n')
    # for role in ROLES:
    #     print(f"{role['rolename'] == btnID}")
    #
    #     if role["rolename"] == btnID:
    #         await btnRoleListPL.bot.rest.add_role_to_member(guildID, member.user.id, role["roleid"])
    #         await event.interaction.create_initial_response(
    #             hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
    #             f"Set State to {btnID} {member.user.username}#{member.user.discriminator}",
    #             # Message content
    #             flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
    #         )
    #     else:
    #         await btnRoleListPL.bot.rest.remove_role_from_member(guildID, member.user.id, role["roleid"])
    #         # await event.interaction.create_initial_response(
    #         #     hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
    #         #     f"Added role {role['rolename']} to {member.user.username}#{member.user.discriminator}",
    #         #     # Message content
    #         #     flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
    #         # )
    #
    #
    # # print(btnID)
    # # if btnID == 'Test 1':
    # #     # print(messageID)
    # #
    # #     guildID = event.interaction.guild_id
    # #
    # #     member = event.interaction.member
    # #
    # #     memRoles = member.get_roles()
    # #     roleIDs = []
    # #     for role in memRoles:
    # #         roleIDs.append(role.id)
    # #
    # #     if 966826632448999464 in roleIDs:
    # #         # await btnRolePL.bot.rest.add_role_to_member(event.interaction.guild_id, member.user.id, 966826632448999464)
    # #         await btnRoleListPL.bot.rest.remove_role_from_member(guildID, member.user.id, 966826632448999464)
    # #         await event.interaction.create_initial_response(
    # #             hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
    # #             f"Removed role Test 1 to {member.user.username}#{member.user.discriminator}",
    # #             # Message content
    # #             flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
    # #         )
    # #     else:
    # #         await btnRoleListPL.bot.rest.add_role_to_member(guildID, member.user.id, 966826632448999464)
    # #         await event.interaction.create_initial_response(
    # #             hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
    # #             f"Added role Test 1 to {member.user.username}#{member.user.discriminator}",
    # #             # Message content
    # #             flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
    # #         )
    # #
    # #     # btnRolePL.bot.rest.create
    #
    #
    # # await plugin.bot.rest.edit_message(966725529652834314, 969061172169035836, content=f"{member.user.username}#{member.user.discriminator} Clicked a button: {event.interaction.custom_id}")
    #
    # # print(event.interaction)
    # # print(f"{member.user.username}#{member.user.discriminator}")
    #
    # # if event.interaction.custom_id == "White":
    # # await event.interaction.create_initial_response(
    # #     hikari.ResponseType.MESSAGE_CREATE,  # Create a new message as response to this interaction
    # #     f"{member.user.username}#{member.user.discriminator} Clicked a button: {event.interaction.custom_id}",  # Message content
    # #     flags=hikari.MessageFlag.EPHEMERAL  # Ephemeral message, only visible to the user who pressed the button
    # # )