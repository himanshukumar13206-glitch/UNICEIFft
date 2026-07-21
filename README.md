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

## Deploying on Render

This repo ships with `render.yaml` and a `Procfile` for a **Background
Worker** deployment (this bot has no HTTP server, so it must be a worker,
not a web service).

1. Push this project to a GitHub repo.
2. In Render, choose **New → Blueprint**, point it at your repo — it will
   read `render.yaml` automatically. (Or manually create a **Background
   Worker**, build command `pip install -r requirements.txt`, start
   command `python3 main.py`.)
3. Fill in the environment variables (`API_ID`, `API_HASH`, `BOT_TOKEN`,
   `SESSION_STRING`, etc.) in the Render dashboard — do **not** commit
   these to git.
4. Deploy. Check the logs for `Music bot is up and running.`

## Notes & limitations

- This is a lean skeleton meant to be extended — it supports a single
  linear per-chat queue, YouTube search/links, and basic playback
  controls. It doesn't include Spotify/Resso/Apple Music resolution,
  multi-quality streams, or a database — those are common next additions.
- yt-dlp occasionally gets rate-limited by YouTube; supplying a
  `COOKIES_FILE` (exported from a logged-in browser session) helps.
- Respect Telegram's [Terms of Service](https://telegram.org/tos) and
  copyright law in whatever content you stream.
