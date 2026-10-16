import asyncio
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

from config import BOT_TOKEN, MIN_TEAMS, MAX_TEAMS, SQUAD_SIZE, OWNER_ID
from database import (
    init_db, get_state, update_state, get_all_teams, get_team,
    add_team, get_sold_by_team, count_players, count_by_position,
    reset_auction, get_player, build_sets, get_set_players,
    get_total_sets, count_pending_in_set
)
from auction import (
    validate_bid, auction_loop, next_player, pause_auction,
    resume_auction, end_auction, build_live_text, update_live_message,
    find_team_by_user, skip_player, start_round2, export_csv, get_top_buys,
    show_set_preview, set_header
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_host(user_id):
    return get_state()["host_id"] == user_id


def host_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not is_host(update.effective_user.id):
            await update.message.reply_text("❌ Only the HOST can run this command.")
            return
        return await func(update, context)
    return wrapper


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state()
    user = update.effective_user
    if state["host_id"]:
        if state["host_id"] == user.id:
            await update.message.reply_text(
                f"👑 You are HOST.\nSetup: {state['status']}\n\n"
                f"/add_teams /lock /start_auction\n/pause /resume /skip /end"
            )
        else:
            await update.message.reply_text(f"ℹ️ HOST: {state['host_username']}\n/claim_host if inactive.")
        return
    kb = [[InlineKeyboardButton("🎯 Become Host", callback_data="become_host")]]
    await update.message.reply_text(
        "🏆 FOOTBALL AUCTION BOT\n━━━━━━━━━━━━━━━━━━━\nTap to become HOST!",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def become_host_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    state = get_state()
    user = q.from_user
    if state["host_id"]:
        await q.edit_message_text(f"❌ {state['host_username']} is already HOST.")
        return
    update_state(host_id=user.id, host_username=f"@{user.username or user.first_name}")
    await q.edit_message_text(f"✅ {user.first_name} is now HOST!\nNext: /add_teams")


async def claim_host(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state()
    user = update.effective_user
    if state["host_id"] == user.id:
        await update.message.reply_text("You are already HOST.")
        return
    update_state(host_id=user.id, host_username=f"@{user.username or user.first_name}")
    await update.message.reply_text(f"🔄 HOST changed to {user.first_name}")


@host_only
async def add_teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = update.message.text.split("\n")[1:]
    if not lines or all(not l.strip() for l in lines):
        await update.message.reply_text(
            "Usage:\n/add_teams\nBayern - @imfantommm\nReal Madrid - @user2"
        )
        return
    added, failed = 0, []
    for line in lines:
        line = line.strip()
        if not line or "-" not in line:
            continue
        parts = line.split("-", 1)
        name = parts[0].strip()
        owner_raw = parts[1].strip().lstrip("@")
        if not name or not owner_raw:
            failed.append(f"'{line}' (invalid)")
            continue
        owner_id = owner_raw if owner_raw.isdigit() else "@" + owner_raw
        if add_team(name, owner_id):
            added += 1
        else:
            failed.append(f"{name} (dup)")
    teams = get_all_teams()
    msg = f"✅ Added {added} team(s)."
    if failed:
        msg += f"\n❌ Failed: {', '.join(failed)}"
    msg += f"\n📊 Total: {len(teams)} (min {MIN_TEAMS}, max {MAX_TEAMS})"
    await update.message.reply_text(msg)


@host_only
async def lock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teams = get_all_teams()
    n = len(teams)
    if n < MIN_TEAMS:
        await update.message.reply_text(f"❌ Need at least {MIN_TEAMS} teams. Have {n}.")
        return
    if n > MAX_TEAMS:
        await update.message.reply_text(f"❌ Max {MAX_TEAMS} teams. Have {n}.")
        return
    total = count_players()
    needed = n * SQUAD_SIZE
    if total < needed:
        await update.message.reply_text(f"❌ Not enough players ({total}, need {needed}).")
        return

    # Build random sets
    total_sets = build_sets()
    update_state(status="locked", current_set=1)

    await update.message.reply_text(
        f"🔒 LOCKED\n👥 Teams: {n}\n⚽ Players: {total}\n"
        f"📦 Sets created: {total_sets}\n\n📋 SET 1 PREVIEW below..."
    )
    await show_set_preview(context.bot, update.effective_chat.id, 1)
    await update.message.reply_text("Ready? /start_auction to begin!")


@host_only
async def start_auction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state()
    if state["status"] not in ("locked", "idle"):
        await update.message.reply_text(f"❌ Cannot start. Status: {state['status']}")
        return
    update_state(
        status="live", current_set=1,
        chat_id=update.effective_chat.id,
        highest_bid=0, highest_team_id=None, current_player_id=None,
        last_reminder=None, live_message_id=None
    )
    await update.message.reply_text("🏆 AUCTION STARTING...")
    if "auction_task" not in context.application.bot_data:
        task = asyncio.create_task(auction_loop(context.bot, update.effective_chat.id))
        context.application.bot_data["auction_task"] = task
    # Loop will pick up the first player automatically


async def bid_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /bid <amount>")
        return
    try:
        amount = float(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid amount")
        return
    user = update.effective_user
    ok, result = validate_bid(user.id, user.username, amount)
    if not ok:
        await update.message.reply_text(result)
        return
    update_state(highest_bid=amount, highest_team_id=result["id"],
                 last_bid_time=time.time(), last_reminder=None)
    state = get_state()
    player = get_player(state["current_player_id"]) if state["current_player_id"] else None
    if player:
        text = build_live_text(player, get_state(), None)
        await update_live_message(context.bot, update.effective_chat.id, text)
    await update.message.reply_text(f"✅ {result['name']} → {amount} M")


@host_only
async def pause_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok, msg = pause_auction()
    await update.message.reply_text("⏸️ PAUSED\n/resume (next set) or /auc_resume (unpause)" if ok else f"❌ {msg}")


async def auc_resume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume after /pause (timer resume)"""
    state = get_state()
    user_id = update.effective_user.id

    if not is_host(user_id) and user_id != OWNER_ID:
        await update.message.reply_text("❌ Host only.")
        return

    if state["status"] != "paused":
        await update.message.reply_text(f"❌ Auction paused nahi hai. Status: {state['status']}")
        return

    if state["highest_bid"] > 0:
        update_state(status="live", last_bid_time=time.time(), last_reminder=None)
    else:
        update_state(status="live")
    await update.message.reply_text("▶️ Auction RESUMED")


async def resume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start next set (only after SET COMPLETE)"""
    state = get_state()
    user_id = update.effective_user.id

    if not is_host(user_id) and user_id != OWNER_ID:
        await update.message.reply_text("❌ Host only.")
        return

    if state["status"] != "set_complete":
        await update.message.reply_text(
            f"❌ No set waiting. Status: {state['status']}\n"
            f"(Use /auc_resume to unpause)"
        )
        return

    set_id = state["current_set"]
    await update.message.reply_text(f"▶️ Starting SET {set_id}...")
    await asyncio.sleep(1)
    update_state(
        status="live", last_bid_time=0, highest_bid=0,
        highest_team_id=None, current_player_id=None,
        last_reminder=None, live_message_id=None
    )


async def squad_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        name = " ".join(context.args)
        team = None
        for t in get_all_teams():
            if t["name"].lower() == name.lower():
                team = t
                break
        if not team:
            await update.message.reply_text("❌ Team not found")
            return
    else:
        user = update.effective_user
        team = find_team_by_user(user.id, user.username)
        if not team:
            await update.message.reply_text("❌ You don't own a team")
            return
    sold = get_sold_by_team(team["id"])
    lines = [f"🏆 {team['name']}",
             f"💰 Spent: {team['spent']:.2f} | Left: {team['budget']-team['spent']:.2f}",
             f"👥 Squad: {len(sold)}/15", ""]
    for s in sold:
        lines.append(f"• {s['name']} ({s['position']}) — {s['price']} M")
    await update.message.reply_text("\n".join(lines))


async def purse_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["💰 BUDGET", "━━━━━━━━━━━━━━━━━━━"]
    for t in get_all_teams():
        left = t["budget"] - t["spent"]
        lines.append(f"{t['name']}: {left:.2f} M | {t['slots_left']} slots")
    await update.message.reply_text("\n".join(lines))


async def pool_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = count_players()
    await update.message.reply_text(f"⚽ TOTAL: {total}\n{count_by_position()}")


@host_only
async def end_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await end_auction(context.bot, update.effective_chat.id)


@host_only
async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reset_auction()
    await update.message.reply_text("🔄 Reset. /add_teams to start fresh.")


@host_only
async def skip_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok, msg = await skip_player(context.bot, update.effective_chat.id)
    if not ok:
        await update.message.reply_text(f"❌ {msg}")


@host_only
async def round2_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok, msg = await start_round2(context.bot, update.effective_chat.id)
    if not ok:
        await update.message.reply_text(f"❌ {msg}")


@host_only
async def export_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        files = export_csv()
        for path in files:
            with open(path, "rb") as f:
                await update.message.reply_document(document=f, filename=path.split("/")[-1])
    except Exception as e:
        await update.message.reply_text(f"❌ Export failed: {e}")


async def top_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 10
    if context.args:
        try:
            limit = int(context.args[0])
        except ValueError:
            pass
    tops = get_top_buys(limit)
    if not tops:
        await update.message.reply_text("📊 No players sold yet.")
        return
    lines = ["📊 TOP BUYS", "━━━━━━━━━━━━━━━━━━━"]
    for i, t in enumerate(tops, 1):
        lines.append(f"{i}. {t['pname']} ({t['pos']}) → {t['tname']} — {t['price']} M")
    await update.message.reply_text("\n".join(lines))


async def clearsession_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Owner only command.")
        return
    reset_auction()
    await update.message.reply_text(
        "🧹 SESSION CLEARED\n━━━━━━━━━━━━━━━━━━━\n"
        "✅ Teams deleted\n✅ Sold reset\n✅ Players pending\n"
        "✅ Host cleared\n\n/add_teams to start fresh."
    )


async def set_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = get_state()
    if state["status"] not in ("live", "paused"):
        await update.message.reply_text("Auction not running.")
        return
    set_id = state["current_set"] or 1
    pending = count_pending_in_set(set_id)
    header = set_header(set_id)
    await update.message.reply_text(
        f"📦 SET {set_id}: {header}\n"
        f"Pending in set: {pending}"
    )


async def set_commands(app: Application):
    cmds = [
        BotCommand("start", "Start / Become host"),
        BotCommand("claim_host", "Claim host if inactive"),
        BotCommand("add_teams", "Add teams (host)"),
        BotCommand("lock", "Lock + show SET 1 preview (host)"),
        BotCommand("start_auction", "Begin auction (host)"),
        BotCommand("bid", "Bid: /bid 2.5"),
        BotCommand("pause", "Pause (host)"),
        BotCommand("resume", "Start next set (host)"),
        BotCommand("auc_resume", "Resume paused auction (host)"),
        BotCommand("skip", "Skip player (host)"),
        BotCommand("squad", "View squad"),
        BotCommand("purse", "All budgets"),
        BotCommand("pool", "Player pool"),
        BotCommand("set", "Current set info"),
        BotCommand("top", "Top buys"),
        BotCommand("round2", "Re-auction unsold (host)"),
        BotCommand("export", "Download CSVs (host)"),
        BotCommand("end", "End auction (host)"),
        BotCommand("reset", "Reset all (host)"),
        BotCommand("clearsession", "Clear session (owner)"),
    ]
    await app.bot.set_my_commands(cmds)


async def error_handler(update, context):
    logger.error(f"Error: {context.error}")


def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("claim_host", claim_host))
    app.add_handler(CommandHandler("add_teams", add_teams))
    app.add_handler(CommandHandler("lock", lock_cmd))
    app.add_handler(CommandHandler("start_auction", start_auction))
    app.add_handler(CommandHandler("bid", bid_cmd))
    app.add_handler(CommandHandler("pause", pause_cmd))
    app.add_handler(CommandHandler("resume", resume_cmd))
    app.add_handler(CommandHandler("auc_resume", auc_resume_cmd))
    app.add_handler(CommandHandler("skip", skip_cmd))
    app.add_handler(CommandHandler("squad", squad_cmd))
    app.add_handler(CommandHandler("purse", purse_cmd))
    app.add_handler(CommandHandler("pool", pool_cmd))
    app.add_handler(CommandHandler("set", set_cmd))
    app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("round2", round2_cmd))
    app.add_handler(CommandHandler("export", export_cmd))
    app.add_handler(CommandHandler("end", end_cmd))
    app.add_handler(CommandHandler("reset", reset_cmd))
    app.add_handler(CommandHandler("clearsession", clearsession_cmd))
    app.add_handler(CallbackQueryHandler(become_host_callback, pattern="^become_host$"))
    app.add_error_handler(error_handler)
    app.post_init = set_commands

    print("🤖 Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
