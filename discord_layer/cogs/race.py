import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from elorace.logger_config import get_logger
from elorace.database import SessionLocal
from elorace.models import race as race_model, summoner as summoner_model, player as player_model
from elorace.schemas import RaceCreate, RaceUpdate, RaceList, EloUpdate, EloRaceBase
from riot_api.summoner import get_summoner_elo
from discord_layer.views.embeds import create_race_embed, race_state_embed
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
            embed = discord.Embed(
                title=f"Race {new_race.name} created",
                description=f"Objective ELO: {new_race.objective}\nTo win, you need to get {new_race.objective} of ELO, good luck! \nUse /join_race {new_race.name} to join the race",
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed)
            await self.join_race(interaction, new_race.name)
            return
        
    @app_commands.command(name="join_race", description="Join a race")
    @app_commands.describe(
        race_name="Race name"
    )
    async def join_race(
        self, 
        interaction: discord.Interaction, 
        race_name: str
    ):
        logger.info(f"Joining race command called for {race_name}")
        user_id = interaction.user.id
        with SessionLocal() as db:
            db_player = db.query(player_model).filter(
                (player_model.source_id == user_id)
                & (player_model.source == 'DISCORD')
            ).first()
            if not db_player:
                logger.error("Player not found")
                await interaction.response.send_message("you need being registered as a player to join a race, try /join instead")
                return
            db_race = db.query(race_model).filter(
                (race_model.name == race_name)
            ).first()
            if not db_race:
                logger.error("Race not found")
                await interaction.response.send_message("Race not found")
                return
            if not db_race.is_active:
                logger.error("Race is not active")
                await interaction.response.send_message("Race is not active")
                return
            db_summoner = db.query(summoner_model).filter(
                (summoner_model.player_id == db_player.id)
            ).first()
            if not db_summoner:
                logger.error("Summoner not found")
                await interaction.response.send_message("Summoner not found")
                return
            try:
                summoner_elo = get_summoner_elo(
                    summoner_name=db_summoner.name,
                    summoner_name_code=db_summoner.name_code
                )
                if summoner_elo:
                    db_summoner.current_elo = summoner_elo
                    db_summoner.base_race_elo = summoner_elo
                    db_summoner.race_id = db_race.id
                    db_summoner.updated_at = datetime.now()
                    db.commit()
                    db.refresh(db_summoner)
                    logger.info(f"Summoner {db_summoner.name} ELO updated to {summoner_elo}")
                    await interaction.response.send_message(f"Summoner registered successfully, prepare to race!")
                    return
            except Exception as e:
                db.rollback()
                logger.error(f"Error registering summoner: {str(e)}")
                await interaction.response.send_message(f"Error registering summoner")
                return
            
    @app_commands.command(name="leave_race", description="Leave a race")
    async def leave_race(
        self, 
        interaction: discord.Interaction
    ):
        logger.info(f"Leave race command called")
        user_id = interaction.user.id
        with SessionLocal() as db:
            db_player = db.query(player_model).filter(
                (player_model.source_id == user_id)
                & (player_model.source == 'DISCORD')
            ).first()
            if not db_player:
                logger.error("Player not found")
                await interaction.response.send_message("you need being registered as a player to leave a race, try /join instead")
                return
            db_summoner = db.query(summoner_model).filter(
                (summoner_model.player_id == db_player.id)
            ).first()
            if not db_summoner:
                logger.error("Summoner not found")
                await interaction.response.send_message("Summoner not found")
                return
            db_race = db.query(race_model).filter(
                (race_model.id == db_player.race_id)
            ).first()
            if not db_race:
                logger.error("Race not found")
                await interaction.response.send_message("Race not found")
                return
            db_summoner.race_id = None
            db_summoner.updated_at = datetime.now()
            db.commit()
            db.refresh(db_summoner)
            logger.info(f"Summoner {db_summoner.name} successfully left race")
            await interaction.response.send_message(f"Summoner successfully left race")
            return
        
    @app_commands.command(name="leaderboard", description="Show leaderboard")
    async def leaderboard(
        self, 
        interaction: discord.Interaction
    ):
        logger.info(f"Leaderboard command called")
        user_id = interaction.user.id
        with SessionLocal() as db:
            db_player = db.query(player_model).filter(
                (player_model.source_id == user_id)
                & (player_model.source == 'DISCORD')
            ).first()
            if not db_player:
                logger.error("Player not found")
                await interaction.response.send_message("you need being registered as a player to see the leaderboard, try /join instead")
                return
            db_summoner = db.query(summoner_model).filter(
                (summoner_model.player_id == db_player.id)
            ).first()
            if not db_summoner:
                logger.error("Summoner not found")
                await interaction.response.send_message("Summoner not found")
                return
            db_race = db.query(race_model).filter(
                (race_model.id == db_summoner.race_id)
            ).first()
            if not db_race:
                logger.error("Race not found")
                await interaction.response.send_message("Race not found")
                return
            if db_race.is_active:
                summoners = db.query(summoner_model).filter(
                    (summoner_model.race_id == db_race.id)
                ).all()
                if not summoners:
                    logger.error("Summoners not found")
                    await interaction.response.send_message("Summoners not found")
                    return
                leaderboard = sorted(summoners, key=lambda x: x.current_elo, reverse=True)
                embed = discord.Embed(
                    title=f"Leaderboard for {db_race.name}",
                    description=f"Objective ELO: {db_race.objective}",
                    color=0x00ff00
                )
                for i, summoner in enumerate(leaderboard):
                    embed.add_field(
                        name=f"{i+1}. {summoner.name}",
                        value=f"ELO: {summoner.current_elo}",
                        inline=False
                    )
                await interaction.response.send_message(embed=embed)
                return
            else:
                await interaction.response.send_message("Race is not active")
                return

    
async def setup(bot): 
    await bot.add_cog(RaceCommands(bot))
