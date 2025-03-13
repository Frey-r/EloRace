from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from elorace.database import Base


class summoner(Base):
    __tablename__ = 'summoners'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    puuid = Column(String(100))
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
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    source_id = Column(String(100))
    source = Column(String(50))
    created_at = Column(Date)
    updated_at = Column(Date)

class region(Base):
    __tablename__ = 'region'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    short_name = Column(String(3))

class race(Base):
    __tablename__ = 'races'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(Integer, ForeignKey('players.id'))
    name = Column(String(50))
    objective = Column(String(50))
    is_active = Column(Boolean)
    created_at = Column(Date)
    updated_at = Column(Date)

class archivement_player(Base):
    __tablename__ = 'archivement_player'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_summoner = Column(Integer, ForeignKey('summoners.id'))
    id_achievement = Column(Integer, ForeignKey('achievments.id'))
    img_link = Column(String(100))
    created_at = Column(Date)

class achievment(Base):
    __tablename__ = 'achievments'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    created_at = Column(Date)
    updated_at = Column(Date)

class elos(Base):
    __tablename__ = 'elos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    tier = Column(String(10))
    rank = Column(String(3))
    elo = Column(Integer)
