import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"

def get_config():
    # Load config at runtime
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def is_admin(user_id: int) -> bool:
    config = get_config()
    admin_ids = config.get("admin_ids", [])
    return user_id in admin_ids
