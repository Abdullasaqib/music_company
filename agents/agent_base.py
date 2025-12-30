import json
import os
import time
import yaml
import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'company_state.json')
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'run.log')
CHECKPOINT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'checkpoints')

# Ensure directories exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

class AgentBase:
    def __init__(self, name):
        self.name = name
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def load_state(self):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"catalog": [], "marketing_log": [], "billing_log": [], "balance": 0}

    def save_state(self, state):
        # Save main state
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)
            
        # Create Timestamped Checkpoint
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        checkpoint_path = os.path.join(CHECKPOINT_DIR, f"state_{timestamp}.json")
        with open(checkpoint_path, 'w') as f:
            json.dump(state, f, indent=4)

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {self.name}: {message}"
        print(formatted)
        
        with open(LOG_FILE, 'a') as f:
            f.write(formatted + "\n")
