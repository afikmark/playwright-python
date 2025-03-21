import json
import os

from settings import ROOT_DIR
from local_config import PASSWORD


class Config:
    SUPPORTED_ENVS = ['dev', 'qa']

    def __init__(self, env):
        with open(f'{ROOT_DIR}/config.json') as config:
            configs = json.load(config)
        self.base_url = configs['env'][env]
        self.user_name = configs['user_info']["default_name"]
        self.user_password = os.environ.get("PASSWORD", PASSWORD)