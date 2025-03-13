import discord
from datetime import datetime
from elorace.logger_config import get_logger


PRINCIPAL_COLOR = 0xff510d
SECONDARY_COLOR = 0xfcba03

logger = get_logger(__name__)


def create_race_embed(race,img):
    embed = discord.Embed(
        title=f"{race.name}",
        description=f"{race.objective}",
        color=0xff510d
    )
    embed.set_thumbnail(url=img)
    embed.add_field(
        name="Owner",
        value=f"{race.owner.name}",
        inline=False
    )
    return embed

def race_state_embed(race):
    embed = discord.Embed(
        title=f"{str(race.name).capitalize()}", 
        description=f"Objective elo:{race.objective}",
        color=0xff510d
    )