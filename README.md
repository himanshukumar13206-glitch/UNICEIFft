# Telegram VC Music Bot

A Telegram bot that streams audio into a group's voice chat, built with
[Pyrogram](https://docs.pyrogram.org/), [PyTgCalls](https://pytgcalls.github.io/)
and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## How it works

Telegram bots can't join voice chats directly — only user accounts can. So
this project runs **two** clients:

1. **`app`** — the bot (via `BOT_TOKEN`) that users send commands to.
2. **`assistant`** — a regular Telegram account (via `SESSION_STRING`) that
   actually joins the voice chat and streams the audio, controlled through
   PyTgCalls.

## Commands

| Command | Description |
|---|---|
| `/play <name or link>` | Search YouTube (or use a direct link) and play/queue it |
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/skip` | Skip to the next queued track |
| `/stop` | Stop and clear the queue, leave the VC |
| `/queue` | Show the current queue |
| `/ping` | Check bot latency |

## Setup

### 1. Get credentials
- `API_ID` / `API_HASH`: from https://my.telegram.org (log in with any account)
- `BOT_TOKEN`: create a bot with [@BotFather](https://t.me/BotFather)
- `SESSION_STRING`: run `python3 generate_session.py` locally and log in
  with the account you want to use as the assistant (this account will
  physically join the VC — use a real user account, not the bot)

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# then fill in .env with your values
```

### 4. Run locally
```bash
python3 main.py
```

### 5. In your Telegram group
1. Add the **bot** to the group.
2. Add the **assistant account** (the one you generated `SESSION_STRING` for) to the group too.
3. Promote both to admin (the assistant needs admin, or at least permission to manage voice chats, in many groups).
4. Start a voice chat in the group.
5. Send `/play <song name>`.

## Deploying on Render (Web Service)

This repo is set up to run as a Render **Web Service** (needed for
Render's free tier, which doesn't offer free background workers). Since
Telegram bots don't normally need to listen on a port, `main.py` starts a
tiny `aiohttp` server (`GET /` → `"Music bot is alive."`) purely so
Render's health check passes and the service isn't killed.

1. Push this project to a GitHub repo.
2. In Render, choose **New → Blueprint**, point it at your repo — it will
   read `render.yaml` automatically. (Or manually create a **Web
   Service** with:
   - **Build command:** `apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt`
   - **Start command:** `python3 main.py`)
3. Fill in the environment variables (`API_ID`, `API_HASH`, `BOT_TOKEN`,
   `SESSION_STRING`, etc.) in the Render dashboard — do **not** commit
   these to git. Render sets `PORT` automatically; you don't need to add it.
4. Deploy. Check the logs for `Music bot is up and running.`

**Free-tier caveat:** Render's free web services spin down after periods
of inactivity and spin back up on the next incoming request. Since
nothing calls your health-check URL on its own, your bot may go to sleep
and briefly delay before responding to the next Telegram command. A
free/paid uptime-pinger (e.g. cron-job.org hitting your Render URL every
few minutes) works around this — or upgrade to a paid instance for
always-on.

## Notes & limitations

- This is a lean skeleton meant to be extended — it supports a single
  linear per-chat queue, YouTube search/links, and basic playback
  controls. It doesn't include Spotify/Resso/Apple Music resolution,
  multi-quality streams, or a database — those are common next additions.
- yt-dlp occasionally gets rate-limited by YouTube; supplying a
  `COOKIES_FILE` (exported from a logged-in browser session) helps.
- Respect Telegram's [Terms of Service](https://telegram.org/tos) and
  copyright law in whatever content you stream.
