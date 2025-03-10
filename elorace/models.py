from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from database import Base


class summoner(Base):
    __tablename__ = 'summoners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column(String(50))
    name = Column(String(50))
    name_code = Column(String(5))
    region_id = Column(Integer, ForeignKey('region.id'))
    player_id = Column(Integer, ForeignKey('players.id'))
    race_id = Column(Integer, ForeignKey('races.id'))
    current_elo = Column(Integer)
    higest_elo = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)

class player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    correo = Column(String(50))
    created_at = Column(Date)
    updated_at = Column(Date)

class region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    short_name = Column(String(3))

class race(Base):
    __tablename__ = 'races'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    objective = Column(String(50))
    is_active = Column(Boolean)
    created_at = Column(Date)
    updated_at = Column(Date)

class archivement_summoner(Base):
    __tablename__ = 'archivement_races'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_summoner = Column(Integer, ForeignKey('summoners.id'))
    id_achievement = Column(Integer, ForeignKey('achievments.id'))
    img_link = Column(String(100))
    created_at = Column(Date)

class achievment(Base):
    __tablename__ = 'achievments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    created_at = Column(Date)
    updated_at = Column(Date)
