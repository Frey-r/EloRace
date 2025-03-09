import discord_layer
import logger_config
from dotenv import load_dotenv
import os


logger = logger_config.get_logger(__name__)
load_dotenv()

if __name__ == "__main__":
    logger.info("Starting discord bot")
    if os.getenv("DISCORDAPITOKEN") is None:
        logger.error("Discord token not found")
        exit(1)
