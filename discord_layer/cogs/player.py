import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from elorace.logger_config import get_logger
from elorace.database import SessionLocal
from elorace.models import player as player_model
from datetime import datetime


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
            new_player = player_model(
                name=player_user,
                source_id=player_source_id,
                source=player_source,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            try:
                db.add(new_player)
                db.commit()
                db.refresh(new_player)
                logger.info(f"Player {new_player.name} registered successfully")
                await interaction.response.send_message(f"Player {new_player.name} registered successfully")
                return
            except Exception as e:
                db.rollback()
                logger.error(f"Error registering player: {str(e)}")
                await interaction.response.send_message(f"Error registering player: {str(e)}")
                return
            
async def setup(bot): 
    await bot.add_cog(PlayerCommands(bot))
