import json
import os

from settings import ROOT_DIR
try:
    from local_config import PASSWORD
except ImportError:
    PASSWORD = os.environ.get("PASSWORD")


class Config:
    SUPPORTED_ENVS = ['dev', 'qa']

    def __init__(self, env):
        with open(f'{ROOT_DIR}/config.json') as config:
            configs = json.load(config)
        self.base_url = configs['env'][env]
        self.user_name = configs['user_info']["default_name"]
        self.user_password = PASSWORD