import asyncio
import logging

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update, StreamEnded

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
log = logging.getLogger("MusicBot")

# ---- Bot client (what users talk to / sends commands) ----
app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ---- Assistant/userbot client (actually joins the voice chat) ----
assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

# ---- PyTgCalls instance, bound to the assistant account ----
calls = PyTgCalls(assistant)


@calls.on_update()
async def on_stream_update(client: PyTgCalls, update: Update):
    """Auto-advance the queue when a track finishes."""
    if isinstance(update, StreamEnded):
        from helpers.queue import pop_current, clear_queue
        from pytgcalls.types import MediaStream

        chat_id = update.chat_id
        next_track = pop_current(chat_id)
        if next_track:
            try:
                await calls.play(chat_id, MediaStream(next_track["stream_url"]))
            except Exception as e:
                log.error(f"Failed to auto-play next track in {chat_id}: {e}")
                clear_queue(chat_id)
        else:
            try:
                await calls.leave_call(chat_id)
            except Exception:
                pass
            clear_queue(chat_id)


async def main():
    # Import plugins AFTER app/assistant/calls exist, since they import from this module
    import plugins.start  # noqa: F401
    import plugins.play  # noqa: F401
    import plugins.controls  # noqa: F401

    await assistant.start()
    await app.start()
    await calls.start()

    log.info("Music bot is up and running.")
    await asyncio.Event().wait()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
