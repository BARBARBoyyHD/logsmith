import sys
from pathlib import Path


PROJECT_ROOT = Path.cwd()
ENV_PATH = PROJECT_ROOT / ".env"


def load_config():
    config = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                key, _, val = line.partition("=")
                if val:
                    config[key.strip()] = val.strip()
    if "SHEET_ID" not in config:
        print("Error: SHEET_ID not found in .env")
        print("Copy .env.example to .env and fill in the values.")
        sys.exit(1)
    if "SERVICE_ACCOUNT_KEY_PATH" not in config:
        json_files = [f for f in PROJECT_ROOT.glob("*.json") if f.name != "opencode.json"]
        if json_files:
            config["SERVICE_ACCOUNT_KEY_PATH"] = str(json_files[0])
        else:
            print("Error: No JSON key file found. Set SERVICE_ACCOUNT_KEY_PATH in .env")
            sys.exit(1)
    return config
