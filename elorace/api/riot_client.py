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
        self.base_url = "https://developer.riotgames.com/apis#"
        self.token = os.getenv("RIOTAPITOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}"
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

    def get(self, endpoint: str, params: dict = None):
        """Realiza una solicitud GET a la API de Riot"""
        logger.info(f"Requesting {endpoint}")
        self._check_rate_limit()
        url = f"{self.base_url}{endpoint}"
        
        response = requests.get(url, headers=self.headers, params=params)
        self.rate_limits["requests"].append(time.time())
        
        if response.status_code == 200:
            logger.info(f"{response.status_code} - {response.json()}")
            return response.json()
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            time.sleep(retry_after)
            return self.get(endpoint, params)  # Reintentar
        else:
            return None