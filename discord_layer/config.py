import os
import dotenv
from elorace.logger_config import get_logger
import discord


logger = get_logger(__name__)
dotenv.load_dotenv()

class Config:
    def __init__(self):
        self.bot_token = os.getenv("DISCORDAPITOKEN")
        self.bot_prefix = "!"
        self.bot_admins = []
        self.bot_owner = None
        self.bot_channels = []
        self.bot_guilds = []
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.presences = True
        self.intents.typing = True
        self.intents.message_content = True
        self.intents.guilds = True

    