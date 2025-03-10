import requests
from dotenv import load_dotenv
import os
import time
from elorace.logger_config import get_logger


logger = get_logger(__name__)
load_dotenv()

class RiotClient:
    def __init__(self):
        logger.info("Creating Riot client")
        self.base_url = "https://americas.api.riotgames.com/riot/"
        self.token = os.getenv("RIOTAPITOKEN")
        self.headers = {
            "X-Riot-Token": self.token
        }
        self.rate_limits = {
            "requests": [],
            "max_per_second": 20,
            "max_per_minute": 100
        }
        self.rate_limits = {
            "requests": [],
            "max_per_second": 20,
            "max_per_minute": 100
        }
    
    def check_rate_limit(self):
        current_time = time.time()
        self.rate_limits["requests"] = [t for t in self.rate_limits["requests"] if current_time - t < 60]

        if len(self.rate_limits["requests"]) >= self.rate_limits["max_per_minute"]:
            sleep_time = 60 - (current_time - self.rate_limits["requests"][0])
            if sleep_time > 0:
                logger.info(f"Rate limit exceeded, sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
        recent_requests = [t for t in self.rate_limits["requests"] 
                          if current_time - t < 1]
        if len(recent_requests) >= self.rate_limits["max_per_second"]:
            logger.info(f"Rate limit exceeded, sleeping for 1 second")
            time.sleep(1)
            