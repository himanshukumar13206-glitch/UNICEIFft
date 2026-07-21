from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream

from main import app, calls
from helpers.queue import clear_queue, is_active, pop_current, current_track


@app.on_message(filters.command("pause") & filters.group)
async def pause_cmd(_, message: Message):
    chat_id = message.chat.id
    if not is_active(chat_id):
        await message.reply_text("Nothing is playing right now.")
        return
    try:
        await calls.pause(chat_id)
        await message.reply_text("⏸ Paused.")
    except Exception as e:
        await message.reply_text(f"❌ Could not pause: `{e}`")


@app.on_message(filters.command("resume") & filters.group)
async def resume_cmd(_, message: Message):
    chat_id = message.chat.id
    if not is_active(chat_id):
        await message.reply_text("Nothing is playing right now.")
        return
    try:
        await calls.resume(chat_id)
        await message.reply_text("▶️ Resumed.")
    except Exception as e:
        await message.reply_text(f"❌ Could not resume: `{e}`")


@app.on_message(filters.command("skip") & filters.group)
async def skip_cmd(_, message: Message):
    chat_id = message.chat.id
    if not is_active(chat_id):
        await message.reply_text("Nothing is playing right now.")
        return

    next_track = pop_current(chat_id)
    if not next_track:
        try:
            await calls.leave_call(chat_id)
        except Exception:
            pass
        clear_queue(chat_id)
        await message.reply_text("⏭ Skipped. Queue is now empty, left the VC.")
        return

    try:
        await calls.play(chat_id, MediaStream(next_track["stream_url"]))
        await message.reply_text(f"⏭ Skipped. Now playing: **{next_track['title']}**")
    except Exception as e:
        await message.reply_text(f"❌ Could not skip: `{e}`")


@app.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, message: Message):
    chat_id = message.chat.id
    if not is_active(chat_id):
        await message.reply_text("Nothing is playing right now.")
        return
    try:
        await calls.leave_call(chat_id)
    except Exception:
        pass
    clear_queue(chat_id)
    await message.reply_text("⏹ Stopped and cleared the queue.")
