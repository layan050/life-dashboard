import json
import os
from plugins.base import BasePlugin

class ManualPlugin(BasePlugin):
    def __init__(self, json_file_path: str):
        super().__init__("manual")
        self.json_file_path = json_file_path

    def fetch(self):
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        return {}