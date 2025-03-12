import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from elorace.logger_config import get_logger
from elorace.database import SessionLocal
from elorace.models import player as player_model
from elorace.schemas import PlayerCreate


logger = get_logger(__name__)


class PlayerCommands(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="join", description="Register as a player")
    async def register(self, interaction: discord.Interaction):  
        """Register a new player"""
        logger.info(f"Registering player {interaction.user.name}")
        player_user = interaction.user.name
        player_source_id = interaction.user.id
        player_source = 'DISCORD'
        with SessionLocal() as db:
            db_player = db.query(player_model).filter(
                (player_model.name == player_user)
                & (player_model.source_id == player_source_id)
                & (player_model.source == player_source)
            ).first()
            if db_player:
                logger.info("Player already exists")
                await interaction.response.send_message("Player already exists")
                return
            

    
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

