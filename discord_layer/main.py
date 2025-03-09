import discord_layer
from elorace.logger_config import get_logger
from dotenv import load_dotenv
import os


logger = get_logger(__name__)
load_dotenv()

if __name__ == "__main__":
    logger.info("Starting discord bot")
    if os.getenv("DISCORDAPITOKEN") is None:
        logger.error("Discord token not found")
        exit(1)
