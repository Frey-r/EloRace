from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from elorace.models import player as player_model, summoner as summoner_model
from elorace.schemas import PlayerCreate, PlayerResponse, PlayerBase
from elorace.database import SessionLocal
from elorace.logger_config import get_logger
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter(
    prefix="/player",
    tags=["player"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=PlayerResponse)
def register_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    db_player = db.query(player_model).filter(
        (player_model.name == player_data.name) & 
        (player_model.source == player_data.source) &
        (player_model.source_id == player_data.source_id)
    ).first()
    
    if db_player:
        logger.info("Player already exists")
        raise HTTPException(status_code=400, detail="Player already exists")
    
    new_player = player_model(
        name=player_data.name,
        source_id=player_data.source_id,
        source=player_data.source,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    try:
        db.add(new_player)
        db.commit()
        db.refresh(new_player)
        logger.info(f"Player {new_player.name} registered successfully")
        return new_player
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering player: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f'Error registering player: {str(e)}')