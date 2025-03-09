from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from elorace.logger_config import get_logger

logger = get_logger(__name__)

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URL = "sqlite:///./elo_race.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_and_update_tables():
    logger.info("Checking database schema for updates")
    inspector = inspect(engine)
    
    try:
        import models  
        defined_tables = Base.metadata.tables
        
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
