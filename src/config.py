import json
from pathlib import Path

EXPENSES_FILE = Path("data/expenses.csv")
CATEGORIES_FILE = Path("data/categories.csv")
USER_CONFIG_FILE = Path("data/user_config.json")

DEFAULT_CONFIG = {
    'currency': 'JOD',
    'monthly_budget': 500
}

def load_user_config():
    if not USER_CONFIG_FILE.exists():
        # Create the file if it doesn't exist
        with open(USER_CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    with open(USER_CONFIG_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_CONFIG

USER_CONFIG = load_user_config()