import os
import random
import datetime
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import lightbulb, hikari, lavaplayer, logging

# from musicBot.Libs import readWrite, updateMsgs

# the lavalink.jar needs to be run with Java 11 (LTS) or newer
# in main file, import the file and do lavalink.connect() before bot.run()
# from TestBot.Music.Commands import *
lavalink = lavaplayer.LavalinkClient(
    host="localhost",  # Lavalink host
    port=2333,  # Lavalink port
    password="youshallnotpass",  # Lavalink password
    user_id=970888803055181844  # Lavalink bot id
)

musicPL = lightbulb.Plugin("musicPL", description="Everything music", include_datastore=True)
load_dotenv()
SPOTCLIENT_ID = os.getenv("SPOTCLIENT_ID")
SPOTCLIENT_SECRET = os.getenv("SPOTCLIENT_SECRET")


loopQueue = False


# region DEBUG/Event LOGS
@lavalink.listen(lavaplayer.TrackStartEvent)
async def track_start_event(event: lavaplayer.TrackStartEvent):

    # await updateMsgs.msgUpdate(musicPL, event.guild_id)

    # from musicBot.Music.mixer import msgUpdate
    # from musicBot.Music.mixer import msgUpdate
    # await msgUpdate(event.guild_id)

    logging.info(f"start track: {event.track.title}")


@lavalink.listen(lavaplayer.TrackEndEvent)
async def track_end_event(event: lavaplayer.TrackEndEvent):
    # await musicPL.bot.application.

    # updateMsgs.msgUpdate(musicPL, event.guild_id)
    from musicBot.Music.mixer import msgUpdate
    await msgUpdate(event.guild_id)
    # if repeat queue is on, add song to queue
    logging.info(f"track end: {event.track.title}")
    node = lavalink.get_guild_node(event.guild_id)

    if loopQueue:
        print('Added song to end of queue')
        await lavalink.play(event.guild_id, track=event.track)


@lavalink.listen(lavaplayer.WebSocketClosedEvent)
async def web_socket_closed_event(event: lavaplayer.WebSocketClosedEvent):
    logging.error(f"error with websocket {event.reason}")
# endregion


# Run to test if music extension is loaded
# region MUSIC COMMAND
@musicPL.command()
@lightbulb.command("music", "Says 'MUSIC!'", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_music(ctx: lightbulb.context):
    await ctx.respond('MUSIC!', delete_after=3)
# endregion


# Have bot join voice channel the user is in
# region JOIN COMMAND
@musicPL.command()
@lightbulb.command(name="join", description="join voice channel", aliases=["connect"])
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_join(ctx: lightbulb.context.Context):
    # if lavalink.nodes

    # test = lavalink.nodes
    # if len(test) > 0:
    #     for x in test:
    #         if x != ctx.guild_id:
    #             print('creating node')
    #             await lavalink.create_new_node(ctx.guild_id)
    #         print(x)
    # else:
    #     print('creating node')
    #     await lavalink.create_new_node(ctx.guild_id)

    # print(lavalink.nodes)

    states = musicPL.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
    voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
    if not voice_state:
        await ctx.respond("Please join a VC", flags=hikari.MessageFlag.EPHEMERAL)
        return
    channel_id = voice_state[0].channel_id
    await musicPL.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
    # await lavalink.create_new_node(ctx.guild_id)
    await ctx.respond(f"Joined: <#{channel_id}>", flags=hikari.MessageFlag.EPHEMERAL)

    # 5% chance to play rickroll on join
    if random.random() < 0.05:

        await lavalink.play(ctx.guild_id, (await lavalink.auto_search_tracks('Rick Astley - Never Gonna Give You Up (Official Music Video)'))[0], requester=1234)


# endregion


# Leave the voice channel
# region LEAVE COMMAND
@musicPL.command()
@lightbulb.command(name="leave", description="Leave command", aliases=["disconnect"])
@lightbulb.implements(lightbulb.SlashCommand)
async def leave_command(ctx: lightbulb.context.Context):
    # ctx.bot.cache

    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())
    # node = await lavalink.get_guild_node(ctx.guild_id)
    if inVC is not None:
        # try:
        # stop music
        queue = await lavalink.queue(ctx.guild_id)
        if len(queue) > 0:
            await lavalink.stop(ctx.guild_id)
            # await lavalink.destroy(ctx.guild_id)
        await musicPL.bot.update_voice_state(ctx.guild_id, None)
        await ctx.respond("Left the voice channel", flags=hikari.MessageFlag.EPHEMERAL)
        # except:
        #     await musicPL.bot.update_voice_state(ctx.guild_id, None)
        #     await ctx.respond("Left the voice channel", flags=hikari.MessageFlag.EPHEMERAL)

    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# add song to queue
# region PLAY / ADD TO QUEUE COMMAND
@musicPL.command()
@lightbulb.option(name="query", description="query to search", required=True)
# @lightbulb.option(name="source", description="Search location", required=False, choices=['YouTube', 'Spotify'], default='YouTube')
@lightbulb.command(name="play", description="Play command", aliases=["p", "add"])
@lightbulb.implements(lightbulb.SlashCommand)
async def play_command(ctx: lightbulb.context.Context):
    # test = lavalink.nodes
    # if len(test) > 0:
    #     for x in test:
    #         if x != ctx.guild_id:
    #             print('creating node')
    #             await lavalink.create_new_node(ctx.guild_id)
    #         print(x)
    # else:
    #     print('creating node')
    #     await lavalink.create_new_node(ctx.guild_id)

    # print(lavalink.nodes)

    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is None:
        print('joining VC')
        states = musicPL.bot.cache.get_voice_states_view_for_guild(ctx.guild_id)
        voice_state = [state async for state in states.iterator().filter(lambda i: i.user_id == ctx.author.id)]
        if not voice_state:
            await ctx.respond("Please join a VC", flags=hikari.MessageFlag.EPHEMERAL)
            return
        channel_id = voice_state[0].channel_id
        await musicPL.bot.update_voice_state(ctx.guild_id, channel_id, self_deaf=True)
        # await lavalink.create_new_node(ctx.guild_id)
        await ctx.respond(f"Joined: <#{channel_id}>", flags=hikari.MessageFlag.EPHEMERAL)
        # inVC = True

    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        from musicBot.Music.mixer import msgUpdate

        query = ctx.options.query

        if "https://open.spotify.com/playlist" in query:
            sp = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
            playlist_link = f"{query}"
            playlist_URI = playlist_link.split("/")[-1].split("?")[0]
            track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

            embed = hikari.Embed(title="Adding a Playlist to the Queue",
                                 description='Will respond when done\nNote: Will take more time, the longer the playlist', color=0x6100FF)
            msg = await ctx.respond(embed=embed, delete_after=10)

            i = 0

            for track in sp.playlist_tracks(playlist_URI)["items"]:
                inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())
                if inVC is None:
                    return
                track_name = track["track"]["name"]
                track_artist = track["track"]["artists"][0]["name"]
                queryfinal = f"{track_name} " + " " + f"{track_artist}"
                result = f"ytmsearch:{queryfinal}"
                query_information = await lavalink.get_tracks(result)
                # print(result)
                # print(query_information)
                # print(f"Song: {query_information[0]}")
                try:
                    await lavalink.play(ctx.guild_id, query_information[0], ctx.author.id)
                    i += 1
                    if i == 6:
                        await msgUpdate(ctx.guild_id)
                except:
                    pass

            if i < 6:
                await msgUpdate(ctx.guild_id)

            embed = hikari.Embed(title="Added the Playlist to Queue",
                                 description='Finished Loading Songs',
                                 color=0x6100FF, timestamp=datetime.datetime.now().astimezone())
            # await musicPL.bot.rest.create_message(ctx.channel_id, embed=embed)
            # await msg.delete()
            await ctx.respond(embed=embed, delete_after=10)
            return

        if "https://open.spotify.com/album" in query:
            sp = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
            album_link = f"{query}"
            album_id = album_link.split("/")[-1].split("?")[0]
            embed = hikari.Embed(title="Adding Album To The Queue", description='Will respond when done\nNote: Will take more time, the longer the playlist', color=0x6100FF)
            msg = await ctx.respond(embed=embed, delete_after=10)

            i = 0
            items = sp.album_tracks(album_id)["items"]
            for track in items:
                inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())
                if inVC is None:
                    return
                track_name = track["name"]
                track_artist = track["artists"][0]["name"]
                queryfinal = f"{track_name} " + f"{track_artist}"
                result = f"ytmsearch:{queryfinal}"
                query_information = await lavalink.get_tracks(result)

                try:
                    await lavalink.play(ctx.guild_id, query_information[0], ctx.author.id)
                    i += 1
                    if i == 6:
                        await msgUpdate(ctx.guild_id)
                except:
                    pass

            if i < 6:
                await msgUpdate(ctx.guild_id)

            embed = hikari.Embed(title="Added the Album to Queue", description=f"Finished Loading Album",
                                 color=0x6100FF, timestamp=datetime.datetime.now().astimezone())
            # await musicPL.bot.rest.create_message(ctx.channel_id, embed=embed)
            # await msg.delete()
            await ctx.respond(embed=embed, delete_after=10)

            return

        if "https://open.spotify.com/track" in query:
            sp = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(client_id=SPOTCLIENT_ID, client_secret=SPOTCLIENT_SECRET))
            track_link = f"{query}"
            track_id = track_link.split("/")[-1].split("?")[0]
            # print(track_id)
            track = f"spotify:track:{track_id}"
            spotifytrack = sp.track(track)
            trackname = spotifytrack['name'] + " " + spotifytrack["artists"][0]["name"]
            result = f"ytmsearch:{trackname}"
            query_information = await lavalink.get_tracks(result)
            # await musicPL.d.lavalink.play(ctx.guild_id, query_information.tracks[0]).requester(ctx.author.id).queue()
            await lavalink.play(ctx.guild_id, query_information[0], ctx.author.id)
            await ctx.respond(content=f'Song added: {trackname}', delete_after=10)
            # embed = hikari.Embed(title="Added Song To The Queue", color=0x6100FF)
            # # await musicPL.bot.rest.delete_m
            # await musicPL.bot.rest.create_message(ctx.channel_id, embed=embed)

            await msgUpdate(ctx.guild_id)
            return

        # region Default Search
        result = await lavalink.auto_search_tracks(f"{query}")  # search for the query
        # result = await lavalink.auto_search_tracks(f"https://www.twitch.tv/giantwaffle")  # search for the query
        if not result:
            await ctx.respond("No results found for your query", delete_after=10)

            # await msgUpdate(ctx.guild_id)
            return

        # Playlist
        if isinstance(result, lavaplayer.PlayList):
            await lavalink.add_to_queue(ctx.guild_id, result.tracks, ctx.author.id)
            # await ctx.respond(f"Added {len(result.tracks)} tracks to queue", delete_after=10)
            await ctx.respond(embed=hikari.Embed(title="Playlist Added", description=f"Playlist added to queue",
                                 color=0x6100FF))
            await msgUpdate(ctx.guild_id)
            return

        await lavalink.play(ctx.guild_id, result[0], ctx.author.id)  # play the first result
        await ctx.respond(embed=hikari.Embed(title='Song Added', description=f" [{result[0].title}]({result[0].uri}) by {result[0].author}"), delete_after=10)  # send the embed
        # await ctx.respond(content='Testing for now')
        # endregion

        await msgUpdate(ctx.guild_id)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Get queue of songs
# region QUEUE COMMAND
@musicPL.command()
@lightbulb.command(name="queue", description="Queue command")
@lightbulb.implements(lightbulb.SlashCommand)
async def queue_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        node = await lavalink.get_guild_node(ctx.guild_id)

        if node is None:
            embedDescription = 'Queue is empty'
            embed = hikari.Embed(title='Queue - Empty',
                                 description=embedDescription
                                 )
            await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
            return
        fullQueue = enumerate(node.queue)

        embedDescription = ''
        for n, i in fullQueue:
            if n > 0:
                if n < 11:
                    embedDescription += f"**{n}** - [{i.title}]({i.uri}) \n\u1CBC\u1CBC Requested by: {hikari.Guild.get_member(ctx.get_guild(), int(i.requester)).mention}\n\u1CBC\u1CBC\n"
                else:
                    break
        embed = hikari.Embed(title='Queue - Next 10',
                             description=embedDescription
                             # description="\n".join(
                             #     [f"{n + 1}- [{i.title}]({i.uri}) requested by: {hikari.Guild.get_member(ctx.get_guild(), int(i.requester)).mention}" for n, i in enumerate(node.queue)])
                             )
        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Stop Player
# region STOP COMMAND
@musicPL.command()
@lightbulb.command(name="stop", description="Stop command", aliases=["s", 'end'], ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def stop_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        await lavalink.stop(ctx.guild_id)
        await ctx.respond("Stopped the player", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Pause Player
# region PAUSE COMMAND
@musicPL.command()
@lightbulb.command(name="pause", description="Pause command")
@lightbulb.implements(lightbulb.SlashCommand)
async def pause_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        await lavalink.pause(ctx.guild_id, True)
        await ctx.respond("The music is paused now", delete_after=10)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Resume Player
# region RESUME COMMAND
@musicPL.command()
@lightbulb.command(name="resume", description="Resume command", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def resume_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())
    if inVC is not None:
        await lavalink.pause(ctx.guild_id, False)
        await ctx.respond("The music is resumed now", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Skip current song
# region SKIP CURRENT SONG
@musicPL.command()
@lightbulb.command(name='skip', description='Skip current song', ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def skip_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        await lavalink.skip(ctx.guild_id)
        await ctx.respond("Skipped current song", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Seek/Skip through song
# region SEEK/SKIP COMMAND
@musicPL.command()
@lightbulb.option(name="position", description="Position to seek", required=True)
@lightbulb.command(name="seek", description="Seek command")
@lightbulb.implements(lightbulb.SlashCommand)
async def seek_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        position = ctx.options.position
        await lavalink.seek(ctx.guild_id, position)
        await ctx.respond(f"Skipped to: {position}", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Now Playing
# region NOW PLAYING COMMAND
@musicPL.command()
@lightbulb.command(name="np", description="Now playing command")
@lightbulb.implements(lightbulb.SlashCommand)
async def np_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        node = await lavalink.get_guild_node(ctx.guild_id)
        if not node.queue:
            await ctx.respond("Nothing Currently Playing", flags=hikari.MessageFlag.EPHEMERAL)
            return
        await ctx.respond(embed=hikari.Embed(title='Now Playing', description=f"[{node.queue[0].title}]({node.queue[0].uri}) by {node.queue[0].author}"), flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Toggle Repeat
# region REPEAT COMMAND
@musicPL.command()
@lightbulb.command(name="repeat", description="Repeat command", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def repeat_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())

    if inVC is not None:
        node = await lavalink.get_guild_node(ctx.guild_id)
        stats = False if node.repeat else True
        await lavalink.repeat(ctx.guild_id, stats)
        if stats:
            await ctx.respond("Now repeating", flags=hikari.MessageFlag.EPHEMERAL)
            return
        await ctx.respond("No longer repeating", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# shuffle the queue
# region SHUFFLE COMMAND
@musicPL.command()
@lightbulb.command(name="shuffle", description="Shuffle command", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def shuffle_command(ctx: lightbulb.context.Context):
    inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())
    from musicBot.Music.mixer import msgUpdate
    if inVC is not None:
        await lavalink.shuffle(ctx.guild_id)
        await msgUpdate(ctx.guild_id)
        await ctx.respond("Shuffled the queue", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# Change Volume (Disabled)
# region VOLUME COMMAND
# @musicPL.command()
# @lightbulb.option(name="vol", description="Volume to set", required=True, min_value=1, max_value=500, type=int)
# @lightbulb.command(name="volume", description="Volume command", ephemeral=True)
# @lightbulb.implements(lightbulb.SlashCommand)
# async def volume_command(ctx: lightbulb.context.Context):
#     inVC = ctx.bot.cache.get_voice_state(ctx.guild_id, musicPL.bot.get_me())
#
#     if inVC is not None:
#         volume = ctx.options.vol
#         await lavalink.volume(ctx.guild_id, volume)
#         await ctx.respond(f"done set volume to {volume}%")
#     else:
#         await ctx.respond(content='Bot not in a VC', flags=hikari.MessageFlag.EPHEMERAL)
# endregion


# On voice state update the bot will update the lavalink node for the Guild
# and disconnect if no people in the VC
# region UPDATE NODE FOR GUILD
@musicPL.listener(hikari.VoiceStateUpdateEvent)
async def voice_state_update(event: hikari.VoiceStateUpdateEvent):
    # await lavalink.raw_voice_state_update(event.guild_id, event.state.user_id, event.state.session_id,
    #                                       event.state.channel_id)

    # check if bot in VC
    if not musicPL.bot.cache.get_voice_state(event.guild_id, musicPL.bot.get_me().id):
        # print('working')
        return  # if the bot is not in the VC, do not check for members in VC

    member = event.state.member
    old = event.old_state
    new = event.state
    if not member.is_bot:
        # Real person just joined
        if not old:
            pass
        # check for changes in the VC
        if (old and new) and old.channel_id != new.channel_id:
            # get the members in the VC
            members = musicPL.bot.cache.get_voice_states_view_for_channel(event.guild_id, old.channel_id)
            if not [m for m in members if not members[m].member.is_bot]:  # if no humans in VC, disconnect
                await lavalink.destroy(event.guild_id)
                await musicPL.bot.update_voice_state(event.guild_id, None)  # disconnect
    await lavalink.raw_voice_state_update(event.guild_id, event.state.user_id, event.state.session_id,
                                          event.state.channel_id)

# endregion


# Do something
# region VoiceServerUpdateEvent
@musicPL.listener(hikari.VoiceServerUpdateEvent)
async def voice_server_update(event: hikari.VoiceServerUpdateEvent):
    await lavalink.raw_voice_server_update(event.guild_id, event.endpoint, event.token)
# endregion


def load(bot: lightbulb.BotApp):
    bot.add_plugin(musicPL)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(musicPL)