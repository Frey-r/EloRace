import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from elorace.routers import player as player_router
from elorace.routers import summoner as summoner_router
from elorace.logger_config import get_logger


logger = get_logger(__name__)

class PlayerCommands(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="join", description="Register as a player")
    async def register(self, interaction: discord.Interaction):  
        """Register a new player"""
        logger.info(f"Registering player {interaction.user.name}")
        try:
            player_user = interaction.user.name
            player_mail = interaction.user.email if hasattr(interaction.user, 'email') else None
            player_data = {
                "name": player_user,
                "correo": player_mail  
            }
            response = await player_router.register_player(player_data)
            logger.info(f"Player {response.name} registered successfully")
            await interaction.response.send_message(f"Player {response.name} registered successfully")
        except Exception as e:
            logger.error(f"Error registering player: {e}")
            await interaction.response.send_message("Error registering player", ephemeral=True)
    
    @app_commands.command(name="register_invocator", description="Register a summoner")
    @app_commands.describe(
        summoner_name="Summoner name",
        summoner_name_code="Region code without '#' (e.g., LAS)",
    )
    async def register_summoner(
        self, 
        interaction: discord.Interaction, 
        summoner_name: str, 
        summoner_name_code: str
    ):
        await interaction.response.send_message(
            f"Registering summoner {summoner_name}#{summoner_name_code}...",
            ephemeral=True
        )
        logger.info(f"Register summoner command called for {summoner_name}#{summoner_name_code}")

async def setup(bot):  # Función necesaria para cargar el cog
    await bot.add_cog(PlayerCommands(bot))

