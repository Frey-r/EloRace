from fastapi import FastAPI
from routers import summoner, player, races
from database import check_and_update_tables, constant_tables
from logger_config import get_logger
from dotenv import load_dotenv
import riot_api.summoner as summoner_api
import os


load_dotenv()
logger = get_logger(__name__)
app = FastAPI()
app.include_router(summoner.router)
app.include_router(player.router)
app.include_router(races.router)
check_and_update_tables()
constant_tables()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    