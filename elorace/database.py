from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from elorace.logger_config import get_logger


logger = get_logger(__name__)

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URL = "sqlite:///./elo_race.db"
#engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_all_models():
    """Retorna todas las clases de modelo definidas."""
    from elorace.models import summoner, player, region, race, archivement_summoner, achievment, elos
    return [summoner, player, region, race, archivement_summoner, achievment, elos]


def check_and_update_tables():
    logger.info("Checking database schema for updates")
    inspector = inspect(engine)
    
    try:  
        models = get_all_models()
        defined_tables = {model.__tablename__: model.__table__ for model in models}
        
        with engine.connect() as connection: 
            for table_name, table in defined_tables.items():
                if not inspector.has_table(table_name):
                    logger.info(f"Creating new table: {table_name}")
                    table.create(engine)
                    continue
                
                existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
                defined_columns = {col.name for col in table.columns}
                new_columns = defined_columns - existing_columns
                
                if new_columns:
                    logger.info(f"Adding new columns to {table_name}: {new_columns}")

                    for col_name in new_columns:
                        column = table.columns[col_name]
                        column_type = column.type.compile(engine.dialect)
                        nullable = "NULL" if column.nullable else "NOT NULL"
                        default = f"DEFAULT {column.default.arg}" if column.default else ""
                        
                        alter_stmt = text(
                            f"ALTER TABLE {table_name} ADD COLUMN {col_name} {column_type} {nullable} {default}"
                        )
                        connection.execute(alter_stmt)
                    
                    connection.commit() 
                    logger.info(f"Successfully added new columns to {table_name}")
            
        logger.info("Database schema update completed successfully")
        
    except Exception as e:
        logger.error(f"Error updating database schema: {str(e)}")
        raise Exception(f"Error updating database schema: {str(e)}")


def constant_tables():
    logger.info("Checking and populating constant tables")
    try:
        db = SessionLocal()
        from elorace.models import elos
        from elorace.models import region

        if db.query(elos).count() == 0:
            logger.info("Populating elos table")
            
            elo_values = [
                # IRON
                {"tier": "IRON", "rank": "IV", "elo": 0},
                {"tier": "IRON", "rank": "III", "elo": 100},
                {"tier": "IRON", "rank": "II", "elo": 200},
                {"tier": "IRON", "rank": "I", "elo": 300},
                
                # BRONZE
                {"tier": "BRONZE", "rank": "IV", "elo": 400},
                {"tier": "BRONZE", "rank": "III", "elo": 500},
                {"tier": "BRONZE", "rank": "II", "elo": 600},
                {"tier": "BRONZE", "rank": "I", "elo": 700},
                
                # SILVER
                {"tier": "SILVER", "rank": "IV", "elo": 800},
                {"tier": "SILVER", "rank": "III", "elo": 900},
                {"tier": "SILVER", "rank": "II", "elo": 1000},
                {"tier": "SILVER", "rank": "I", "elo": 1100},
                
                # GOLD
                {"tier": "GOLD", "rank": "IV", "elo": 1200},
                {"tier": "GOLD", "rank": "III", "elo": 1300},
                {"tier": "GOLD", "rank": "II", "elo": 1400},
                {"tier": "GOLD", "rank": "I", "elo": 1500},
                
                # PLATINUM
                {"tier": "PLATINUM", "rank": "IV", "elo": 1600},
                {"tier": "PLATINUM", "rank": "III", "elo": 1700},
                {"tier": "PLATINUM", "rank": "II", "elo": 1800},
                {"tier": "PLATINUM", "rank": "I", "elo": 1900},
                
                # EMERALD
                {"tier": "EMERALD", "rank": "IV", "elo": 2000},
                {"tier": "EMERALD", "rank": "III", "elo": 2100},
                {"tier": "EMERALD", "rank": "II", "elo": 2200},
                {"tier": "EMERALD", "rank": "I", "elo": 2300},
                
                # DIAMOND
                {"tier": "DIAMOND", "rank": "IV", "elo": 2400},
                {"tier": "DIAMOND", "rank": "III", "elo": 2500},
                {"tier": "DIAMOND", "rank": "II", "elo": 2600},
                {"tier": "DIAMOND", "rank": "I", "elo": 2700},
                
                # MASTER+
                {"tier": "MASTER", "rank": "I", "elo": 2700},
                {"tier": "GRANDMASTER", "rank": "I", "elo": 2700},
                {"tier": "CHALLENGER", "rank": "I", "elo": 2700}
            ]
            
            for elo_data in elo_values:
                db_elo = elos(
                    tier=elo_data["tier"],
                    rank=elo_data["rank"],
                    elo=elo_data["elo"]
                )
                db.add(db_elo)
            
            try:
                db.commit()
                logger.info("Elos table populated successfully")
            except Exception as e:
                db.rollback()
                logger.error(f"Error populating elos table: {str(e)}")
        else:
            logger.info("Elos table already populated")
        
        if db.query(region).count() == 0:
            logger.info("Populating region table")
            Regions = [
                {"name": "north-america", "short_name": "na"},
                {"name": "europe-east", "short_name": "eue"},
                {"name": "europe-west", "short_name": "euw"},
                {"name": "asia", "short_name": "as"},
                {"name": "oceania", "short_name": "oc"},
                {"name": "latin-america-1", "short_name": "lan"},
                {"name": "latin-america-2", "short_name": "las"},
            ]

            for region_data in Regions:
                db_region = region(
                    name=region_data["name"],
                    short_name=region_data["short_name"]
                )
                db.add(db_region)
            
            try:
                db.commit()
                logger.info("Region table populated successfully")
            except Exception as e:
                db.rollback()
                logger.error(f"Error populating region table: {str(e)}")
        else:
            logger.info("Region table already populated")
            
    except Exception as e:
        logger.error(f"Error checking/populating constant tables: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    check_and_update_tables()