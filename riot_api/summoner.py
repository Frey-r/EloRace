from fastapi import HTTPException
import requests
import json
import riot_api.riot_client as rc
from elorace.logger_config import get_logger


logger = get_logger(__name__)
client = rc.RiotClient()

def get_summoner_uid(summoner_name,summoner_name_code):
    logger.info(f"Getting summoner {summoner_name} #{summoner_name_code} UID")
    summoner_url = f"{client.base_url}account/v1/accounts/by-riot-id/{summoner_name}/{summoner_name_code}"
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

