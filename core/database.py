import json
import os
from datetime import datetime, timedelta

class CompanyDatabase:
    def __init__(self, db_path="data/company_state.json"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.state = self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {
            "company_name": "Antigravity Music",
            "balance": 100.0,
            "simulated_date": datetime.now().isoformat(),
            "catalog": [],
            "subscriptions": [],
            "marketing_log": [],
            "billing_log": []
        }

    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.state, f, indent=4)

    def add_song(self, song_data):
        self.state["catalog"].append(song_data)
        self.save()

    def update_balance(self, amount):
        self.state["balance"] += amount
        self.save()

    def log_event(self, category, message):
        timestamp = self.state["simulated_date"]
        event = {"timestamp": timestamp, "message": message}
        if category not in self.state:
            self.state[category] = []
        self.state[category].append(event)
        self.save()
