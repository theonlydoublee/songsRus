from dotenv import load_dotenv
import lightbulb, os


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




    bot.load_extensions_from("./musicBot/Commands")
    # bot.load_extensions_from("./musicBot/Tasks")
    bot.load_extensions_from("./musicBot/Listeners")
    # bot.load_extensions_from("./musicBot/ButtonRoles")
    bot.load_extensions_from("./musicBot/Music")

    # Loads tasks and autostart tasks will start
    # tasks.load(bot)
    return bot

    # listen for on started, reset all mixers for each guild


if __name__ == "__main__":
    print("USING MAIN")
    lavalink.connect()
    create_bot().run()
