import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from elorace.logger_config import get_logger
from elorace.database import SessionLocal
from elorace.models import summoner as summoner_model, player as player_model
from elorace.schemas import SummonerCreate, SummonerUpdate
from riot_api.summoner import get_summoner_uid, get_summoner_elo
from datetime import datetime


logger = get_logger(__name__)

class SummonerCommands(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="new_summoner", description="Register a summoner")
    @app_commands.describe(
        summoner_name="Summoner name",
        summoner_name_code="Region code without '#' (e.g., LAS)",
    )
    async def new_summoner(
        self, 
        interaction: discord.Interaction, 
        summoner_name: str, 
        summoner_name_code: str
    ):
        logger.info(f"Register summoner command called for {summoner_name}#{summoner_name_code}")
        user_id = interaction.user.id
        with SessionLocal() as db:
            db_player = db.query(player_model).filter(
                (player_model.source_id == user_id)
                & (player_model.source == 'DISCORD')
            ).first()
            if not db_player:
                logger.error("Player not found")
                await interaction.response.send_message("you need being registered as a player to register a summoner, try /join instead")
                return
            db_summoner = db.query(summoner_model).filter(
                (summoner_model.name == summoner_name)
                & (summoner_model.name_code == summoner_name_code)
            ).first()
            if db_summoner:
                logger.info("Summoner already exists")
                await interaction.response.send_message("Summoner already exists")
                return
            summoner_uid = get_summoner_uid(summoner_name,summoner_name_code)
            if not summoner_uid:
                logger.error("Summoner not found")
                await interaction.response.send_message(f"Summoner {summoner_name} not found in RIOT")
                return
            new_summoner = summoner_model(
                puuid=summoner_uid,
                name=summoner_name,
                player_id=db_player.id,
                name_code=summoner_name_code,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(new_summoner)
            db.commit()
            db.refresh(new_summoner)
            logger.info(f"Summoner {new_summoner.name} registered successfully")
            try:
                summoner_elo = get_summoner_elo(
                    summoner_name=summoner_name,
                    summoner_name_code=summoner_name_code
                )
                if summoner_elo:
                    new_summoner.current_elo = summoner_elo
                    new_summoner.higest_elo = summoner_elo
                    new_summoner.updated_at = datetime.now()
                    db.commit()
                    logger.info(f"Summoner {new_summoner.name} ELO updated to {summoner_elo}")
                    await interaction.response.send_message(f"Summoner successfully updated")
                    return
            except Exception as e:
                db.rollback()
                logger.error(f"Error registering summoner: {str(e)}")
                await interaction.response.send_message(f"Error registering summoner")
                return
            
async def setup(bot): 
    await bot.add_cog(SummonerCommands(bot))
