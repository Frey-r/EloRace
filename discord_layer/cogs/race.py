import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from elorace.logger_config import get_logger
from elorace.database import SessionLocal
from elorace.models import race as race_model, summoner as summoner_model, player as player_model
from elorace.schemas import RaceCreate, RaceUpdate, RaceList, EloUpdate
from riot_api.summoner import get_summoner_elo
from datetime import datetime


logger = get_logger(__name__)

class RaceCommands(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="new_race", description="Register a new race")
    @app_commands.describe(
        race_name="Race name",
        objective="Race objective"
    )
    async def new_race(
        self, 
        interaction: discord.Interaction, 
        race_name: str, 
        objective: int
    ):
        logger.info(f"Register race command called for {race_name}")
        user_id = interaction.user.id
        with SessionLocal() as db:
            db_player = db.query(player_model).filter(
                (player_model.source_id == user_id)
                & (player_model.source == 'DISCORD')
            ).first()
            if not db_player:
                logger.error("Player not found")
                await interaction.response.send_message("you need being registered as a player to register a race, try /join instead")
                return
            db_race = db.query(race_model).filter(
                (race_model.name == race_name)
            ).first()
            if db_race:
                logger.info("Race already exists")
                await interaction.response.send_message("Race already exists")
                return
            new_race = race_model(
                name=race_name,
                objective=objective,
                owner=db_player.id,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(new_race)
            db.commit()
            db.refresh(new_race)
            logger.info(f"Race {new_race.name} registered successfully")
            await interaction.response.send_message(f"Race {new_race.name} registered successfully")
            return

async def setup(bot): 
    await bot.add_cog(RaceCommands(bot))
