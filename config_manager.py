# Config-Manager
# Simple config file handler for PicPile
# Daisy Universe [D]
# 05 . 11 . 25

import json

# just allows us to get/set easily
class cfgmgr:
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = self._load_config()

    def _load_config(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, key, default=None):
         return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self._save_config()
        
    def _save_config(self):
        with open(self.filepath, 'w') as f:
            json.dump(self._data, f, indent=4)

    def delete(self, key):
        if key in self._data:
            del self._data[key]
            self._save_config()
        else:
            print(f"Key '{key}' not found in config.")