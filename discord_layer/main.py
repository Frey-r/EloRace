import discord
from discord.ext import commands
from elorace.logger_config import get_logger
from dotenv import load_dotenv
from config import Config
import os
import sys


logger = get_logger(__name__)
load_dotenv()

class EloRaceBot(commands.Bot):
    def __init__(self, config: Config):
        super().__init__(
            command_prefix=config.bot_prefix,
            intents=config.intents,
            application_id=config.application_id
        )
        self.config = config
        
    async def setup_hook(self):
        """Se ejecuta antes de que el bot se conecte"""
        logger.info("Setting up bot...")
        try:
            await self.load_extension("discord_layer.cogs.summoner")
            logger.info("Summoner cog loaded successfully")
            await self.load_extension("discord_layer.cogs.player")
            logger.info("Player cog loaded successfully")
        except Exception as e:
            logger.error(f"Error loading player cog: {e}")
            raise
        
    async def on_ready(self):
        """Se ejecuta cuando el bot está conectado y listo"""
        logger.info(f"Logged in as {self.user.name}")
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Discord API version: {discord.__version__}")
        
        await self.tree.sync()
        logger.info("Slash commands synced")
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="/help for commands"
            )
        )
        
    async def on_command_error(self, ctx, error):
        """Manejo global de errores de comandos"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            logger.error(f"Error executing command: {error}")
            await ctx.send(f"An error occurred: {str(error)}")

async def main():
    config = Config()
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    bot = EloRaceBot(config)
    try:
        async with bot:
            await bot.start(config.bot_token)
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == "__main__":
    import asyncio
    
    logger.info("Starting discord bot")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
