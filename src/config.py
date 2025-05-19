import os
import json

class Config:
    def __init__(self):
        self.config_file = 'config.json'
        self.api_key = None
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.api_key = config.get('api_key')

    def save_config(self, api_key):
        with open(self.config_file, 'w') as f:
            json.dump({'api_key': api_key}, f)
        self.api_key = api_key

    def get_api_key(self):
        return self.api_key