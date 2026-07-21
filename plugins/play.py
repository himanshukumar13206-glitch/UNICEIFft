from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream

from main import app, calls
from helpers.queue import add_to_queue, current_track, clear_queue, is_active
from helpers.youtube import resolve_track


@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: `/play <song name or YouTube link>`")
        return

    query = message.text.split(None, 1)[1]
    status = await message.reply_text(f"🔎 Searching for **{query}**...")

    track = await resolve_track(query)
    if not track or not track.get("stream_url"):
        await status.edit_text(
            "❌ Couldn't find or resolve that track (it may be too long, "
            "region-locked, or unavailable)."
        )
        return

    track["requested_by"] = message.from_user.mention if message.from_user else "Unknown"
    chat_id = message.chat.id
    already_playing = is_active(chat_id)
    position = add_to_queue(chat_id, track)

    if already_playing:
        await status.edit_text(
            f"➕ Queued **{track['title']}** at position #{position} "
            f"(requested by {track['requested_by']})"
        )
        return

    try:
        await calls.play(chat_id, MediaStream(track["stream_url"]))
    except Exception as e:
        clear_queue(chat_id)
        await status.edit_text(f"❌ Failed to start stream: `{e}`")
        return

    await status.edit_text(
        f"▶️ **Now playing:** {track['title']}\n"
        f"Requested by: {track['requested_by']}"
    )


@app.on_message(filters.command("queue") & filters.group)
async def queue_cmd(_, message: Message):
    from helpers.queue import get_queue

    q = get_queue(message.chat.id)
    if not q:
        await message.reply_text("Queue is empty. Use /play to add a track.")
        return

    lines = [f"**Current queue ({len(q)} tracks):**"]
    for i, t in enumerate(q):
        marker = "▶️" if i == 0 else f"{i}."
        lines.append(f"{marker} {t['title']} — {t.get('requested_by', 'Unknown')}")
    await message.reply_text("\n".join(lines))
