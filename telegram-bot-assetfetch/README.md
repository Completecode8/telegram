# AssetFetch Pro – Telegram Bot File Structure

This project provides a robust, modular, and production-ready foundation for a high-performance Telegram bot (AssetFetch Pro) that downloads requested files from specific websites, enforces group/user subscription and authentication, and manages file distribution via Google Drive and link shorteners.

---

## Directory and File Overview

```
telegram-bot-assetfetch/
│
├── .gitignore               # Ignore secrets, logs, downloads, __pycache__, backups, etc.
├── LICENSE                  # Project license.
├── README.md                # Project overview and usage.
├── requirements.txt         # Python dependencies.
├── runtime.txt              # Python runtime version.
├── docker-compose.yml       # (Optional) Docker multi-container orchestration.
├── Dockerfile               # Docker build for bot+dependencies.
│
├── scripts/                 # Helper scripts for setup, run, backup, cleanup, Windows/Linux.
│   ├── setup.py
│   ├── start_bot.bat
│   ├── start_bot.sh
│   └── backup_and_cleanup.py
│
├── config/                  # All runtime and sensitive configuration.
│   ├── config.example.json  # Template config for safe sharing.
│   ├── config.json          # (Excluded!) Stores real tokens, admin/channel IDs.
│   ├── domains.json         # Defines supported sites and domain rewriting rules.
│   ├── admins.json          # List of admin Telegram IDs.
│   ├── channels.json        # Channel links/IDs for user eligibility.
│   ├── allowed_groups.db    # SQLite: Authorized group registry.
│   ├── credentials/         # API/service secrets.
│   │   ├── gdrive1.json
│   │   └── gdrive2.json
│   └── chrome_profile/      # Selenium Chrome user-data-dir (pre-logged; not in repo)
│
├── downloads/               # All downloaded files (per group/user/task, deleted after upload).
│
├── logs/
│   └── bot.log              # Rotating logs for all events/warnings/errors.
│
├── backups/                 # 8h periodic DB/config backups, purged after 48h.
│
├── src/                     # All bot and app source code (modularized).
│   ├── __init__.py
│   ├── main.py              # Main entrypoint, loads config & starts asyncio bot.
│   ├── queue_manager.py     # Persistence & prioritised task queue.
│   ├── subscription.py      # Plan switching, group/user quotas.
│   ├── file_handler.py      # Downloads/Chrome automations, uploads to Drive.
│   ├── shrinkme_api.py      # ShrinkMe.io API logic.
│   ├── admin_commands.py    # All admin-only command handling.
│   ├── auth.py              # User, channel, group verification/auth.
│   ├── user_utils.py        # User state, eligibility, limits.
│   ├── group_utils.py       # Group state, banned sites/plans.
│   ├── commands/            # Each bot command modularized.
│   │   ├── __init__.py
│   │   ├── start_stop.py
│   │   ├── group_approve.py
│   │   ├── subscriptions.py
│   │   ├── queue_admin.py
│   │   ├── error_control.py
│   │   └── help.py
│   └── utils/               # Utilities: logging, headless browser, power-control, backups.
│       ├── logger.py
│       ├── chrome_utils.py
│       ├── sleep_blocker.py
│       └── backup.py
│
└── tests/                   # (Optional) Pytest-based tests, for robust CI/CD.

```

---

## Key Design Principles

- **Separation of Concerns:** Each module/script serves a single purpose.
- **Security:** All secrets/tokens and user credentials are excluded from version control.
- **Extensibility:** Easy to add new commands, sites, integrations.
- **Resilience:** Automated backup, cleanup, recovery, and power control.
- **Containerization:** Docker/Docker Compose for isolation and portability.

---

## Getting Started

1. Copy `config/config.example.json` to `config/config.json` and fill in secrets.
2. Install Python dependencies (`pip install -r requirements.txt`).
3. Prepare your Chrome profile, Google credentials, and ShrinkMe API key.
4. Run with `python src/main.py` or use provided scripts/Docker as needed.

---

This structure is ready for industry-grade development and scaling.
