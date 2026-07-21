import os
from dotenv import load_dotenv

load_dotenv()

# ---- Telegram API credentials (get from https://my.telegram.org) ----
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")

# ---- Bot token (from @BotFather) ----
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ---- Assistant account session string (used to actually join the VC) ----
# Generate with: python3 generate_session.py
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# ---- Owner / sudo users (comma separated telegram user ids) ----
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
SUDO_USERS = [
    int(x) for x in os.environ.get("SUDO_USERS", "").split(",") if x.strip().isdigit()
]

# ---- Logger group / channel (optional, bot posts logs here) ----
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", "0"))

# ---- Misc ----
DURATION_LIMIT_MIN = int(os.environ.get("DURATION_LIMIT_MIN", "120"))  # max track length
COOKIES_FILE = os.environ.get("COOKIES_FILE", "")  # optional yt-dlp cookies.txt path

if not API_ID or not API_HASH or not BOT_TOKEN or not SESSION_STRING:
    print(
        "[WARNING] One or more required env vars (API_ID, API_HASH, BOT_TOKEN, "
        "SESSION_STRING) are missing. The bot will not start correctly until "
        "these are set."
    )
