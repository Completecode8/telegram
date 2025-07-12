import asyncio
import logging
import os
import sys
import json
import sqlite3
from pathlib import Path
from telegram.ext import ApplicationBuilder, CommandHandler, ChatMemberHandler

# Entry point and async main for bot development
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"
LOGS_PATH = PROJECT_ROOT / "logs" / "bot.log"
DB_PATH = PROJECT_ROOT / "config" / "allowed_groups.db"

# --- Logging setup (rotating, simple) ---
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(LOGS_PATH),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger("assetfetch_bot")
    return logger

# --- Config loader ---
def load_config():
    # For first run, allow dev to use config.example.json as fallback
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        try:
            with open(CONFIG_PATH.parent / "config.example.json", "r") as f:
                logging.warning("Falling back to example config! Please create config/config.json for production.")
                return json.load(f)
        except Exception as e:
            logging.error(f"Config load error: {e}")
            sys.exit(1)

# --- SQLite DB check/connection ---
def setup_db():
    # For now, only ensure allowed_groups.db exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Table is just a registry of allowed group IDs
    c.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            group_id TEXT PRIMARY KEY,
            is_approved INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 0,
            subscription_plan TEXT DEFAULT 'default'
        )
    """)
    conn.commit()
    conn.close()

# --- PTB bot setup (hander scaffolding comes later) ---
async def main():
    logger = setup_logger()
    logger.info("Starting AssetFetch Pro...")
    config = load_config()
    setup_db()
    token = config.get("telegram_token")
    if not token:
        logger.error("No `telegram_token` found in configuration.")
        sys.exit(1)
    # Build PTB app, ready for handlers
    app = ApplicationBuilder().token(token).concurrent_updates(True).build()
    logger.info("Bot application created. Ready to add handlers.")

    #--- Register all AssetFetch Pro commands (group and admin DM) ---
    from src.commands.command_registry import (
        bot_start, stop_bot, activate, unactivate, defaultsubscription, h12subscription,
        freesubscription, filesubscription, onesubscription, block_website, unblock_website, reset_queue,
        groupapprovae, allapprovaedgroup, deletethisapprovaedgroup, manage_this_group_queue,
        api_start_working, bot_error_fixed, bot_all_commandlist, bot_resume_task
    )
    from src.commands.group_approve import my_chat_member_handler

    app.add_handler(CommandHandler("bot-start", bot_start))
    app.add_handler(CommandHandler("stop-bot", stop_bot))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("unactivate", unactivate))
    app.add_handler(CommandHandler("defaultsubscription", defaultsubscription))
    app.add_handler(CommandHandler("12hsubscription", h12subscription))
    app.add_handler(CommandHandler("freesubscription", freesubscription))
    app.add_handler(CommandHandler("filesubscription", filesubscription))
    app.add_handler(CommandHandler("1subscription", onesubscription))
    app.add_handler(CommandHandler("block-website", block_website))
    app.add_handler(CommandHandler("unblock-website", unblock_website))
    app.add_handler(CommandHandler("reset-queue", reset_queue))

    app.add_handler(CommandHandler("groupapprovae", groupapprovae))
    app.add_handler(CommandHandler("allapprovaedgroup", allapprovaedgroup))
    app.add_handler(CommandHandler("deletethisapprovaedgroup", deletethisapprovaedgroup))
    app.add_handler(CommandHandler("manage-this-group-queue", manage_this_group_queue))
    app.add_handler(CommandHandler("api-start-working", api_start_working))
    app.add_handler(CommandHandler("bot-error-fixed", bot_error_fixed))
    app.add_handler(CommandHandler("bot-All-commandlist", bot_all_commandlist))
    app.add_handler(CommandHandler("bot_resume_task", bot_resume_task))

    # Add chat member handler for auto-approval enforcement
    app.add_handler(ChatMemberHandler(my_chat_member_handler, chat_member_types="my_chat_member"))

    # Start polling
    logger.info("Starting polling...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
