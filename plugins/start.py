from pyrogram import filters
from pyrogram.types import Message

from main import app

HELP_TEXT = """
**🎵 Music Bot Commands**

/play <song name or link> — play/queue a track in the VC
/pause — pause playback
/resume — resume playback
/skip — skip to the next track in queue
/stop — stop playback and clear queue
/queue — show current queue
/ping — check bot latency

Add this bot **and** its assistant account to your group, promote both to admin, start a voice chat, then use /play.
"""


@app.on_message(filters.command("start") & filters.private)
async def start_cmd(_, message: Message):
    await message.reply_text(
        "👋 Hi! I'm a Telegram voice-chat music bot.\n"
        "Add me to a group as admin and use /play to stream music.\n\n"
        "Send /help to see all commands."
    )


@app.on_message(filters.command("help"))
async def help_cmd(_, message: Message):
    await message.reply_text(HELP_TEXT)


@app.on_message(filters.command("ping"))
async def ping_cmd(_, message: Message):
    import time

    start = time.perf_counter()
    msg = await message.reply_text("Pinging...")
    took = (time.perf_counter() - start) * 1000
    await msg.edit_text(f"🏓 Pong! `{took:.2f} ms`")
