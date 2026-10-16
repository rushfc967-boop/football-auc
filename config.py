import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing!")

BUDGET_PER_TEAM = 500.0
SQUAD_SIZE = 15
MIN_TEAMS = 2
MAX_TEAMS = 20

COOLDOWN_SECONDS = 3
COUNTDOWN_SECONDS = 10
TOTAL_TIMER = COOLDOWN_SECONDS + COUNTDOWN_SECONDS
REMINDER_AT = [10, 5, 3, 2, 1]

SET_ORDER = ["GK", "DEF", "MID", "FWD"]
SET_NAMES = {"GK": "🧤 GOALKEEPERS", "DEF": "🛡️ DEFENDERS", "MID": "🎯 MIDFIELDERS", "FWD": "⚡ FORWARDS"}

MIN_BASE_PRICE = 3
# DB path from env (Railway volume) or local default
DB_PATH = os.getenv("DB_PATH", "auction.db")
EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
