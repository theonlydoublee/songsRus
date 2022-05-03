import hikari
from lightbulb.ext import tasks
from dotenv import load_dotenv
import lightbulb, os

# https://github.com/parafoxia/hikari-intro/blob/main/lightbulb_bot/__main__.py

# Create a new message
# await pluginName.bot.rest.create_message(ctx.channel_id, "Create New Message")


# import TestBot.Music.musicCommands as M
from musicBot.Music.musicCommands import lavalink


def create_bot() -> lightbulb.BotApp:
    # load TOKEN and GUILDS from .env file
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    bot = lightbulb.BotApp(
        token=TOKEN,
        help_slash_command=True,
    )

    # bot.reload_extensions('TestBot.Music.Commands')

    # bot.load_extensions_from("./TestBot/Commands")
    # bot.load_extensions_from("./TestBot/Tasks")
    # bot.load_extensions_from("./TestBot/Listeners")
    # bot.load_extensions_from("./TestBot/ButtonRoles")
    bot.load_extensions_from("./musicBot/Music")

    # Loads tasks and autostart tasks will start
    # tasks.load(bot)
    return bot


if __name__ == "__main__":
    print("USING MAIN")
    lavalink.connect()
    create_bot().run()
