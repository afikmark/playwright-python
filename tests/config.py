import json
import os
from settings import ROOT_DIR
PASSWORD = os.environ["PASSWORD"]
PET_STORE_API_TOKEN = os.getenv("PET_STORE_API_TOKEN")


class Config:

    def __init__(self):
        with open(f'{ROOT_DIR}/config.json') as config:
            configs = json.load(config)
        self.user_name = configs['user_info']["default_name"]
        self.user_password = PASSWORD
        self.pet_store_api_token = PET_STORE_API_TOKEN