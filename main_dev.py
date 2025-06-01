from pathlib import Path
from dotenv import load_dotenv
from _bot.bot import DiscordBot

if __name__ == "__main__":

    configFound = load_dotenv(Path().absolute() / ".env.development")

    if configFound:
        bot = DiscordBot()
        bot.run()
    else:
        raise Exception("No dev run config found")
