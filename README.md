# ⚽ Football Auction Bot

Telegram bot for running football player auctions.

## Features
- Host selection via button
- Teams: 2-20
- Budget: 500M per team
- Squad: 15 players
- 12 sets (GK/DEF/MID/FWD × 3 parts)
- Auto-timer bidding (3s cooldown + 10s countdown)
- Auto SOLD / UNSOLD
- Pause / Resume / Skip (host only)
- Export CSVs

## Setup

1. Install Python 3.11 (TUR repo on Termux)
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your bot token
4. `python seed_players.py && python add_more_players.py && python add_extra_players.py`
5. `python bot.py`

## Commands
| Command | Purpose |
|---|---|
| /start | Become host |
| /add_teams | Add teams |
| /lock | Finalize + preview |
| /start_auction | Begin |
| /bid <amount> | Bid |
| /pause /resume | Control (host) |
| /skip | Skip player (host) |
| /squad /purse /pool | Info |
| /top /round2 /export | Extras |
| /end /reset | End / reset |
