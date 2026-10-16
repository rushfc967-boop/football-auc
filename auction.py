import asyncio
import time
import math
from config import COUNTDOWN_SECONDS, REMINDER_AT, SQUAD_SIZE, MIN_BASE_PRICE
from database import (
    get_state, update_state, get_all_teams, get_team, update_team,
    get_player, update_player, log_sold, get_min_base_price, get_sold_by_team,
    get_next_player_in_set, get_set_players, get_set_position, get_total_sets
)

SET_ICONS = {"GK": "🧤", "DEF": "🛡️", "MID": "🎯", "FWD": "⚡"}
SET_LABELS = {"GK": "GOALKEEPERS", "DEF": "DEFENDERS", "MID": "MIDFIELDERS", "FWD": "FORWARDS"}

_next_lock = asyncio.Lock()


def find_team_by_user(user_id, username):
    for t in get_all_teams():
        owner = t["owner_username"]
        if not owner:
            continue
        if owner.isdigit() and int(owner) == user_id:
            return t
        if owner.startswith("@") and username and owner.lower() == ("@" + username).lower():
            return t
    return None


def set_header(set_id):
    pos, part = get_set_position(set_id)
    return f"{SET_ICONS.get(pos, '📦')} {SET_LABELS.get(pos, pos)} (Part {part})"


def validate_bid(user_id, username, amount):
    state = get_state()
    if state["status"] == "paused":
        return False, "⏸️ Auction is paused."
    if state["status"] != "live":
        return False, "❌ Auction is not live"
    team = find_team_by_user(user_id, username)
    if not team:
        return False, "❌ You are not an owner of any team"
    if team["slots_left"] <= 0:
        return False, f"❌ {team['name']} squad is full (15/15)"
    if state["highest_team_id"] == team["id"]:
        return False, "❌ You are already the highest bidder"

    player = get_player(state["current_player_id"]) if state["current_player_id"] else None
    if not player:
        return False, "❌ No active player"

    base_ceil = math.ceil(player["base_price"])

    if state["highest_bid"] == 0:
        # First bid — must be >= ceil(base)
        if amount < base_ceil:
            return False, f"❌ Min first bid: {base_ceil}M (base: {player['base_price']}M → rounded up)"
    else:
        if amount <= state["highest_bid"]:
            return False, f"❌ Bid must be > {state['highest_bid']}M"

    remaining_budget = team["budget"] - team["spent"]
    if amount > remaining_budget:
        return False, f"❌ Insufficient budget (max {remaining_budget:.2f}M)"
    slots_after = team["slots_left"] - 1
    min_base = get_min_base_price() or MIN_BASE_PRICE
    max_allowed = remaining_budget - (slots_after * min_base)
    if amount > max_allowed:
        return False, f"❌ Max allowed: {max_allowed:.2f}M"
    return True, team


def build_live_text(player, state, countdown=None):
    set_id = state["current_set"] or 1
    lines = [f"📦 SET {set_id}: {set_header(set_id)}", "━━━━━━━━━━━━━━━━━━━",
             f"⚽ {player['name']}",
             f"📍 {player['position']} | 💰 Base: {math.ceil(player['base_price'])}M", ""]
    if state["highest_bid"] > 0 and state["highest_team_id"]:
        team = get_team(state["highest_team_id"])
        if team:
            lines.append(f"🔥 Current: {state['highest_bid']}M by {team['name']}")
    if countdown is not None and countdown > 0:
        lines.append(f"⏰ {countdown} seconds left!")
    elif countdown is not None:
        lines.append("🔓 Bidding OPEN")
    lines.append("")
    lines.append("💡 /bid <amount> to bid")
    return "\n".join(lines)


async def update_live_message(bot, chat_id, text):
    state = get_state()
    if state["live_message_id"]:
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=state["live_message_id"], text=text)
            return
        except Exception:
            pass
    msg = await bot.send_message(chat_id=chat_id, text=text)
    update_state(live_message_id=msg.message_id)


async def show_set_preview(bot, chat_id, set_id):
    players = get_set_players(set_id)
    lines = [f"📋 SET {set_id} PREVIEW",
             f"📦 {set_header(set_id)} — {len(players)} players",
             "━━━━━━━━━━━━━━━━━━━"]
    for i, p in enumerate(players, 1):
        lines.append(f"{i}. {p['name']} ({p['position']}) — {math.ceil(p['base_price'])}M")
    lines.append("━━━━━━━━━━━━━━━━━━━")
    text = "\n".join(lines)
    for i in range(0, len(text), 4000):
        await bot.send_message(chat_id=chat_id, text=text[i:i+4000])


async def finalize_sold(bot, chat_id):
    state = get_state()
    player = get_player(state["current_player_id"])
    if not player:
        return
    if state["highest_bid"] > 0 and state["highest_team_id"]:
        team = get_team(state["highest_team_id"])
        price = state["highest_bid"]
        new_spent = team["spent"] + price
        new_slots = team["slots_left"] - 1
        update_team(team["id"], spent=new_spent, slots_left=new_slots)
        update_player(player["id"], status="sold")
        log_sold(player["id"], team["id"], price)
        remaining = team["budget"] - new_spent
        await bot.send_message(chat_id=chat_id,
            text=(f"━━━━━━━━━━━━━━━━━━━\n🔨 SOLD!\n⚽ {player['name']}\n"
                  f"👥 {team['name']}\n💰 {price}M\n━━━━━━━━━━━━━━━━━━━\n"
                  f"💵 {team['name']}: {remaining:.2f}M | {new_slots} slots"))
    else:
        update_player(player["id"], status="unsold")
        await bot.send_message(chat_id=chat_id,
            text=(f"━━━━━━━━━━━━━━━━━━━\n🔨 UNSOLD!\n"
                  f"⚽ {player['name']} | Base: {math.ceil(player['base_price'])}M\n━━━━━━━━━━━━━━━━━━━"))
    update_state(current_player_id=None, highest_bid=0, highest_team_id=None, last_bid_time=0, last_reminder=None)


async def next_player(bot, chat_id):
    async with _next_lock:
        state = get_state()
        if state["current_player_id"]:
            p = get_player(state["current_player_id"])
            if p and p["status"] == "pending":
                return

        set_id = state["current_set"] or 1
        total = get_total_sets()
        player = get_next_player_in_set(set_id)

        # Current set finished — pause and wait for /resume
        if not player:
            if set_id >= total:
                await end_auction(bot, chat_id)
                return
            next_set = set_id + 1
            update_state(status="set_complete", current_set=next_set)
            await bot.send_message(
                chat_id=chat_id,
                text=f"✅ SET {set_id} COMPLETE\n━━━━━━━━━━━━━━━━━━━"
            )
            await asyncio.sleep(1)
            await show_set_preview(bot, chat_id, next_set)
            await asyncio.sleep(1)
            await bot.send_message(
                chat_id=chat_id,
                text=f"👑 Host: /resume to start SET {next_set}"
            )
            return

        update_state(
            current_player_id=player["id"],
            highest_bid=0, highest_team_id=None,
            last_bid_time=time.time(),
            last_reminder=None, live_message_id=None
        )
        text = (f"📦 SET {set_id}: {set_header(set_id)}\n━━━━━━━━━━━━━━━━━━━\n"
                f"⚽ {player['name']}\n📍 {player['position']} | 💰 Base: {math.ceil(player['base_price'])}M\n"
                "🔓 Bidding OPEN\n━━━━━━━━━━━━━━━━━━━\n💡 /bid <amount> to bid")
        msg = await bot.send_message(chat_id=chat_id, text=text)
        update_state(live_message_id=msg.message_id)


async def auction_loop(bot, chat_id):
    while True:
        await asyncio.sleep(0.5)
        try:
            state = get_state()
            if state["status"] == "paused":
                continue
            if state["status"] == "set_complete":
                continue
            if state["status"] != "live":
                continue
            if not state["current_player_id"]:
                await next_player(bot, chat_id)
                continue

            player = get_player(state["current_player_id"])
            if not player:
                update_state(current_player_id=None)
                continue

            if state["last_bid_time"] == 0:
                update_state(last_bid_time=time.time())
                continue

            elapsed = time.time() - state["last_bid_time"]
            remaining = COUNTDOWN_SECONDS - elapsed
            countdown = max(0, math.ceil(remaining))

            if remaining <= 0:
                await finalize_sold(bot, chat_id)
                if all_teams_full():
                    await end_auction(bot, chat_id)
                await asyncio.sleep(1.5)
                continue

            # Send reminder as SEPARATE message
            if countdown in REMINDER_AT and state["last_reminder"] != countdown:
                team = get_team(state["highest_team_id"]) if state["highest_team_id"] else None
                bid_line = f"🔥 {state['highest_bid']}M by {team['name']}" if team else "❌ No bids yet"
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"⏰ {countdown} seconds left!\n{bid_line}"
                )
                update_state(last_reminder=countdown)

        except Exception as e:
            print(f"[loop error] {e}")


def all_teams_full():
    teams = get_all_teams()
    return all(t["slots_left"] <= 0 for t in teams)


async def end_auction(bot, chat_id):
    update_state(status="ended")
    teams = get_all_teams()
    lines = ["🏁 AUCTION ENDED", "━━━━━━━━━━━━━━━━━━━", "📊 FINAL RESULTS", ""]
    for t in teams:
        sold = get_sold_by_team(t["id"])
        spent = t["spent"]
        left = t["budget"] - spent
        lines.append(f"🏆 {t['name']}")
        lines.append(f"   Spent: {spent:.2f}M | Left: {left:.2f}M | Squad: {len(sold)}/15")
        for s in sold:
            lines.append(f"   • {s['name']} ({s['position']}) — {s['price']}M")
        lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━")
    text = "\n".join(lines)
    for i in range(0, len(text), 4000):
        await bot.send_message(chat_id=chat_id, text=text[i:i+4000])


def pause_auction():
    state = get_state()
    if state["status"] != "live":
        return False, "Auction is not live"
    update_state(status="paused")
    return True, "paused"


def resume_auction():
    state = get_state()
    if state["status"] != "paused":
        return False, "Auction is not paused"
    # Resume with fresh 10s timer IF timer was already running
    if state["highest_bid"] > 0:
        update_state(status="live", last_bid_time=time.time(), last_reminder=None)
    else:
        update_state(status="live")
    return True, "resumed"


async def skip_player(bot, chat_id):
    state = get_state()
    if state["status"] != "live":
        return False, "Auction not live"
    if not state["current_player_id"]:
        return False, "No active player"
    player = get_player(state["current_player_id"])
    if not player:
        return False, "Player not found"
    update_player(player["id"], status="unsold")
    await bot.send_message(chat_id=chat_id, text=f"⏭️ SKIPPED\n⚽ {player['name']} → UNSOLD")
    update_state(current_player_id=None, highest_bid=0, highest_team_id=None, last_bid_time=0, last_reminder=None)
    return True, "skipped"


async def start_round2(bot, chat_id):
    from database import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM players WHERE status='unsold'")
    cnt = cur.fetchone()[0]
    cur.close()
    conn.close()
    if cnt == 0:
        return False, "No unsold players"
    from database import _execute
    conn = get_conn()
    _execute(conn, "UPDATE players SET status='pending' WHERE status='unsold'")
    conn.close()
    update_state(status="live", last_bid_time=0, highest_bid=0,
                 highest_team_id=None, current_player_id=None,
                 last_reminder=None, live_message_id=None)
    await bot.send_message(chat_id=chat_id, text=f"📦 ROUND 2: {cnt} unsold players back in pool")
    return True, "started"


def export_csv():
    import os, csv
    from config import EXPORT_DIR
    from database import get_conn
    os.makedirs(EXPORT_DIR, exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()

    p1 = os.path.join(EXPORT_DIR, "final_squads.csv")
    with open(p1, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Team", "Player", "Position", "Price"])
        cur.execute("SELECT t.name, p.name, p.position, s.price FROM sold s JOIN teams t ON t.id=s.team_id JOIN players p ON p.id=s.player_id ORDER BY t.name, s.id")
        for r in cur.fetchall():
            w.writerow(list(r))

    p2 = os.path.join(EXPORT_DIR, "team_summary.csv")
    with open(p2, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Team", "Owner", "Spent", "Left", "SquadCount"])
        cur.execute("SELECT name, owner_username, spent, budget, slots_left FROM teams ORDER BY name")
        for r in cur.fetchall():
            w.writerow([r[0], r[1], round(r[2], 2), round(r[3]-r[2], 2), 15-r[4]])

    p3 = os.path.join(EXPORT_DIR, "unsold_players.csv")
    with open(p3, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Player", "Position", "BasePrice"])
        cur.execute("SELECT name, position, base_price FROM players WHERE status='unsold'")
        for r in cur.fetchall():
            w.writerow(list(r))

    cur.close()
    conn.close()
    return [p1, p2, p3]


def get_top_buys(limit=10):
    from database import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT p.name, p.position, s.price, t.name FROM sold s JOIN players p ON p.id=s.player_id JOIN teams t ON t.id=s.team_id ORDER BY s.price DESC LIMIT %s" if hasattr(conn, 'cursor') and 'psycopg' in str(type(conn)).lower() else "SELECT p.name, p.position, s.price, t.name FROM sold s JOIN players p ON p.id=s.player_id JOIN teams t ON t.id=s.team_id ORDER BY s.price DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"pname": r[0], "pos": r[1], "price": r[2], "tname": r[3]} for r in rows]
