import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing!")

OWNER_ID = 7558715645

BUDGET_PER_TEAM = 500.0
SQUAD_SIZE = 15
MIN_TEAMS = 2
MAX_TEAMS = 20

# Timer: 15s countdown, reminders at 10, 5, 3
COUNTDOWN_SECONDS = 15
REMINDER_AT = [10, 5, 3]

SET_ORDER = ["GK", "DEF", "MID", "FWD"]
SET_NAMES = {"GK": "🧤 GOALKEEPERS", "DEF": "🛡️ DEFENDERS", "MID": "🎯 MIDFIELDERS", "FWD": "⚡ FORWARDS"}

MIN_BASE_PRICE = 3
DB_PATH = os.getenv("DB_PATH", "auction.db")
EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
