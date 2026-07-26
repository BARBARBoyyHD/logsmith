from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from logsmith.config import load_config

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

_CONFIG_CACHE = None


def _config():
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        _CONFIG_CACHE = load_config()
    return _CONFIG_CACHE


def get_worksheet():
    cfg = _config()
    creds = Credentials.from_service_account_file(cfg["SERVICE_ACCOUNT_KEY_PATH"], scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(CONFIG["SHEET_ID"])
    month_label = datetime.now().strftime("%b %y")
    try:
        ws = sheet.worksheet(month_label)
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title=month_label, rows=200, cols=9)
        ws.append_row([
            "No", "Date", "Category", "Description",
            "Business Impact", "Skill / Competency", "Project",
            "Evidence", "Recognition",
        ])
    return ws


def next_number(ws):
    vals = ws.col_values(1)
    return len([v for v in vals if v and v != "No"]) + 1


def append_row(ws, row):
    ws.append_row(row)


def get_all_rows(ws):
    return ws.get_all_values()
