from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from elorace.models import race as race_model
from elorace.schemas import RaceCreate, RaceResponse, RaceBase, RaceList, RaceResponse
from elorace.database import SessionLocal
from elorace.logger_config import get_logger
from datetime import datetime


logger = get_logger(__name__)

router = APIRouter(
    prefix="/race",
    tags=["race"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=RaceResponse)
def create_race(race_data: RaceCreate, db: Session = Depends(get_db)):
    db_race = db.query(race_model).filter(
        (race_model.name == race_data.name) & 
        (race_model.objective == race_data.objective)
    ).first()

    if db_race:
        logger.info("Race already exists")
        raise HTTPException(status_code=400, detail="Race already exists")
    
    new_race = race_model(
        name=race_data.name,
        objective=race_data.objective,
        updated_at = datetime.now(),
        created_at = datetime.now(),
        is_active = True
    )

    try:
        db.add(new_race)
        db.commit()
        db.refresh(new_race)
        logger.info(f"Race {new_race.name} created successfully")
        return new_race
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating race: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f'Error creating race: {str(e)}')

@router.post("/update", response_model=RaceResponse)
def update_race(race_data: RaceCreate, db: Session = Depends(get_db)):
    db_race = db.query(race_model).filter(
        race_model.id == race_data.id
    ).first()
    if not db_race:
        raise HTTPException(status_code=404, detail="Race not found")
    
    db_race.name = race_data.name
    db_race.objective = race_data.objective
    db_race.is_active = race_data.is_active
    db_race.updated_at = datetime.now()

    try:
        db.commit()
        db.refresh(db_race)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f'Error updating race: {str(e)}')
    
@router.get('/', response_model=RaceList)
def get_races(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    racesList = []
    try:
        races = db.query(race_model).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(races)} races")
        for race in races:
            racesList.append(race.name)
        return racesList
    
    except Exception as e:
        logger.error(f"Error retrieving races: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving races: {str(e)}"
        )

@router.get("/{race_id}", response_model=RaceResponse)
def get_race(race_id: int, db: Session = Depends(get_db)):
    try:
        race = db.query(race_model).filter(race_model.id == race_id).first()
        if not race:
            logger.error(f"Race {race_id} not found")
            raise HTTPException(status_code=404, detail="Race not found")
        db.refresh(race)
        logger.info(f"Retrieved race {race.name}")
        return race
    except Exception as e:
        logger.error(f"Error retrieving race: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving race: {str(e)}"
        )
    