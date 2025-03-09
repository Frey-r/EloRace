import discord
from discord.ext import commands
from elorace.logger_config import get_logger
from dotenv import load_dotenv
from config import Config
import os

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
        # Aquí cargarías tus cogs/extensiones
        # await self.load_extension("cogs.admin")
        # await self.load_extension("cogs.player")
        # await self.load_extension("cogs.matches")
        
    async def on_ready(self):
        """Se ejecuta cuando el bot está conectado y listo"""
        logger.info(f"Logged in as {self.user.name}")
        logger.info(f"Bot ID: {self.user.id}")
        logger.info(f"Discord API version: {discord.__version__}")
        
        # Establecer estado del bot
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="!help for commands"
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
    # Crear y validar configuración
    config = Config()
    try:
        config.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    # Crear y ejecutar bot
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
