from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import requests
import json
import riot_api.riot_client as rc
from elorace.logger_config import get_logger
from elorace.database import SessionLocal
from elorace.models import summoner as summoner_model
from elorace.models import elos as elos_model
from contextlib import contextmanager


logger = get_logger(__name__)
client = rc.RiotClient()

@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_summoner_uid(summoner_name,summoner_name_code):
    logger.info(f"Getting summoner {summoner_name} #{summoner_name_code} UID")
    summoner_url = f"{client.base_url_americas}account/v1/accounts/by-riot-id/{summoner_name}/{summoner_name_code}"
    response = requests.get(summoner_url, headers=client.headers)
    try:
        response_content = response.json()
        if response.status_code == 200:
            summoner_uid = response_content["puuid"]
            logger.info(f"Summoner {summoner_name} #{summoner_name_code} - UID: {summoner_uid}")
            return summoner_uid
        else:
            logger.error(f"Error getting summoner {summoner_name}: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error getting summoner {summoner_name}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f'Error getting summoner {summoner_name}: no se ha podido procesar la respuesta de RIOT')

def get_summoner_elo(summoner_puuid=None, summoner_name=None, summoner_name_code=None):
    with get_db_context() as db:
        if summoner_puuid:
            db_summoner = db.query(summoner_model).filter(
                (summoner_model.puuid == summoner_puuid)
            ).first()
        else:
            db_summoner = db.query(summoner_model).filter(
                (summoner_model.name == summoner_name)
                & (summoner_model.name_code == summoner_name_code)
            ).first()
        
        if not db_summoner:
            logger.error("Summoner not found")
            return None
        
        summoner_data_url = f'{client.base_url_las2}lol/league/v4/entries/by-puuid/{db_summoner.puuid}'
        summoner_data = requests.get(summoner_data_url, headers=client.headers)
        
        try:
            summoner_data_content = summoner_data.json()
            if summoner_data.status_code == 200:
                summoner_elo_solo = summoner_data_content[0]
                summoner_elo_base = db.query(elos_model).filter(
                    (elos_model.tier == summoner_elo_solo["tier"])
                    & (elos_model.rank == summoner_elo_solo["rank"])
                ).first()
                summoner_elo = int(summoner_elo_base.elo) + int(summoner_elo_solo["leaguePoints"])
                db_summoner.current_elo = summoner_elo
                try:
                    if summoner_elo>db_summoner.higest_elo:
                        db_summoner.higest_elo = summoner_elo
                except Exception as e:
                    pass
                try:
                    db.commit()
                    db.refresh(db_summoner)
                    logger.info(f"Summoner {db_summoner.name} updated successfully")
                    return db_summoner.current_elo
                except Exception as e:
                    db.rollback()
                    logger.error(f"Error getting summoner elo: {str(e)}")
                    return None
            else:
                logger.error(f"Error getting summoner elo {summoner_name}: {summoner_data.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return None
        