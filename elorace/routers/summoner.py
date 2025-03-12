from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from elorace.models import summoner as summoner_model
from elorace.schemas import SummonerCreate, SummonerResponse, SummonerUpdate, EloUpdate, SummonerBase
from elorace.database import SessionLocal
from elorace.logger_config import get_logger
from riot_api.summoner import get_summoner_uid, get_summoner_elo
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter(
    prefix="/summoner",
    tags=["summoner"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/register", response_model=SummonerResponse)
def register_summoner(summoner_data: SummonerCreate, db: Session = Depends(get_db)):
    # Verificar si existe
    logger.info(f"Registering summoner {summoner_data.name} - {summoner_data.name_code}")
    db_summoner = db.query(summoner_model).filter(
        (summoner_model.name == summoner_data.name) & 
        (summoner_model.name_code == summoner_data.name_code)
    ).first()
    
    if db_summoner:
        logger.info("Summoner already exists")
        raise HTTPException(status_code=400, detail="Summoner already exists")
    
    summoner_puuid = get_summoner_uid(summoner_data.name,summoner_data.name_code)
    if summoner_puuid:
        new_summoner = summoner_model(
        puuid=summoner_puuid,
        name=summoner_data.name,
        name_code=summoner_data.name_code,
        region_id=summoner_data.region_id,
        player_id=summoner_data.player_id,
        race_id=summoner_data.race_id,
        current_elo=summoner_data.current_elo,
        higest_elo=summoner_data.higest_elo,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
        try:
            db.add(new_summoner)
            db.commit()
            db.refresh(new_summoner)
            logger.info(f"Summoner {new_summoner.name} registered successfully")
            return new_summoner
        except Exception as e:
            db.rollback()
            logger.error(f"Error registering summoner: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f'Error registering summoner: {str(e)}')

@router.post("/current_elo", response_model=SummonerResponse)
def update_current_elo(summoner_data:EloUpdate , db: Session = Depends(get_db)):
    db_summoner = db.query(summoner_model).filter(
        (summoner_model.name == summoner_data.name) &
        (summoner_model.name_code == summoner_data.name_code)
    ).first()
    if not db_summoner:
        raise HTTPException(status_code=404, detail="Summoner not found")
    db_summoner.current_elo = get_summoner_elo(summoner_name=summoner_data.name, summoner_name_code=summoner_data.name_code)
    if db_summoner.current_elo>db_summoner.higest_elo:
        db_summoner.higest_elo = db_summoner.current_elo
    db_summoner.updated_at = datetime.now()
    try:
        db.commit()
        db.refresh(db_summoner)
        logger.info(f"Summoner {db_summoner.name} updated successfully")
        return db_summoner
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f'Error updating summoner: {str(e)}')
    
@router.post("/update", response_model=SummonerResponse)
def update_summoner(summoner_data: SummonerUpdate, db: Session = Depends(get_db)):
    db_summoner = db.query(summoner_model).filter(
        summoner_model.id == summoner_data.id
    ).first()
    if not db_summoner:
        raise HTTPException(status_code=404, detail="Summoner not found")
    db_summoner.name = summoner_data.name
    db_summoner.name_code = summoner_data.name_code
    db_summoner.region_id = summoner_data.region_id
    db_summoner.player_id = summoner_data.player_id
    db_summoner.race_id = summoner_data.race_id
    db_summoner.current_elo = summoner_data.current_elo
    db_summoner.higest_elo = summoner_data.higest_elo
    db_summoner.updated_at = datetime.now()
    try:
        db.commit()
        db.refresh(db_summoner)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f'Error updating summoner: {str(e)}')
    
    return db_summoner
    