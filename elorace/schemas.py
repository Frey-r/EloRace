from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


#SUMMONER SCHEMAS
class SummonerBase(BaseModel):
    name : str
    name_code : str
    region_id : int
    player_id : Optional[int] = None
    race_id : Optional[int] = None
    updated_at : datetime = Field(default_factory=datetime.now)

class SummonerCreate(SummonerBase):
    current_elo : int = Field(default=0)
    higest_elo : int = Field(default=0)
    created_at : datetime = Field(default_factory=datetime.now)


class SummonerResponse(SummonerBase):
    current_elo: int
    higest_elo: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Permite convertir modelos SQLAlchemy a Pydantic

class SummonerUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    name_code: Optional[str] = Field(default=None)
    region_id: Optional[int] = Field(default=None)
    player_id: Optional[int] = Field(default=None)
    race_id: Optional[int] = Field(default=None)
    current_elo: Optional[int] = Field(default=None)
    higest_elo: Optional[int] = Field(default=None)

class EloUpdate(BaseModel):
    id: int
    current_elo: int


#PLAYER SCHEMAS
class PlayerBase(BaseModel):
    name : str
    correo : Optional[str] = Field(default=None)
    updated_at : datetime = Field(default_factory=datetime.now)

class PlayerCreate(PlayerBase):
    created_at : datetime = Field(default_factory=datetime.now)

class PlayerResponse(PlayerBase):
    created_at: datetime 
    updated_at: datetime

    class Config:
        orm_mode = True  # Permite convertir modelos SQLAlchemy a Pydantic

#RACE SCHEMAS
class RaceBase(BaseModel):
    name : str
    objective : int
    updated_at : datetime = Field(default_factory=datetime.now)

class RaceCreate(RaceBase):
    created_at : datetime = Field(default_factory=datetime.now)
    is_active : bool = Field(default=True)

class RaceResponse(RaceBase):
    created_at: datetime
    class Config:
        orm_mode = True  # Permite convertir modelos SQLAlchemy a Pydantic
    
class RaceUpdate(BaseModel):
    id: int
    name: Optional[str] 
    objective: Optional[str] 
    is_active: Optional[bool] 
    updated_at: datetime = Field(default_factory=datetime.now)

class RaceList(BaseModel):
    races: list[str]
    class Config:
        orm_mode = True

